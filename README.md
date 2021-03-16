# Tailor Made Training: Python application

#### What is this project about?
This project implements the TMT climate atlas. This climate atlas is a simple dashboard providing information about temperature in Kenya, in the past and in the future, and is meant to be a starting point to create a more complex climate atlas.

The project is developed with the Python visualization library [Dash](https://plotly.com/dash/) by Plotly.

#### Why is this useful?
This starter climate atlas is part of the course materials of the 'Tailor-Made Training - Build a climate atlas from open data' MOOC. Students can login into Moodle here: [https://courses.deltacapproject.net/](https://courses.deltacapproject.net/)

#### How can users get started with this project?
Download the code in this repository and run the application locally with command: `python app.py`. More information about this is given on the course page on Moodle.

#### Who maintains and contributes to the project?
This project is created and maintained by [Stichting CAS](https://www.climateadaptationservices.com).

Main contributors: Sophie van der Horst, Merlijn van Selm and Daniël Staal.

#### Where can users get help with this project?
daniel@climateadaptationservices.com
sophie@climateadaptationservices.com
merlijn@climateadaptationservices.com

#### What is the role of the different files?
*app.py*

This is the main file of the application. This file contains the following actions: 
1. The .geojson file for the map is imported.
2. The app is initialized. 
3. The settings from settings.py are imported. 
4. maps_current_state tracks the state of the two maps
5. The app elements (two maps + figure) are created.
6. The app elements are included in the layout. 


*app_layout.py*

This file organizes the layout of the application. The input elements and output elements are organized and the loading buttons are included. 


*chloropleth_map_figure.py*

In this file, the maps are made. The left map shows the historic values and the right map the projection. 


*data_preprocessing_temperature.py*

This file contains multiple functions which are required to import and process the data for the application. The data for temperature can be found in the following folder: Data/temperature. The following functions are included:
1. app_data: imports the data for the map. 
2. load_data_figure_temp: imports the data for the figure. 
3. load_data_equilizevar: function to rename the variables to make the datasets uniform. 
4. get_map_data_temp: processes the imported data for the map with functions from temperature_data_functions.py


*figure.py*

This file uses the input of the application to create a figure as output. The following functions are included:
find_location: this function is used to define the location of the clicked point on the map. 
temperature_graph: this function creates the figure.


*map.py*
This file uses the input of the application to create a map as output. 


*settings.py*

Includes the settings that are used for the application.


*temperature_data_functions.py*

This file is used to make calculations on the data imported to the application. The main goal of the application is to display the number of days in which the variable is between a particular threshold. This file includes the following functions:
1. temp_days_hist: this function calculates the number of days for the historical period. between the range that is given through the input. 
2. temp_days_hist: this function calculates the number of days for the projected period. between the range that is given through the input. 
3. new_climate: this function regrids the data so that the historical data and projected data have the same resolution. In addition, the difference between the historical model results and future model results is calculated. This difference is then added to the historical era5 data. 
4. make_pandas: converts the data to the correct pandas dataframes. 


*user_input.py*

This file contains the input of the application. Thus, the dropdown menus, text input and slider. 


