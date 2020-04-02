import flask
import dash
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

if __name__ == '__main__':
    app.run(debug=True, port=8050)
