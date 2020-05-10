from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import CSRFProtect
import os, modelTrain, modelPredict, directoryUtils, downloadUtils, re, json, subprocess
from werkzeug.utils import secure_filename

from forms import TrainForm, TestForm

app = Flask(__name__)
csrf = CSRFProtect(app)

LOG_FILE_TRAIN = 'trainModel.out'
LOG_FILE_TEST = 'testModel.out'

with open('secret_key.dat', 'r') as f:
    k = json.load(f)
    app.secret_key = k['SECRET_KEY']

def allowed_file(filename, exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in exts

@app.route("/", methods = ['GET', 'POST'])
def index():
    trainForm = TrainForm()
    testForm = TestForm()

    if trainForm.submitTrain.data and trainForm.validate_on_submit():
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
            if os.path.isfile(LOG_FILE_TRAIN):
                os.remove(LOG_FILE_TRAIN)
            w = open(LOG_FILE_TRAIN, 'w+')
            cmd = ['python', '-u', 'modelTrain.py', str(split), str(epochs), str(trainForm.width.data), str(trainForm.height.data)]
            subprocess.Popen(cmd, stdout=w, stderr=subprocess.STDOUT)
            w.close()
            return redirect(url_for('trainResults'))            

    if testForm.submitTest.data and testForm.validate_on_submit():
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

            # process based on source
            print('Beginning handover to prediction script.')
            images_dir_path = None
            if testForm.source.data == 'images':
                for f in testForm.images.data:
                    if allowed_file(secure_filename(f.filename), ['jpeg', 'jpg', 'png']):
                        f.save(os.path.join('temp', 'images', secure_filename(f.filename)))
                images_dir_path = 'temp'
            elif testForm.source.data == 'path':
                images_dir_path = testForm.path.data
            if os.path.isfile(LOG_FILE_TEST):
                os.remove(LOG_FILE_TEST)
            w = open(LOG_FILE_TEST, 'w+')
            cmd = ['python', '-u', 'modelPredict.py', images_dir_path]
            subprocess.Popen(cmd, stdout=w, stderr=subprocess.STDOUT)
            w.close()
            return redirect(url_for('testResults')) 

    return render_template("HTML_Interface.html", trainForm = trainForm, testForm = testForm)

@app.route('/download/<folder>')
def download(folder):
    return downloadUtils.zipAndDownload(folder)

@app.route('/trainResults')
def trainResults():
    return render_template("trainResults.html")

@app.route('/testResults')
def testResults():
    return render_template("testResults.html")

@app.route('/results/<process>')
def result_data(process):
    res = {}
    if request.method == "GET":
        outFile = None
        if process == 'train':
            outFile = LOG_FILE_TRAIN
        elif process == 'test':
            outFile = LOG_FILE_TEST
        else:
            return f'Unknown process type: {process}', status.HTTP_400_BAD_REQUEST        
        with open(outFile, 'r') as f:
            res['logs'] = f.readlines()
    
        if os.path.isfile(outFile):
            lastLine = res['logs'][-1] if len(res['logs']) > 0 else None
            # train results
            if process == 'train':
                if lastLine and lastLine.strip().lower().startswith('training complete'):
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
                    res['model_list'] = modelList
                    if os.path.isdir('temp'):
                        directoryUtils.rmtree("temp")
            # test results
            elif process == 'test':
                if lastLine and lastLine.strip().lower().startswith('image output complete'):
                    if os.path.isdir('temp'):
                        directoryUtils.rmtree("temp")

    return jsonify(res)

if __name__ == '__main__':
    import webbrowser, threading
    port = 5000
    threading.Timer(2, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    debug = os.getenv('FLASK_DEBUG') == '1'
    app.run(port = port, debug = debug)