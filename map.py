# modules
import dash_core_components as dcc
from dash.dependencies import Input, Output

# custom modules
from data_preprocessing_temperature import get_map_data_temp
from choropleth_map_figure import choropleth_map_figure


def create_map(maps_current_state, map_id, other_map_id, geojson_grid_temp, legend_flag, period, app):
    '''
    In this function a callback is defined, updating and creating the two maps

    Returns: dcc.Graph
    '''

    # Click on map callback:
    # https://towardsdatascience.com/highlighting-click-data-on-plotly-choropleth-map-377e721c5893

    # this is the map graph figure
    graph = dcc.Graph(id=map_id)

    # This callback is called at the start of the app AND
    # when the map is zoomed or panned OR user input has changed
    # At the start it creates the other map
    # When it is panned or zoomed it changes the other map
    # When the user input has changed, it changes both maps
    @app.callback(
        Output(map_id, 'figure'),
        Input(other_map_id, 'relayoutData'),
        Input('Variable', 'value'),
        Input('Years', 'value'),
        Input('temperature threshold', 'value'),
        Input('temperature threshold 2', 'value'),
        Input('rangeslider_temp', 'value'),
        Input('tabs', "active_tab"))
    def update_maps(relayoutData, variable, years, temp_threshold, temp_threshold_2, slider, tab):

        # don't run this when the app is initializing
        if relayoutData != None and len(relayoutData) != 1:
            # check if zoom or pan has changed
            if maps_current_state['zoom'] != relayoutData['mapbox.zoom'] or maps_current_state['center'] != relayoutData['mapbox.center']:
                maps_current_state['zoom'] = relayoutData['mapbox.zoom']
                maps_current_state['center'] = relayoutData['mapbox.center']

        # check which tab is currently selected;
        if tab == 'temperature':

            # check if the input has changed, if so change both maps
            if maps_current_state['user_input'] != [variable, years, temp_threshold, temp_threshold_2, slider]:

                tempdays_hist, tempdays_proj = get_map_data_temp(
                    variable, years, temp_threshold, temp_threshold_2, slider)

                # update maps current state
                maps_current_state['Historic'] = tempdays_hist
                maps_current_state['Projection'] = tempdays_proj
                maps_current_state['user_input'] = [
                    variable, years, temp_threshold, temp_threshold_2, slider]

        # create a gridded data layer on top of the map
        return choropleth_map_figure(maps_current_state, period, legend_flag, geojson_grid_temp, variable)

    return graph
