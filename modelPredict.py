from tensorflow.keras.models import load_model
import pickle, cv2, numpy as np

def predict(modeldir, imagedir, labeldir):
    model = load_model(modeldir)

    img = cv2.imread(imagedir)

    x = np.array([img], dtype = 'float32')

    ys = model.predict(x)

    y = ys[0]

    with open(labeldir, 'rb') as f:
        labels = pickle.load(f)
    print(y)
    return labels[np.argmax(y)]
