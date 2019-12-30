import tensorflow as tf, numpy as np, os, pickle, cv2, random, modelHolder, imageUploadUtils, shutil
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def generateNewTrainingData(splitRatio):
    images, labels, classes = imageUploadUtils.getAllTrainImages('temp')
    print(images[:2], labels[:2], classes)

    trainx, testx, trainy, testy = train_test_split(images, labels, test_size = 1 - splitRatio, stratify = labels)

    print(f"{len(trainx)} images have been collected for training.")
    print(f"{len(testx)} images have been collected for testing.")
    print(f"is data valid? {len(trainx) == len(trainy) and len(testx) == len(testy)}")

    finaldata = (np.array(trainx), np.array(trainy), np.array(testx), np.array(testy))

    if os.path.exists("output"):
        shutil.rmtree("output")

    os.makedirs("output")

    with open(os.path.join('output', 'labels.dat'), 'wb+') as f:
        pickle.dump(classes, f)

    return finaldata
    
def trainModel(splitRatio, epoch):
    allData = generateNewTrainingData(splitRatio)

    model = modelHolder.getModel(allData)

    model.compile(loss="sparse_categorical_crossentropy",
                                    optimizer="adam",
                                    metrics=["accuracy"])

    mc = ModelCheckpoint(os.path.join('output', 'model.h5'), monitor='val_loss', mode='max', verbose=1, save_best_only=True)

    history = model.fit(x = allData[0], y = allData[1], batch_size = 30, epochs = epoch, verbose = 1, validation_data = (allData[2], allData[3]), callbacks = [mc])

    return history.history
