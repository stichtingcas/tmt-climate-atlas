# custom modules
from data_preprocessing_temperature import get_chart_data_temp
import dash_core_components as dcc
import plotly.express as px
import numpy as np
import xarray as xr
import pandas as pd
import datetime as dt
import json
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.figure_factory as ff


def create_chart(app, figureid, mapid):
    '''
    In this function a chart is created that is shown below the maps

    Returns: a dcc.Graph figure
    '''
    figure = dcc.Graph(id=figureid, style={
                       'display': 'inline-block', 'width': '100%', 'height':  '50vh'})

    @app.callback(
        Output(figureid, 'figure'),
        Input(mapid, "clickData"),
        Input('Variable', 'value'),
        Input('tabs', "active_tab"))
    def display_selected_data(clickData, variable, tab):
        if clickData is None:
            fig = px.line(title="Click on the left map to select a location")
        elif tab == 'temperature':
            lat, lon = find_location(clickData)

            ds = get_chart_data_temp(
                variable, lat, lon)

            fig = temperature_chart(ds, variable)

        return fig

    return figure


def find_location(clickData):
    '''
    Retrieve the coordinates from the clicked gridcell

    Returns: lat, lon
    '''
    location = clickData['points'][0]['location']
    location = location.split("_")
    lat = float(location[0])
    lon = float(location[1])
    return lat, lon


def temperature_chart(ds, variable):
    '''
    Create a chart for the average monthly temperature for the four models
    era5, end century, mid century and historical

    Returns: Figure
    '''
    ds = ds[::-1]
    start = dt.datetime(2012, 1, 1)
    end = dt.datetime(2012, 12, 31)
    index = pd.date_range(start, end)
    ds['date'] = pd.to_datetime(ds.index, format='%j')
    ds['month'] = pd.to_datetime(ds['date']).dt.month
    monthly_average = ds.groupby(['month'], as_index=False).mean()
    monthly_average = monthly_average.set_index(['month']).round(1)

    traces = {}
    colors = ['maroon', 'red', 'orange', 'yellow']
    for col, color in zip(monthly_average.columns, colors):
        traces['trace_' + col] = go.Scatter(x=monthly_average.index, name=col, y=monthly_average[col], line=dict(
            color=color),  hoverlabel=dict(namelength=-1))
    data = list(traces.values())
    fig = go.Figure(data)

    fig.update_xaxes(
        tickmode='array',
        tickvals=[1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12],
        ticktext=['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    )

    fig.update_yaxes(title_text=str(variable) + ' (\u00b0C)')

    fig.update_layout(legend_title="", title="Seasonality of " + str(variable).lower() +
                      " for selected location", hovermode="x unified", hoverlabel=dict(bgcolor="white"))

    return fig
