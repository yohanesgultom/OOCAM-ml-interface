from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
import os, modelTrain, modelPredict, directoryUtils, downloadUtils, re, json
from werkzeug.utils import secure_filename

from forms import TrainForm, TestForm

app = Flask(__name__)
csrf = CSRFProtect(app)

with open('secret_key.dat', 'r') as f:
    k = json.load(f)
    app.secret_key = k['SECRET_KEY']

def allowed_file(filename, exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in exts

@app.route("/", methods = ['GET', 'POST'])
def index():
    trainForm = TrainForm()
    testForm = TestForm()

    if trainForm.submit.data and trainForm.validate_on_submit():
        if request.method == "POST":
            if os.path.exists('temp'):
                directoryUtils.rmtree("temp")
            os.mkdir('temp')
            for f in trainForm.images.data:
                # remove underscores to avoid ambiguity 
                # as secure_filename() replaces os.path.sep with underscore
                safe_name = f.filename.replace('_', '')
                fil = secure_filename(safe_name)
                if allowed_file(fil, ['jpg', 'jpeg', 'png']):                                            
                    f.save(os.path.join('temp', fil))
            split = float(trainForm.split.data)
            epochs = int(trainForm.epochs.data)

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

    if testForm.submit.data and testForm.validate_on_submit():
        if request.method == "POST":
            if os.path.exists('temp'):
                directoryUtils.rmtree("temp")
            os.mkdir('temp')
            os.mkdir(os.path.join("temp", "model"))
            os.mkdir(os.path.join("temp", "label"))
            os.mkdir(os.path.join("temp", "images"))

            model = testForm.model.data
            label = testForm.labels.data

            if allowed_file(secure_filename(model.filename), ['h5']):
                model.save(os.path.join("temp", "model", secure_filename(model.filename)))
            else:
                return 'Invalid model.'
            if allowed_file(secure_filename(label.filename), ['dat']):
                label.save(os.path.join("temp", "label", secure_filename(label.filename)))
            else:
                return 'Invalid labels.'

            for f in testForm.images.data:
                if allowed_file(secure_filename(f.filename), ['jpeg', 'jpg', 'png']):
                    f.save(os.path.join('temp', 'images', secure_filename(f.filename)))

            print("Beginning handover to prediction script.")
            modelPredict.predict()

            directoryUtils.rmtree("temp")

            return render_template("testResults.html")

    return render_template("HTML_Interface.html", trainForm = trainForm, testForm = testForm)

@app.route('/download/<folder>')
def download(folder):
    return downloadUtils.zipAndDownload(folder)

if __name__ == '__main__':
    import webbrowser, threading
    port = 5000
    threading.Timer(2, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    app.run(port = port, debug = False)
