import tensorflow as tf
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

def getModel(allData):
     
    model = Sequential()
    model.add(Flatten())
    model.add(Dense(32))
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(32))
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(4, activation = 'softmax'))

    return model
