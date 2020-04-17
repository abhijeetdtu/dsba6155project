import flask
from flask import jsonify
import dash
import requests
import json
from d3 import D3 , D3BookData
import dash_html_components as html
from dashapps.example.example import get_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, render_template

app = flask.Flask(__name__)


get_app(app,'/app1/').index()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page/<int:number>/')
def page(number):
    return render_template(f'page{number}.html' , pagenumber = number)
    #return "app1"


@app.route("/d3data")
def d3data():
    return jsonify(D3().getData())


@app.route("/d3bookdata/<string:filter>")
def d3bookdata(filter):
    return jsonify(D3BookData().getData(filter))


@app.route('/d3/<string:dashId>')
def d3(dashId):
    dashMap = {
        "timeline": "d3app.network()",
        "bubble" : "d3bubbleForce.draw()"
    }
    return render_template(f'd3.html' , instantiate=dashMap[dashId])
    #return "app1"

if __name__ == '__main__':
    app.run(debug=True, port=8050)
