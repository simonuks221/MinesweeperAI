from tensorflow import keras
import tensorflow as tf
# nuosekliai jungtam neuroniniam tinklui
from keras import Sequential
# sluoksniai kuriuos desim i neuronini tinkla
from keras.layers import Dense
from keras.layers import Dense
from keras.models import save_model
import pandas as pd
import numpy as np
import ast
from sklearn.model_selection import train_test_split

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


df = pd.read_csv('FullBoardTrainData.csv')

train_x = []
train_y = []
for i in range(df.shape[0]):
    newXList = np.array(ast.literal_eval(df['Board'][i]))
    newYList = np.array(ast.literal_eval(df['Bombs'][i]))
    train_x.append(newXList)
    train_y.append(newYList)
# train_x = train_x.tolist()
# train_y = train_y.tolist()

train_x = np.array(train_x)
train_y = np.array(train_y)
print()

model = Sequential([
    Dense(512, input_shape=(train_x.shape[1],), activation='relu'),
    Dense(512, activation='relu'),
    Dense(100)
])

model.compile(optimizer='adam',
              loss="mean_absolute_error")

history = model.fit(train_x,
                    train_y,
                    batch_size=64, epochs=10, verbose=1, validation_split=0.2,
                    callbacks=[keras.callbacks.EarlyStopping(patience=5)])

save_model(model, 'modelisFullBoard.h5')
