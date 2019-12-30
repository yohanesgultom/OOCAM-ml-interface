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
        os.mkdir('temp')
        os.mkdir(os.path.join("temp", "model"))
        os.mkdir(os.path.join("temp", "label"))
        os.mkdir(os.path.join("temp", "images"))

        model = request.files['modeldir']
        label = request.files['labeldir']

        model.save(os.path.join("temp", "model", secure_filename(model.filename)))
        label.save(os.path.join("temp", "label", secure_filename(label.filename)))

        for f in request.files.getlist('imagedir'):
            f.save(os.path.join('temp', 'images', secure_filename(f.filename)))

        modelPredict.predict()

        shutil.rmtree('temp')

        return f"Predictions were made and stored in the 'predictions' folder."

if __name__ == '__main__':
    app.run(debug = True)
