"""
Created on 19.12.2019

@author: Tanja Pfaffel
"""

#basics
import pandas as pd
import numpy as np

#plotly
import plotly.graph_objs as go
import plotly.express as px

#dash
import dash
import dash_core_components as dcc
import dash_html_components as html


# read in data (randomly generated data about production defects in car manufacturing plants)
data = pd.read_csv("myRandomData.csv")

#define counter dummy variable (for later group-bys)
data['Total']=1

# Prepare empty plots for first loading of website
fig = go.Figure()
boxplot = go.Figure()
scatter = go.Figure()

#predefine app
app = dash.Dash(__name__)

#########################
#set up dashboard layout
#########################
# for the layout we use the css stylesheet saved in the folder 'assets'
# with this, we can partition the dashboard into columns and rows
# we can define a row by html.Div([], className='row')
# the whole site is partitioned in 12 column parts. 
# if you want to define two columns, you use respectively 6 parts: 
# html.Div([html.Div([], classnames='six columns), html.Div([], className='six columns')], classname='row')

app.layout = html.Div(style={'backgroundColor': 'silver'}, children=[   
    
    #title
    html.H1(children='Interactive Dashboard for Data Visualization of Quality Data in Car Manufacturing Plants'),
    
    #line breaks
    html.Br(),
    html.Br(),
    
    # description text for dashboard (such that it only covers one part of website)
    html.Div([
        html.Div([
            html.Div('In production lines mistakes are made by humans and machines that lead to defects on the produced cars. Information about the defects and the reparation processes are saved in datasests, which are analyzed by car manufacturers.', style={'fontSize': 20}),
            html.Br()
        ], className="six columns" ),
        html.Div([
            html.Br()
        ], className="six columns" )
    ], className="row"),
    
    
    
    html.Div([
        
        #prevents that selections fields stand directly on left side of screen
        html.Div([
            html.Br()
        ], className="one columns"), 
        
        # Selection fields of features that influence the plot
        html.Div(style={'fontSize': 20}, children=[
            
            # Checkboxes for selection of plants
            html.H5('Select plant'),
            dcc.Checklist(
                id='plant', # ID for sending values to update function
                options=[   # Options for selection: 'label' describes the text shown on the website, 'value' is the internal value that is send to the update function
                    {'label': 'Munich', 'value': 'Munich'},
                    {'label': 'Sindelfingen', 'value': 'Sindelfingen'},
                    {'label': 'Ingolstadt', 'value': 'Ingolstadt'},
                ],
                value=['Munich'] # pre-set value when opening the website for the first time
            ),
            
            # Selection field to choose the feature you want to examine
            html.H5('Select feature to examine'),
            dcc.Dropdown(
                id='feature', # ID for sending values to update function
                options=[     # options for selection: 'label' describes the text shown on the website, 'value' is the internal value that is send to the update function
                    {'label': 'Rework activity', 'value': 'Rework Activity'},
                    {'label': 'Rework station', 'value': 'Rework Station'},
                    {'label': 'Defect location', 'value':'Defect Location'}, 
                    {'label': 'Defect type', 'value': 'Defect Type'}, 
                ],
                value='Rework Activity' # pre-set value when opening the website for the first time
            ),
            
            # Selection field stacked barplots 
            html.H5('Select if plot should be partitioned by pseudo defects'),
            dcc.Dropdown(
                id='stacks',  # ID for sending values to update function
                options=[     # Options for selection: 'label' describes the text shown on the website, 'value' is the internal value that is send to the update function
                    {'label': 'No partition', 'value':'No'},
                    {'label': 'Partition by pseudo defect', 'value':'Pseudo Defect'},
                ],
                value='No'   # pre-set value when opening the website for the first time
            ),
            
            # Slider for time frame in calendar weeks
            html.H5('Select calendar weeks'),
            dcc.RangeSlider(
                id='week', # ID for sending values to update function
                min=1,     # Minimum value of slider
                max=15,    # Maximum value of slider
                step=1,    # Stepsize
                marks=list(range(0,16)), # Numbers shown under the slider
                value=[1, 15]
            )
            
        ], className="four columns"),
        
        # To get a gap between selection fields and next plot (are in one row)
        html.Div([
            html.Br()
        ], className="one columns"), 
        
        
        #Scatterplot about weekly defect rate
        html.Div([
            
            # Heading
            html.H3(children='Frequency of defects per calender week'),
            
            # Include graphic to site. Figure is defined for first time as empty figure and then by update function
            dcc.Graph(id='scatter', figure = scatter)
            
        ], className="six columns"),
        
        
        
    ], className="row"),
    
    
    # 2 more graphics about defects
    html.Div(style={'padding': 60}, children=[
               
        # Barplot about freqeuncy occurence
        html.Div([
            
            html.H3(children='Frequency of occurence in dataset'),
            
            # Include graphic to site. Figure is defined for first time as empty figure and then by update function
            dcc.Graph(id = 'barplot', figure = fig)
                
        ], className="six columns"),
    
        
        #Boxplot showning distribution of rework duration
        html.Div([
            
            html.H3(children='Distribution of rework duration'),
            
            # Include graphic to site. Figure is defined for first time as empty figure and then by update function
            dcc.Graph(id = 'boxplot', figure = boxplot)
        
        ], className="six columns"),
        
        
    ], className="row"),
    

    #Add Logo
    #just small in the corner
    html.Div([
        html.Div([
            html.Br()
        ], className="eleven columns"),
        
        html.Div([
            
            html.Img(src=app.get_asset_url('KiMotion_Logo.png'), style={'height':'100%', 'width':'100%'})
            
        ], className="one columns")
    ], className="row")
])


##############################
# Define input and output for updating function
# Output: three plots (lineplot, barplot, boxplot)
# Input: Input of all selection boxes named above
##############################
            
@app.callback(
    [
         dash.dependencies.Output(component_id='barplot',component_property='figure'),
         dash.dependencies.Output(component_id='boxplot',component_property='figure'),
         dash.dependencies.Output(component_id='scatter',component_property='figure')
    ],
    [
         dash.dependencies.Input(component_id='plant', component_property='value'),
         dash.dependencies.Input(component_id='feature', component_property='value'),
         dash.dependencies.Input(component_id='stacks', component_property='value'),
         dash.dependencies.Input(component_id='week', component_property='value')
    ]
)


#############################
# Define UPDATING FUNCTION which is run when updating a selection box
#############################

# The input is the input of the selection boxes
def update_graph(plant, selected_variable, stacked, week):
    
    # Define the data for further plotting based on input of selection box plant and of slider week
    data_plant = data[np.logical_and(data['Plant'].isin(plant),data['Week'].isin(range(week[0], week[1]+1)))]
    
    # Define order of classes on y-axis (=classes of selected feature in selection box 'features')
    # Goal: have a consistent order for each variable in the two plots
    myorder = data_plant[selected_variable].value_counts(ascending=True).index
    # Order data such that rework activities that happen more often are shown on top of data set using prepared order
    data_plant[selected_variable]=pd.Categorical(data_plant[selected_variable],myorder)
    data_plant.sort_values(selected_variable)
    
    
    ############################
    # Update barplot showing frequency of occurence in dataset
    ############################
    
    # compute frequencies for frequency plot by groupin data regarding the selected feature
    # counter.columns = <Selected variable>, 'Pseudo Defect' (=Number of defects which are pseudodefects regarding the class), 
    # 'Total' (=Number of defects in total regarding the class),  'No Pseudo Defect' (=Number of defects which are NOT pseudo defect regarding the class)
    counter = data_plant[[selected_variable, 'Pseudo Defect', 'Total']].groupby(selected_variable).sum().reset_index()
    # add a new column to count the entries, which are NOT pseudo errors
    counter['No Pseudo Defect'] = counter['Total'] - counter['Pseudo Defect']
                                     
    # plot for case "no division selected"
    if stacked == 'No':
        fig = go.Figure(
            data=[go.Bar(x=counter['Total'], y=counter[selected_variable],
                         orientation='h',                                                                          # orientation of bars should be horizontal
                         text=[str(perc)+'%' for perc in np.round(counter['Total']/sum(counter['Total'])*100,2)], # text on bars: pecentage share of this class regarding whole number of defects
                         textposition='auto', marker={'color': counter['Total'] ,'colorscale':"Bluered"}          # define colors of bars
            )] ,
            layout={'yaxis': {'type': 'category'}}
        )
    # plot for division for pseudo errors: stacked barchart
    else:
        fig = go.Figure(
            data=[go.Bar(name = 'No pseudo defect', x=counter['No Pseudo Defect'], y=counter[selected_variable],
                         orientation='h',                                                                               # orientation of bars should be horizontal
                         text=[str(perc)+'%' for perc in np.round(counter['No Pseudo Defect']/counter['Total']*100,2)], # text: pecentage share of 'No Pseudo Defect' in this class
                         textposition='auto'
                        ),
                  go.Bar(name = 'Pseudo defect',x=counter['Pseudo Defect'], y=counter[selected_variable],
                         orientation='h',                                                                            # orientation of bars should be horizontal
                         text=[str(perc)+'%' for perc in np.round(counter['Pseudo Defect']/counter['Total']*100,2)], # text: pecentage share of 'Pseudo Defect' in this class
                         textposition='auto'
                        )
                 ],
            layout={'yaxis': {'type': 'category'}}
        )
        
        fig.update_layout(barmode='stack') #stacked barchart
    
    # layout of frequency chart
    fig.update_layout(
            autosize=False,
            paper_bgcolor='rgba(0,0,0,0)', # backround color of outer part
            plot_bgcolor='gainsboro',      # backround color of inner part
            yaxis_title=selected_variable, # y-axis title
            xaxis_title='Frequency',       # x-axis title
            font=dict(size=16),            # fontsize of all letters in plot
            height=600)                    # height of graphic (should be the same as in boxplot)
    
    
    #############################
    # boxplot for rework duration
    #############################
    
    #define data for boxplot (only needed columns)
    mydata = data_plant[[selected_variable, 'Rework Duration', 'Pseudo Defect']]
    #sort the classes in the selected variable the same way, as it is shown in the frequency plot
    mydata[selected_variable]=pd.Categorical(mydata[selected_variable],myorder)
    mydata = mydata.sort_values(selected_variable)
    
    #plot if we have no division depending on the pseudo defects
    if stacked == 'No':
        boxplot= px.box(mydata, y=selected_variable, x="Rework Duration", orientation='h')
    #plot if we have a division depending on the pseudo defects
    else:
        boxplot= px.box(mydata, y=selected_variable, x="Rework Duration", orientation='h', color=stacked, color_discrete_sequence=['red', 'blue'])
    
    #boxplot layout
    boxplot.update_layout(autosize=False,paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='gainsboro', xaxis_title = 'Time [Min]', font=dict(size=16), height=600)
        
        
    ############################
    # scatterplot for weekly analysis
    ############################
    
    #plot if we have no division depending on the pseudo defects
    if stacked == 'No':
        #prepare dataset by grouping by week
        counter_scatter = data_plant[['Week', 'Total']].groupby('Week').sum()
        scatter = go.Figure(data=go.Scatter(x=counter_scatter.index, y=counter_scatter['Total']))
    #plot if we have a division depending on the pseudo defects
    else: 
        #prepare dataset by grouping by week
        counter_scatter = data_plant[['Week', 'Pseudo Defect', 'Total']].groupby('Week').sum().reset_index()
        #line for pseudo defects
        scatter = go.Figure(data=go.Scatter(x=counter_scatter['Week'], y=counter_scatter['Total']-counter_scatter['Pseudo Defect'], name= 'No pseudo defect'))
        #line for non-pseudo defects
        scatter.add_trace(go.Scatter(x=counter_scatter['Week'], y=counter_scatter['Pseudo Defect'], name = 'Pseudo defect'))
        
    #scatterplot layout
    scatter.update_layout(autosize=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='gainsboro', xaxis_title = 'Calendar week', font=dict(size=16), yaxis_title='Frequency of defects',xaxis = dict(tickmode = 'linear',dtick = 1))
    
    #returning output (return the three updated figures)
    return fig, boxplot, scatter


#############################
# Run application
#############################
if __name__ == '__main__':
    app.run_server()