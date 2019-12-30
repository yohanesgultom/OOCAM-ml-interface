from flask import Flask, render_template, request
import os, modelTrainScript, modelPredict, shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("HTML_Interface.html")

@app.route("/train", methods = ["POST", "GET"])
def train():
    if request.method == "POST":
        os.mkdir('temp')
        for f in request.files.getlist('foldername'):
            fil = secure_filename(f.filename)
            f.save(os.path.join('temp', fil))
        split = float(request.form['split'])
        epochs = int(request.form['epoch'])

        history = modelTrainScript.trainModel(split, epochs)

        val_accs = list(map(float, history['val_accuracy']))
        max_val_acc = max(val_accs)
        
        shutil.rmtree('temp')

        return f"Maximum validation accuracy: {max_val_acc * 100:.3f}%. Your model and labels were saved in the 'output' folder."
        
@app.route("/predict", methods = ["POST", "GET"])
def predict():
    if request.method == "POST":
        print(request.form)
        modeldir = request.form['modeldir']
        imagedir = request.form['imagedir']
        labeldir = request.form['labeldir']

        prediction = modelPredict.predict(modeldir, imagedir, labeldir)

        return f"Prediction: {prediction}"

if __name__ == '__main__':
    app.run(debug = True)
