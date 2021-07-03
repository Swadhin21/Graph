
import plotly
import plotly.graph_objs as go
from flask import Flask, render_template,request,redirect 
import json
import os

app = Flask(__name__)


def create_plot(destination):
    ylist = []
    xlist = []
    with open(destination,'r') as f:
        for line in f:
            ylist.append(line)

    y=range(1,len(ylist)+1)
    for i in y:
        xlist.append(i)  

    data = [
        go.Line(
            x=xlist, 
            y=ylist
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON



APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload",methods = ["POST","GET"])
def upload():
    target = os.path.join(APP_ROOT,'analysis/')
    #print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        #print(file)
        filename = file.filename
        destination = "/".join([target,filename])
        print(destination)
        file.save(destination)
        bar = create_plot(destination)
    return render_template('graph.html', plot=bar) 


if __name__ == '__main__':
    app.run(debug=True)

    