import cv2, numpy, os, re

def getAllTrainImages(directory):
    allFiles = os.listdir(directory)
    labels = []
    
    query = re.compile(r'(([a-zA-Z]+)\d+).(jpg|png|jpeg)')

    images = []

    for file in allFiles:
        matches = query.findall(file)

        images.append(cv2.imread(os.path.join(directory, file)))

        labels.append(matches[0][1])

    classes = list(set(labels))

    labels = [classes.index(l) for l in labels]

    classes = dict((i, v) for i, v in enumerate(classes))

    return images, labels, classes
