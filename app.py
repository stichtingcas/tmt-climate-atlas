# modules
import dash
import geojson
import dash_bootstrap_components as dbc

# custom modules
from general_settings import get_settings
from user_input import user_input
from map import create_map
from chart import create_chart
from app_layout import make_app_layout

# Here a geojson grids is loaded for temperature data.
# This geojson file consists of a grid which
# will be displayed on top of a map. The geojson file is made
# specifically for the resoultion of the data.
# There is no data attached to these grids yet, this happens in
# choropleth_map_figure.py
with open("Data/temperature_grid.geojson") as f:
    geojson_grid_temp = geojson.load(f)

# initialize app
app = dash.Dash(__name__,
                # stylesheet
                external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# Import settings
settings = get_settings()

# this object will keep track of the state of the two maps
maps_current_state = {
    'Historic': None,
    'Projection': None,
    'zoom': settings['start_map_zoom'],
    'center': settings['start_map_center'],
    # user_input consists of: [variable, years, min_temp, max_temp]
    'user_input': ['', '', '', '']
}

# create app elements
map_left = create_map(maps_current_state, 'map_left',
                      'map_right', geojson_grid_temp, True, 'Historic', app)
map_right = create_map(maps_current_state, 'map_right',
                       'map_left', geojson_grid_temp, False, 'Projection', app)
user_input_elements = user_input(maps_current_state, app)
figure = create_chart(app, "Temp_graph", 'map_left')

# Make app layout
make_app_layout(app, map_left, map_right, figure,
                user_input_elements, settings)

# main function
if __name__ == '__main__':
    app.run_server(debug=settings['debug'])
