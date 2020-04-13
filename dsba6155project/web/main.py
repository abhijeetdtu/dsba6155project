import flask
from flask import jsonify
import dash
import requests
import json
import dash_html_components as html
from dashapps.example.example import get_example_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, render_template

app = flask.Flask(__name__)


get_example_app(app,'/app1/').index()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page/<int:number>/')
def page(number):
    return render_template(f'page{number}.html' , pagenumber = number)
    #return "app1"


@app.route("/d3data")
def d3data():
    data = requests.get("http://www.thearda.com/timeline/json/tlRank1to2JsonFeed.js?_=1586741122479")
    js = data.text.replace("TLonJSONPLoad(" , "").replace(")" , "")
    js = json.loads(js)
    nodes = []
    links = []
    for i,j in enumerate(js):
        if 'startDate' in j:

            j["year"] = int(j["startDate"].split("-")[0])
            j["id"] = j["title"] + " - " + str(j["year"])
            totalLinks = 0
            for k,l in enumerate(js):
                if k > i and 'startDate' in l:
                    l["year"] = int(l["startDate"].split("-")[0])
                    l["id"] = l["title"] + " - " + str(l["year"])

                    dist = abs(int(l["startDate"].split("-")[0]) - int(j["startDate"].split("-")[0]))
                    if dist < 10:
                        totalLinks += 1
                        links.append({"source" : j["id"] , "target" : l["id"] , "value" : dist})
            j["totalLinks"] = totalLinks
            nodes.append(j)
    return jsonify({"nodes":nodes , "links":links})



@app.route('/d3/')
def d3():
    return render_template(f'd3.html')
    #return "app1"
if __name__ == '__main__':
    app.run(debug=True, port=8050)
