import cv2, numpy as np, os, re

def getAllTrainImages(directory):
    allFiles = os.listdir(directory)
    labels = []
    
    query = re.compile(r'(([a-zA-Z]+)\d+).(jpg|png|jpeg)')

    images = []

    print("Beginning image read and resize process.")
    for file in allFiles:
        matches = query.findall(file)

        img = cv2.imread(os.path.join(directory, file))
        resized = cv2.resize(img, (256, 256))
        images.append(resized)

        labels.append(matches[0][1])

    classes = list(set(labels))

    labels = [classes.index(l) for l in labels]

    classes = dict((i, v) for i, v in enumerate(classes))

    print("Read and resize complete.")
    return images, labels, classes

def getAllPredictImages(directory):
    allFiles = os.listdir(os.path.join(directory, "images"))

    images = []

    print("Beginning image read and resize process.")
    for file in allFiles:
        img = cv2.imread(os.path.join(directory, "images", file)) 
        resized = cv2.resize(img, (256, 256))
        images.append(resized)
    
    print("Read and resize complete.")
    return np.array(images)
