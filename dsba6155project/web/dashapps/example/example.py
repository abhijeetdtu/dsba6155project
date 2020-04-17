import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os
import pandas as pd
import json
import pathlib
import visdcc
import plotly.express as px

projectId = "dsba6155p"
datasetTable = "nlpdataset.document_entities"
__file__ = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\web\\dashapps\\example\\example.py"
path = os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute() , "staticdata")
dfp = os.path.join(path, "outputs_document_entities_export.csv")

lbp = os.path.join(path, "label_descriptions.csv")

#df = pd.read_gbq(query=f"SELECT * from {projectId}.{datasetTable}",project_id=projectId)
df = pd.read_csv(dfp)
ldesc = pd.read_csv(lbp)
ldesc.index = ldesc["label"]

ldesc = ldesc.drop(["label"] , axis=1)
df = pd.merge(df , ldesc , on="label")

def getBubbleData(df, labelFilter,filterValue=50):
    #__file__ = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\web\\d3.py"
    ndf = df[df["label"] == labelFilter]
    ndf = ndf[ndf["count"] > filterValue]
    ndf["category"] = ndf["file"].apply(lambda x: x.split("/")[-1].split("_")[0])
    #return ndf[[ "text" , "count" , "category"]]
    return ndf

def get_app(server,path):
    dash_example = dash.Dash(
        __name__,
        server=server,
        url_base_pathname =path
    )

    label_map = json.loads(ldesc.to_json(orient="index"))

    dash_example.layout = html.Div(
        className="dash-div",
        children=[
            dcc.Dropdown(
                id='label-dropdown',
                options=[{'label': label_map[i]["label_description"], 'value':i } for i in df['label'].unique()],
                value=df['label'].unique()[0]
            ),
            dcc.Slider(
                id='filter-slider',
                min=0,
                max=20,
                step=1,
                value=10
            ),
            dcc.Graph(id="bubble-chart")
            ]
        )


    @dash_example.callback(
        Output('bubble-chart', 'figure'),
        [Input('label-dropdown', 'value'),Input('filter-slider', 'value')])
    def update_figure(label,value):
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
        ndf = getBubbleData(df,label)
        #print(ndf.head())
        return ndf["count"].min()

    @dash_example.callback(
        Output('filter-slider', 'min'),
        [Input('label-dropdown', 'value')])
    def update_slider_min(label):
        ndf = getBubbleData(df,label)
        #print(ndf.head())
        return ndf["count"].min()

    @dash_example.callback(
        Output('filter-slider', 'max'),
        [Input('label-dropdown', 'value')])
    def update_slider_max(label):
        ndf = getBubbleData(df,label)
        #print(ndf.head())
        return ndf["count"].max()


    return dash_example
