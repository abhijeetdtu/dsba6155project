from plotnine import *

import pathlib
import os

def _getDataPath():
    try:
        __file__
        p = os.path.join(pathlib.Path(__file__).parent.parent.absolute())
    except:
        p =  os.path.join(pathlib.Path(".").absolute() , "dsba6155project")

    return os.path.join(p, "data" , "outputs_document_entities_export.csv")

dfpath = _getDataPath()


import pandas as pd

df = pd.read_csv(dfpath)
df["category"] = df.iloc[:,0].apply(lambda x: x.split("/")[-1].split("_")[0])
df.head()



pltdf = df.groupby(["category" , "label"]).agg(counttot = ("count" , "sum")).reset_index()
pltdf  =(pltdf.groupby(["category"])
     .apply(lambda x:  (x["counttot"] - x["counttot"].mean()) / x["counttot"].std())
     .reset_index()
     .join(pltdf ,how="inner" , rsuffix="_r"))


from plotnine import *

#pltdf.apply(lambda x:  (x["counttot"] - x["counttot"].mean()) / x["counttot"].std())
pltdf.groupby("category").agg(counttotmean=("counttot" , "mean"))
(ggplot(pltdf , aes(x="label" , y="counttot" , fill="category")) +
geom_col(position="dodge") + theme(axis_text_x=element_text(angle=65)))



locdf = df[df["label"] == "GPE"]

locpltdf = (locdf.groupby(["category" , "text"])
     .agg(counttot = ("count" , "sum"))
     .reset_index()
     .groupby("category")
     .apply(lambda x : x.sort_values("counttot" , ascending=False).head(10)))

locpltdf = locpltdf[[ "text" , "counttot"]].reset_index()


(ggplot(locpltdf , aes(x="category" , y="counttot" ,fill="text")) +
geom_col(position = "fill",stat="identity") +
coord_flip() +
theme(axis_text_x = element_text(angle=65)))



from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import plotly.express as px

fig = px.choropleth(locpltdf, geojson=counties, locations='text', color='category',
                           #color_continuous_scale="Viridis",
                           #range_color=(0, 12),
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


import folium

from IPython.core.display import display, HTML
from IPython.display import IFrame



m = folium.Map(location=[45.5236, -122.6750])

from IPython.display import Image, HTML

import io


def displayFolium(m):
    fname = "tmp.html"
    with open( fname, "w") as f:
        f.write(m._repr_html_())
        f.close()
    display(IFrame(fname , width= "100%" , height="500"))


displayFolium(m)

m._repr_html_()


sio = io.StringIO(m._repr_html_())
m.render()
img = 'test_image.png'
m.save(img)
def path_to_image_html(path):
    return '<img src="'+ path + '"/>'

img_html = path_to_image_html(img)
display(IFRAME(img_html))


display(HTML(m))
