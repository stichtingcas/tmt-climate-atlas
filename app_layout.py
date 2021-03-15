import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


def make_app_layout(app, map_left, map_right, figure, userInputElements, settings):

    # add title
    app_layout_input = [
        html.H1(settings['title'], style={'textAlign': 'center'})]

    # add user input
    app_layout_input.append(html.Br())
    for element in userInputElements:
        app_layout_input.append(element)

    app_layout_input.append(html.Br())

    # add maps wrapped in a loading animation
    loading_map_left = dcc.Loading(
        id="loading_map_left",
        children=html.Div(
            [html.P(children='Current climate', style={
                'text-align': 'center', 'padding-right': '88px', 'font-size': '18px', 'color': '#414649'}),
                map_left
             ]),
        type="circle",
        parent_style={'width': '52%', 'display': 'inline-block'},
    )
    loading_map_right = dcc.Loading(
        id="loading_map_right",
        children=html.Div(
            [html.P(children='Future climate', style={
                'text-align': 'center', 'font-size': '18px', 'color': '#414649'}),
                map_right
             ]),
        type="circle",
        parent_style={'width': '48%', 'display': 'inline-block'},
    )
    app_layout_input.append(loading_map_left)
    app_layout_input.append(loading_map_right)

    # add the chart
    app_layout_input.append(figure)

    # create the layout
    app.layout = html.Div(app_layout_input, style={
                          'marginLeft': 30, 'marginRight': 30})
