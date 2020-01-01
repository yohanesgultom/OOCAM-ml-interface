from tensorflow.keras.applications.xception import preprocess_input, Xception
from tensorflow.keras.models import load_model
import pickle, cv2, numpy as np, imageUploadUtils, shutil, os

def predict():
    if os.path.exists("predictions"):
        shutil.rmtree("predictions")

    os.mkdir("predictions")

    model = load_model(os.path.join("temp", "model", os.listdir(os.path.join("temp", "model"))[0]))

    print("Obtaining images.")
    oldImages = imageUploadUtils.getAllPredictImages("temp")

    print("Preprocessing images.")
    images = preprocess_input(oldImages)

    print("Beginning Xception download.")
    xc = Xception(include_top = False, weights = 'imagenet', input_shape = images[0].shape)

    print("Beginning passthrough of images through Xception.")
    images = xc.predict(images)

    print("Beginning passthrough of images through trained model.")
    ys = model.predict(images)

    with open(os.path.join("temp", "label", os.listdir(os.path.join("temp", "label"))[0]), 'rb') as f:
        labels = pickle.load(f)
        
    counters = dict((v, 0) for v in labels.values())

    print("Beginning image output.")
    for category in counters.keys():
        os.mkdir(os.path.join("predictions", category))

    for i, y in enumerate(ys):
        category = labels[np.argmax(y)]
        cv2.imwrite(os.path.join("predictions", category, str(counters[category]) + ".jpg"), oldImages[i])

        counters[category] += 1
    print("Image output complete.")
