from tensorflow.keras.applications.xception import preprocess_input, Xception
from tensorflow.keras.models import load_model
import pickle, cv2, numpy as np, imageUploadUtils, directoryUtils, os

def predict(images_dir_path='temp'):

    print("Obtaining images.")
    subdir = 'images' if images_dir_path == 'temp' else None
    oldImages, imageNames = imageUploadUtils.getAllPredictImages(images_dir_path, subdir=subdir)

    model = load_model(os.path.join("temp", "model", os.listdir(os.path.join("temp", "model"))[0]))
    
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

    print("Beginning image output.")
    if images_dir_path == 'temp':    
        if os.path.exists("predictions"):
            directoryUtils.rmtree("predictions")
        os.mkdir("predictions")

        counters = dict((v, 0) for v in labels.values())

        for category in counters.keys():
            os.mkdir(os.path.join("predictions", category))

        for i, y in enumerate(ys):
            category = labels[np.argmax(y)]
            cv2.imwrite(os.path.join("predictions", category, str(counters[category]) + ".jpg"), oldImages[i])

            counters[category] += 1
    else:
        output_dir = os.path.join(images_dir_path, "predictions")
        if os.path.isdir(output_dir):
            directoryUtils.rmtree(output_dir)
        os.mkdir(output_dir)
        
        for category in labels.values():
            os.mkdir(os.path.join(output_dir, category))

        for i, y in enumerate(ys):
            category = labels[np.argmax(y)]
            cv2.imwrite(os.path.join(output_dir, category, imageNames[i]), oldImages[i])

    print("Image output complete.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('usage: python modelPredict.py {imagesDir}')
        sys.exit(0)
    imagesDir = sys.argv[1]
    print(f'images_dir_path={imagesDir}')
    predict(images_dir_path=imagesDir)