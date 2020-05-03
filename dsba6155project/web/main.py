from flask import jsonify
from dashapps.example.example import get_app
from d3 import D3, D3BookData
from flask import Flask, render_template

app = Flask(__name__)


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
    import os

    app.run(debug=True, port=os.environ.get("PORT" , 8000))
