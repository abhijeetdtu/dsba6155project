from dash import Dash
from dash_core_components import Slider, Dropdown, Graph
from dash_html_components import Div
from dash.dependencies import Input, Output

from json import loads

import plotly.express as px

from dashapps.example.data_loader import Model


def getBubbleData(df, labelFilter, filterValue=50):
    #__file__ = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\web\\d3.py"
    ndf = df[df["label"] == labelFilter]
    ndf = ndf[ndf["count"] > filterValue]

    #return ndf[[ "text" , "count" , "category"]]
    return ndf

def get_app(server,path):

    df = Model().df
    ldesc = Model().ldesc

    dash_example = Dash(
        __name__,
        server=server,
        url_base_pathname =path
    )

    label_map = loads(ldesc.to_json(orient="index"))

    dash_example.layout = Div(
        className="dash-div",
        children=[
            Dropdown(
                id='label-dropdown',
                options=[{'label': label_map[i]["label_description"], 'value':i } for i in df['label'].unique()],
                value=df['label'].unique()[0]
            ),
            Slider(
                id='filter-slider',
                min=0,
                max=20,
                step=1,
                value=10
            ),
            Graph(id="bubble-chart")
            ]
        )


    @dash_example.callback(
        Output('bubble-chart', 'figure'),
        [Input('label-dropdown', 'value'),Input('filter-slider', 'value')])
    def update_figure(label,value):
        df = Model().df
        ndf = getBubbleData(df,label,value)
        #print(ndf.head())
        bar = px.bar(ndf, y="text", x="count", color="category", orientation='h',barmode='group')
        bar.update_layout(autosize=False,
        width=960,
        height=550 ,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode = 'closest',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="white"
        ))
        #return fig
        return bar


    @dash_example.callback(
        Output('filter-slider', 'value'),
        [Input('label-dropdown', 'value')])
    def update_slider_min(label):
        df = Model().df
        ndf = getBubbleData(df,label)
        #print(ndf.head())
        return ndf["count"].min()

    @dash_example.callback(
        Output('filter-slider', 'min'),
        [Input('label-dropdown', 'value')])
    def update_slider_min(label):
        df = Model().df
        ndf = getBubbleData(df,label)
        #print(ndf.head())
        return ndf["count"].min()

    @dash_example.callback(
        Output('filter-slider', 'max'),
        [Input('label-dropdown', 'value')])
    def update_slider_max(label):
        df = Model().df
        ndf = getBubbleData(df,label)
        #print(ndf.head())
        return ndf["count"].max()


    return dash_example
