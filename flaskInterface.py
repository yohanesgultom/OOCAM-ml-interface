from flask import Flask, render_template, request
import os, modelTrainScript

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("HTML_Interface.html")

@app.route("/train", methods = ["POST", "GET"])
def train():
    if request.method == "POST":
        folder_path = request.form['foldername']
        split = float(request.form['split'])

        history = modelTrainScript(folder_path, split)

        return history
        

if __name__ == '__main__':
    app.run(debug = True)
