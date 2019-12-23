from flask import Flask, render_template, request, os, modelTrainScript

app = Flask(__name__)

@app.route("/changetext", methods=['POST'])
def changetext():
    user = request.form['Name']
    return render_template("HTML_Interface.html", name=user)

@app.route("/")
def index():
    return render_template("HTML_Interface.html")

@app.route("/train", methods = ["POST", "GET"])
def train():
    if request.method == "POST":
        folder_path = request.form['folder_path']
        

if __name__ == '__main__':
    app.run(debug = True)
