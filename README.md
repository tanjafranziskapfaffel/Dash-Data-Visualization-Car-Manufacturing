# Dashboard for Data Visualization of Quality Data in Car Manufacturing Plants
In production lines mistakes are made by humans or machines that lead to defects on the cars running on the production lines. Information about the defects and the reparation processes in the plants are saved in datasets, which are analyzed by the car manufacturers. For example, managers are interested in the number of defects per week or in the rework duration per vehicle. The shorter the duration of the rework activity the better for the car manufacturers, as in production processes time is money.

The Python file **Showcase.py** generates a Dash dashboard which shows information about defects in car manufacturing plants. The data used for the dashboard was randomly generated (with technical knowledge about production processes). The data is stored in **myRandomData.csv**. There is also a Jupyter Notebook file **Showcase.ipynb** available that contains the same code as the Python file.

**Notes:** 
- Before running the code, you need to install the **dash python library** by running *pip install dash==1.7.0* in your command line
- It is necessary to store the folder **assets** in the same folder as the Python / Jupyter Notebook file as the code that generates the dashboard accesses on the folder (the .css format is saved there).
