from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/input", methods=['POST'])
def changetext():
    folder = request.form['foldername']
    return render_template("HTML_Interface.html", name=folder)

@app.route("/")
def index():
    return render_template("HTML_Interface.html")

@app.route("/train", methods = ["POST", "GET"])
def train():
    if request.method == "POST":
        folder_path = request.form['folder_path']
        

if __name__ == '__main__':
    app.run(debug = True)
