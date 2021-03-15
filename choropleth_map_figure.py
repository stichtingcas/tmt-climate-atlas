import plotly.express as px
import numpy as np
import math


def choropleth_map_figure(maps_current_state, period, legend_flag, geojson_grid, variable):
    '''
    Function to create a choropleth map figure

    Returns: choropleth mapbox Figure
    '''

    opacity = 0.7
    # the color scheme depends on the variable
    # more hot days is more red
    # the average temperature between has a neutral grey color scheme
    colors = px.colors.sequential.RdBu_r
    if variable == 'Minimum temperature below':
        colors = px.colors.sequential.RdBu
    elif variable == 'Average temperature between':
        colors = px.colors.sequential.Greys[1:]
        opacity = 0.8

    # rgba colors are necessary to make the legend the same opacity as the markers
    # here the colors are taken from a plotly sequential color scheme
    rgba_colors = ['rgba(' + x.split('rgb(')[1][:-1] + ',' +
                   str(opacity) + ')' for x in colors]

    fig = px.choropleth_mapbox(
        data_frame=maps_current_state[period],
        geojson=geojson_grid,
        color=maps_current_state[period].columns[-1],
        locations="lat_lon", featureidkey="properties.lat_lon",
        center=maps_current_state['center'],
        mapbox_style="open-street-map", zoom=maps_current_state['zoom'],
        opacity=opacity,
        title=period,
        color_continuous_scale=rgba_colors,
        hover_data={"lat_lon": False}
    )

    def append_days(x):
        if x == 'No data':
            return x
        else:
            return str(int(x)) + ' days'

    # these variables are just used to show the right data in the hover tooltip,
    # set in the update_traces function down below
    historic = maps_current_state['Historic'][
        maps_current_state[period].columns[-1]].round(0).fillna('No data').apply(append_days)
    projection = maps_current_state['Projection'][
        maps_current_state[period].columns[-1]].round(0).fillna('No data').apply(append_days)

    fig.update_traces(marker_line_width=0,
                      customdata=np.stack((
                          historic,
                          projection), axis=-1),
                      hovertemplate=(
                          '<br><b>Historical</b>: %{customdata[0]}<br>' +
                          '<br><b>Projection</b>: %{customdata[1]}<br>'
                      ))

    fig.update_layout(
        hoverlabel=dict(bgcolor="white"),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=legend_flag,
    )

    return fig
