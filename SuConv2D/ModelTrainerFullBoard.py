from tensorflow import keras
import tensorflow as tf
# nuosekliai jungtam neuroniniam tinklui
from keras import Sequential
# sluoksniai kuriuos desim i neuronini tinkla
from keras.layers import Dense, Input, Conv2D, MaxPooling2D, Flatten
from keras.models import save_model, load_model
import pandas as pd
import numpy as np
import ast
from sklearn.model_selection import train_test_split
from minesweeperGameLogic import GameInstance
gm = GameInstance(1, 1)

BOARD_SIZE = 5

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# model = load_model('modelisFullBoard.h5')

model = Sequential([
    # Conv2D(128, (3, 3), padding='same',
    #       input_shape=(BOARD_SIZE, BOARD_SIZE, 10)),
    #Conv2D(16, (2, 2), padding='same'),

    Conv2D(filters=1024, kernel_size=3, strides=(2, 2),
           activation='elu', input_shape=(BOARD_SIZE, BOARD_SIZE, 10)),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(BOARD_SIZE*BOARD_SIZE)
])


model.compile(optimizer='adam',
              loss="mean_absolute_error")

print(model.summary())
print()


df = pd.read_csv('FullBoardTrainData.csv')

train_x = []
train_y = []
for i in range(df.shape[0]):
    if i % 1000 == 0:
        print("{a} / {b}".format(a=i, b=df.shape[0]))
    newXList = np.array(ast.literal_eval(df['Board'][i]))
    newYList = np.array(ast.literal_eval(df['Bombs'][i]))

    newnewXlist = []
    for y in range(len(newXList)):
        newnewXlist += (gm.ConvertGameTile(newXList[y]))
    newnewXlist = np.array(newnewXlist).reshape((BOARD_SIZE, BOARD_SIZE, 10))

    train_x.append(newnewXlist.tolist())
    train_y.append(newYList)

# train_x = train_x.tolist()
# train_y = train_y.tolist()

train_x = np.array(train_x)
train_y = np.array(train_y)


history = model.fit(train_x,
                    train_y,
                    batch_size=255, epochs=30, verbose=1, validation_split=0.2,
                    callbacks=[keras.callbacks.EarlyStopping(patience=5)])

save_model(model, 'modelisFullBoard.h5')
