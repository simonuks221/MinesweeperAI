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
import matplotlib.pyplot as plt
gm = GameInstance(1, 1)

BOARD_SIZE = 5

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
model = Sequential([
    Conv2D(filters=512, kernel_size=5, strides=(1, 1), padding="same",
           activation='elu', input_shape=(BOARD_SIZE, BOARD_SIZE, 10)),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(BOARD_SIZE*BOARD_SIZE)
])


model.compile(optimizer='adam',
              loss="mean_absolute_error", metrics=['acc'])

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

train_x = np.array(train_x)
train_y = np.array(train_y)


history = model.fit(train_x,
                    train_y,
                    batch_size=255, epochs=30, verbose=1, validation_split=0.2,
                    callbacks=[keras.callbacks.EarlyStopping(patience=5)])

save_model(model, 'modelisFullBoard.h5')

# performace grafa
plt.plot(history.history['acc'], c='blue', lw=3)
plt.plot(history.history['val_acc'], c='orange', lw=3)
plt.title('Tikslumo grafikas')
plt.xlabel('Iteracijos, (a.k. epochs)')
plt.ylabel('tikslumas, (a.k. accuracy)')
plt.legend(['acc', 'val_acc'])
plt.grid(True)
plt.show()

# ---- Loss measure---
plt.plot(history.history['loss'], c='blue', lw=3)
plt.plot(history.history['val_loss'], c='orange', lw=3)
plt.title('Tikslumo grafikas')
plt.xlabel('Iteracijos, (a.k. epochs)')
plt.ylabel('Paklaida, (a.k. loss)')
plt.legend(['loss', 'val_loss'])
plt.grid(True)
plt.show()
