from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/changetext", methods=['POST'])
def changetext():
    user = request.form['Name']
    return render_template("HTML_Interface.html", name=user)

@app.route("/")
def index():
    return render_template("HTML_Interface.html")

if __name__ == '__main__':
    app.run(debug = True)
