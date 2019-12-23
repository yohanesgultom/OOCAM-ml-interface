from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/input", methods=['POST'])
def changetext():
    folder = request.form['foldername']
    return render_template("HTML_Interface.html", name=folder)

@app.route("/")
def index():
    return render_template("HTML_Interface.html")

if __name__ == '__main__':
    app.run(debug = True)
