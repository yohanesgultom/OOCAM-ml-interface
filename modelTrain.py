import tensorflow as tf, numpy as np, os, pickle, cv2, random, modelHolder, imageUploadUtils, directoryUtils
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications.xception import preprocess_input, Xception
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def generateNewTrainingData(splitRatio, dim=(256, 256)):
    print("Obtaining images.")
    images, labels, classes = imageUploadUtils.getAllTrainImages('temp', dim=dim)

    trainx, testx, trainy, testy = train_test_split(images, labels, test_size = 1 - splitRatio, stratify = labels)

    print("Beginning Xception download.")
    xc = Xception(include_top = False, weights = 'imagenet', input_shape = trainx[0].shape)
    
    trainx = np.array(trainx)
    testx = np.array(testx)

    print("Beginning preprocessing for training set.")
    trainx = preprocess_input(trainx)
    
    print("Beginning preprocessing for testing set.")
    testx = preprocess_input(testx)

    print("Beginning passthrough of training set through Xception.")
    trainx = xc.predict(trainx, verbose = 1)

    print("Beginning passthrough of testing set through Xception.")
    testx = xc.predict(testx, verbose = 1)

    print(f"{len(trainx)} images have been collected for training.")
    print(f"{len(testx)} images have been collected for testing.")
    print(f"is data valid? {len(trainx) == len(trainy) and len(testx) == len(testy)}")

    finaldata = (trainx, np.array(trainy), testx, np.array(testy))

    if os.path.exists("output"):
        directoryUtils.rmtree("output")

    os.makedirs("output")

    with open(os.path.join('output', 'labels.dat'), 'wb+') as f:
        pickle.dump(classes, f)

    return finaldata
    
def trainModel(splitRatio, epoch, dim=(256, 256)):
    print("Generating training data.")
    allData = generateNewTrainingData(splitRatio, dim=dim)

    print("Getting classifier model.")
    model = modelHolder.getModel(allData)

    model.compile(loss="sparse_categorical_crossentropy",
                                    optimizer="adam",
                                    metrics=["accuracy"])

    filename_loss = os.path.join('output', 'min_loss_{val_loss:.3f}_{val_accuracy:.3f}.h5')
    mc_loss = ModelCheckpoint((filename_loss), monitor='val_loss', mode='auto', verbose=1, save_best_only=True)

    filename_acc = os.path.join('output', 'max_acc_{val_loss:.3f}_{val_accuracy:.3f}.h5')
    mc_acc = ModelCheckpoint((filename_acc), monitor='val_accuracy', mode='auto', verbose=1, save_best_only=True)

    print("Beginning training.")
    history = model.fit(x = allData[0], y = allData[1], batch_size = 3, epochs = epoch, verbose = 1, validation_data = (allData[2], allData[3]), callbacks = [mc_loss, mc_acc])

    loss_models = []
    accuracy_models = []
    
    for file in os.listdir("output"):
        if file.endswith(".h5"):
            if file.startswith("min_loss"):
                loss_models.append(os.path.join("output", file))
            else:
                accuracy_models.append(os.path.join("output", file))
    
    loss_models.sort(key = os.path.getmtime, reverse = True)
    accuracy_models.sort(key = os.path.getmtime, reverse = True)

    for file in loss_models[min(3, len(loss_models)):]:
        os.remove(file)

    for file in accuracy_models[min(3, len(accuracy_models)):]:
        os.remove(file)

    print("Training complete.")
    return history.history
