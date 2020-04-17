import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os
import pandas as pd
import json
import visdcc
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

path = os.path.abspath(os.path.join(os.path.dirname(__file__) , ".." , ".." , "staticdata" , "test.json"))
data = json.load(open(path , "r"))
data = data[:100]

x = []
y= []

for d in data:
    x.append(d["x"])
    y.append(d["y"])

print(data)
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
                'data':[{"x":x , "y":y}],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )

    ])


    return dash_example
