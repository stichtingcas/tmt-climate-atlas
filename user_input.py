import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output


def user_input(map_current_state, app):
    '''
    In this function all user input fields are created. dbc Bootstrap components
    are used here to make styling easier.

    Returns: a list of dbc.Tabs containing the respective inputs for
    temperature
    '''

    # user input for temperature tab
    temperature = html.Div([
        dbc.Row([
            dbc.Col(
                create_dropdown('Variable',
                                ['Maximum temperature above', 'Minimum temperature below',
                                 'Average temperature between'],
                                'Number of days per year with:',
                                'Maximum temperature above'),
                width={"size": True}),

            dbc.Col(create_input("temperature threshold",
                                 "Degrees °C", 25),
                    width={"size": True},),
            dbc.Col(create_input("temperature threshold 2",
                                 "Degrees °C", 35),
                    width={"size": True},),
            dbc.Col(
                create_dropdown('Years',
                                ['2011-2040', '2041-2070', '2071-2100'],
                                'Future time period',
                                '2041-2070'),
                width={"size": True}),
        ], align="center"
        ),
        dbc.Row(
            dbc.Label(['Select months:'], style={
                      'color': 'rgb(108, 117, 125)', 'padding-left': '2%'})
        ),
        dbc.Row([
            dbc.Col(create_slider('rangeslider_temp'))
        ])
    ])


    tabs = dbc.Tabs([
        dbc.Tab(temperature, label="Temperature", tab_id='temperature'),

    ], active_tab="temperature", id='tabs')

    # callback to show a second degree input for the 'average temperature between' option
    @app.callback(
        Output('temperature threshold 2_visibility', 'style'),
        Input('Variable', 'value'))
    def update_thresholds(variable):
        if variable == 'Average temperature between':
            return {'visibility': 'visible'}
        else:
            return {'visibility': 'hidden'}

    return [tabs]


def create_dropdown(dropdownid, options, placeholder, default):
    dropdown = html.Div([
        html.P(placeholder,
               style={'marginBottom': 0, 'marginTop': 10, 'font-style': 'italic'}),
        dcc.Dropdown(
            id=dropdownid,
            options=[{'label': option, 'value': option} for option in options],
            multi=False,
            style={'marginTop': '0em', 'marginBottom': '1em'},
            placeholder=placeholder,
            value=default)
    ])

    return dropdown


def create_input(inputid,  placeholder, value):
    inputmenu = html.Div([
        html.P(placeholder,
               style={'marginBottom': 0, 'marginTop': 10, 'font-style': 'italic'}),
        dbc.Input(
            id=inputid,
            type="number",
            style={'marginTop': '0em', 'marginBottom': '1em'},
            placeholder=placeholder,
            value=value,
            disabled=False)
    ], id=inputid + '_visibility')

    return inputmenu


def create_slider(rangeid):
    rangeslider = dcc.RangeSlider(
        id=rangeid,
        min=1,
        max=12,
        step=1,
        marks={1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
               7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'},
        value=[1, 12]
    )
    return rangeslider
