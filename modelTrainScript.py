import tensorflow as tf, numpy as np, os, pickle, cv2, random, modelHolder
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def generateNewTrainingData(datadir, splitRatio):
    folders = os.listdir(datadir)
    imageCount = len(os.listdir((datadir + "\\" + folders[0])))
    
    trainImageCount = int(imageCount * splitRatio)

    labels = dict((ind, breed) for ind, breed in enumerate(folders))

    trainX = []
    trainY = []

    testX = []
    testY = []

    for ind, folder in enumerate(folders):
        folderImages = [cv2.imread(datadir + "\\" + folder + "\\" + folder + str(i) + ".jpg") for i in range(imageCount)]

        random.shuffle(folderImages)

        trainX.extend(folderImages[:trainImageCount])
        testX.extend(folderImages[trainImageCount:])

        trainY.extend([ind for _ in range(trainImageCount)])
        testY.extend([ind for _ in range(imageCount - trainImageCount)])

    print(f"{len(trainX)} images have been collected for training.")
    print(f"{len(testX)} images have been collected for testing.")
    print(f"Is data valid? {len(trainX) == len(trainY) and len(testX) == len(testY)}")

    finalData = (np.array(trainX), np.array(trainY), np.array(testX), np.array(testY), labels)

    if not os.path.exists("output"):
        os.makedirs("output")

    with open('output\\labels.dat', 'wb+') as f:
        pickle.dump(labels, f)

    return finalData

def trainModel(newDatadir, splitRatio, epoch):
        
    allData = generateNewTrainingData(newDatadir, splitRatio)

    model = modelHolder.getModel(allData)

    model.compile(loss="sparse_categorical_crossentropy",
                                    optimizer="adam",
                                    metrics=["accuracy"])

    mc = ModelCheckpoint('output\\model.h5', monitor='val_loss', mode='max', verbose=1, save_best_only=True)

    history = model.fit(x = allData[0], y = allData[1], batch_size = 30, epochs = epoch, verbose = 1, validation_data = (allData[2], allData[3]), callbacks = [mc])

    return history.history

    
