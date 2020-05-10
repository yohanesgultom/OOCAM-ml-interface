import cv2, numpy as np, os, re

def getAllTrainImages(directory, dim=(256, 256)):
    allFiles = os.listdir(directory)
    labels = []
    
    images = []

    print("Beginning image read and resize process.")
    for file in allFiles:        
        img = cv2.imread(os.path.join(directory, file))
        resized = cv2.resize(img, dim)
        images.append(resized)
        label = file.split('_')[1]
        labels.append(label)

    classes = list(set(labels))

    labels = [classes.index(l) for l in labels]

    classes = dict((i, v) for i, v in enumerate(classes))

    print("Read and resize complete.")
    return images, labels, classes

def getAllPredictImages(directory, dim=(256, 256), subdir=None):
    if subdir:
        directory = os.path.join(directory, subdir)
    allFiles = os.listdir(directory)

    images = []
    names = []

    print("Beginning image read and resize process.")
    for file in allFiles:
        full_path = os.path.join(directory, file)
        if os.path.isfile(full_path):
            img = cv2.imread(full_path) 
            resized = cv2.resize(img, dim)
            images.append(resized)
            names.append(file)
    
    print("Read and resize complete.")
    return np.array(images), names