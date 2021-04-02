from flask import jsonify, render_template, request
from server import app

@app.route("/")
def index():
    return "Hello"

@app.route('/getData')
def getData():
    pass

@app.route("/graphData")
def getGraphData():
   pass