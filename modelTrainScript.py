import tensorflow as tf, numpy as np, os, pickle, cv2, random, modelHolder, imageUploadUtils, shutil
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications.xception import preprocess_input, Xception
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def generateNewTrainingData(splitRatio):
    images, labels, classes = imageUploadUtils.getAllTrainImages('temp')
    print(images[:2], labels[:2], classes)

    trainx, testx, trainy, testy = train_test_split(images, labels, test_size = 1 - splitRatio, stratify = labels)
    
    xc = Xception(include_top = False, weights = 'imagenet', input_shape = trainx[0].shape)
    
    trainx = np.array(trainx)
    testx = np.array(testx)

    trainx = preprocess_input(trainx)
    testx = preprocess_input(testx)
    trainx = xc.predict(trainx)
    testx = xc.predict(testx)

    print(f"{len(trainx)} images have been collected for training.")
    print(f"{len(testx)} images have been collected for testing.")
    print(f"is data valid? {len(trainx) == len(trainy) and len(testx) == len(testy)}")

    finaldata = (trainx, np.array(trainy), testx, np.array(testy))

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

    mc = ModelCheckpoint(os.path.join('output', 'model.h5'), monitor='val_loss', mode='auto', verbose=1, save_best_only=True)

    history = model.fit(x = allData[0], y = allData[1], batch_size = 3, epochs = epoch, verbose = 1, validation_data = (allData[2], allData[3]), callbacks = [mc])

    return history.history
