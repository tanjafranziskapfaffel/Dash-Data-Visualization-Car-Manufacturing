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


# read in random data
data = pd.read_csv("C://Users//pfafft//msg//KiMotion - Dokumente//Showcases und Demos//Dash Dashboard Visualization//myRandomData.csv")

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

app.layout = html.Div(style={'backgroundColor': 'silver'}, children=[   
    
    #title
    html.H1(children='Interactive Dashboard for Data Visualization of Quality Data in Car Manufacturing Plants'),
      
    html.Br(),
    html.Br(),
    
    # Description of Dashboard
    html.Div([
        html.Div([
            html.Div('In production lines mistakes are made by humans and machines that lead to defects on the produced cars. Information about the defects and the reparation processes are saved in datasests, which are analyzed by car manufacturers.', style={'fontSize': 20}),
            html.Br()
        ], className="six columns" ),
        html.Div([
            html.Br()
        ], className="six columns" )
    ], className="row"),
    
    
    # Selection fields of features that influence the plot
    html.Div([
        
        html.Div([
            html.Br()
        ], className="one columns"), 
        
        html.Div(style={'fontSize': 20}, children=[
            
            #checkboxes for selection of plants
            html.H5('Select plant'),
            dcc.Checklist(
                id='plant',
                options=[
                    {'label': 'Munich', 'value': 'Munich'},
                    {'label': 'Sindelfingen', 'value': 'Sindelfingen'},
                    {'label': 'Ingolstadt', 'value': 'Ingolstadt'},
                ],
                value=['Munich']
            ),
            
            #selection field to choose the feature you want to examine
            html.H5('Select feature to examine'),
            dcc.Dropdown(
                id='feature',
                options=[
                    {'label': 'Rework activity', 'value': 'Rework Activity'},
                    {'label': 'Rework station', 'value': 'Rework Station'},
                    {'label': 'Defect location', 'value':'Defect Location'}, 
                    {'label': 'Defect type', 'value': 'Defect Type'}, 
                ],
                value='Rework Activity'
            ),
            
            #selection field stacked barplots 
            html.H5('Select if plot should be partitioned by pseudo defects'),
            dcc.Dropdown(
                id='stacks',
                options=[
                    {'label': 'No partition', 'value':'No'},
                    {'label': 'Partition by pseudo defect', 'value':'Pseudo Defect'},
                ],
                placeholder="Wählen Sie ",
                value='No'
            ),
            
            #Slider for time frame 
            html.H5('Select calendar weeks'),
            dcc.RangeSlider(
                id='week',
                min=1,
                max=15,
                step=1,
                marks=list(range(0,16)),
                value=[1, 15]
            )
            
        ], className="four columns"),
        
        
        html.Div([
            html.Br()
        ], className="one columns"), 
        
        
        #Scatterplot about weekly defect rate
        html.Div([
            
            html.H3(children='Frequency of defects per calender week'),
            
            dcc.Graph(id='scatter', figure = scatter)
            
        ], className="six columns"),
        
        
        
    ], className="row"),
    
    
    #plots
    html.Div(style={'padding': 60}, children=[
               
        #Frequency plot
        html.Div([
            
            html.H3(children='Frequency of occurence in dataset'),
            
            dcc.Graph(id = 'barplot', figure = fig)
                
        ], className="six columns"),
    
        
        #Boxplot showning distribution of rework duration
        html.Div([
            
            html.H3(children='Distribution of rework duration'),
            
            dcc.Graph(id = 'boxplot', figure = boxplot)
        
        ], className="six columns"),
        
        
    ], className="row"),
    

    #KiMotion Logo
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
# define input and output for updating function
# Output: 2 plots (frequency and boxplot)
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
# define updating function which is performed when updating a selection box
# the input is the input of the selection boxes
#############################

def update_graph(plant, selected_variable, stacked, week):
    
    # define the data for further plotting based on input of selection box plant and of slider week
    data_plant = data[np.logical_and(data['Plant'].isin(plant),data['Week'].isin(range(week[0], week[1]+1)))]
    
    # define order of classes on y-axis (=classes of selected feature in selection box 'features')
    # Goal: have a consistent order for each variable in the two plots
    myorder = data_plant[selected_variable].value_counts(ascending=True).index
    # order data such that rework activities that happen more often are shown on top of data set using prepared order
    data_plant[selected_variable]=pd.Categorical(data_plant[selected_variable],myorder)
    data_plant.sort_values(selected_variable)
    
    
    ############################
    # barplot showing frequency of occurence in dataset
    ############################
    
    # compute frequencies for frequency plot by groupin data regarding the selected feature
    counter = data_plant[[selected_variable, 'Pseudo Defect', 'Total']].groupby(selected_variable).sum().reset_index()
    # add a new column to count the entries, which are NOT pseudo errors
    counter['No Pseudo Defect'] = counter['Total'] - counter['Pseudo Defect']
                                     
    # plot for case "no division selected"
    if stacked == 'No':
        fig = go.Figure(
            data=[go.Bar(x=counter['Total'], y=counter[selected_variable],
                         orientation='h',
                         text=[str(perc)+'%' for perc in np.round(counter['Total']/sum(counter['Total'])*100,2)], #text: pecentage share of this class
                         textposition='auto', marker={'color': counter['Total'] ,'colorscale':"Bluered"}
            )] ,
            layout={'yaxis': {'type': 'category'}}
        )
    # plot for division for pseudo errors: stacked barchart
    else:
        fig = go.Figure(
            data=[go.Bar(name = 'No pseudo defect', x=counter['No Pseudo Defect'], y=counter[selected_variable],
                         orientation='h',
                         text=[str(perc)+'%' for perc in np.round(counter['No Pseudo Defect']/counter['Total']*100,2)],#text: pecentage share of this class and divition
                         textposition='auto'
                        ),
                  go.Bar(name = 'Pseudo defect',x=counter['Pseudo Defect'], y=counter[selected_variable],
                         orientation='h',
                         text=[str(perc)+'%' for perc in np.round(counter['Pseudo Defect']/counter['Total']*100,2)],#text: pecentage share of this class and divition
                         textposition='auto'
                        )
                 ],
            layout={'yaxis': {'type': 'category'}}
        )
        
        fig.update_layout(barmode='stack')
    
    # layout of frequency chart
    fig.update_layout(autosize=False,paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='gainsboro', yaxis_title=selected_variable, xaxis_title='Frequency', font=dict(size=16), height=600)
    
    
    #############################
    # boxplot for rework duration
    #############################
    
    #plot if we have no division depending on the pseudo defects
    if stacked == 'No':
        boxplot= px.box(data_plant, y=selected_variable, x="Rework Duration", orientation='h')
    #plot if we have a division depending on the pseudo defects
    else:
        boxplot= px.box(data_plant, y=selected_variable, x="Rework Duration", orientation='h', color=stacked, color_discrete_sequence=['red', 'blue'])
    
    #boxplot layout
    boxplot.update_layout(autosize=False,paper_bgcolor='rgba(0,0,0,0)', yaxis = {'type': 'category'}, plot_bgcolor='gainsboro', xaxis_title = 'Time [Min]', font=dict(size=16), height=600)
        
        
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
    
    #returning output
    return fig,boxplot, scatter

if __name__ == '__main__':
    app.run_server()