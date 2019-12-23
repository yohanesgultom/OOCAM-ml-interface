from flask import Flask, render_template, request
import os, modelTrainScript, modelPredict

app = Flask(__name__)

def processDirectory(datadir):
    newDatadir = ''

    for i in datadir:
        if i == '\\':
            newDatadir += '\\\\'
        else:
            newDatadir += i

    return newDatadir

@app.route("/")
def index():
    return render_template("HTML_Interface.html")

@app.route("/train", methods = ["POST", "GET"])
def train():
    if request.method == "POST":
        folder_path = processDirectory(request.form['foldername'])
        split = float(request.form['split'])
        epochs = int(request.form['epoch'])

        history = modelTrainScript.trainModel(folder_path, split, epochs)

        val_accs = list(map(float, history['val_accuracy']))
        max_val_acc = max(val_accs)
        return f"Maximum validation accuracy: {max_val_acc * 100:.3f}%. Your model and labels were saved in the 'output' folder."
        
@app.route("/predict", methods = ["POST", "GET"])
def predict():
    if request.method == "POST":
        modeldir = processDirectory(request.form['modeldir'])
        imagedir = processDirectory(request.form['imagedir'])
        labeldir = processDirectory(request.form['labeldir'])

        prediction = modelPredict.predict(modeldir, imagedir, labeldir)

        return f"Prediction: {prediction}"

if __name__ == '__main__':
    app.run(debug = True)
