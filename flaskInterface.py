from flask import Flask, render_template, request
import os, modelTrain, modelPredict, directoryUtils, re
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("HTML_Interface.html")

@app.route("/train", methods = ["POST", "GET"])
def train():
    if request.method == "POST":
        if os.path.exists('temp'):
            directoryUtils.rmtree("temp")
        os.mkdir('temp')
        for f in request.files.getlist('foldername'):
            fil = secure_filename(f.filename)
            f.save(os.path.join('temp', fil))
        split = float(request.form['split'])
        epochs = int(request.form['epoch'])

        print("Beginning handover to training script.")
        modelTrain.trainModel(split, epochs)
        
        modelList = []
        query = re.compile(r'^(\w+)_(\d.\d{3})_(\d.\d{3}).h5$')

        for file in os.listdir("output"):
            matches = query.findall(file)

            model = {}

            if len(matches) > 0:
                model['specialization'] = "Maximum Accuracy" if matches[0][0] == "max_acc" else "Minimum Loss"
                model['val_loss'] = '{:.3f}'.format(float(matches[0][1]))
                model['val_acc'] = '{:.1f}%'.format(float(matches[0][2]) * 100)
                model['filename'] = file

                modelList.append(model)

        directoryUtils.rmtree("temp")

        return render_template("trainResults.html", models = modelList)
        
@app.route("/predict", methods = ["POST", "GET"])
def predict():
    if request.method == "POST":
        if os.path.exists('temp'):
            directoryUtils.rmtree("temp")
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

        print("Beginning handover to prediction script.")
        modelPredict.predict()

        directoryUtils.rmtree("temp")

        return f"Predictions were made and stored in the 'predictions' folder."

if __name__ == '__main__':
    app.run(debug = True)
