import tensorflow as tf 
import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint
import pickle, cv2, random

def generateNewTrainingData(datadir, splitRatio):
    folders = os.listdir(datadir)
    print(folders)
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

    return finalData

def trainModel(datadir, splitRatio):
    newDatadir = ''

    for i in datadir:
        if i == '\\':
            newDatadir += '\\\\'
        else:
            newDatadir += i

    print(newDatadir)
        
    allData = generateNewTrainingData(newDatadir, splitRatio)

    model = Sequential()

    model.add(Conv2D(32, (3,3), input_shape = allData[0].shape[1:]))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(128, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation("relu"))

    model.add(Dense(4))
    model.add(Activation("softmax"))

    model.compile(loss="sparse_categorical_crossentropy",
                                    optimizer="adam",
                                    metrics=["accuracy", "val_acc"])

    mc = ModelCheckpoint('model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)



    model.fit(x = allData[0], y = allData[1], batch_size = 30, epochs = 10, verbose = 1, validation_data = (allData[2], allData[3]), callbacks = [mc])

trainModel(r"C:\Users\admin\Downloads\ResizedMantaImages", 0.8)

    
