import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import visdcc
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def get_example_app(server,path):
    dash_example = dash.Dash(
        __name__,
        server=server,
        external_stylesheets=external_stylesheets,
        url_base_pathname =path
    )

    dash_example.layout = html.Div(
        className="dash-div",
        children=[
            dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )

    ])


    return dash_example
