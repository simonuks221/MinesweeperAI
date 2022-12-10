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
    newList = ast.literal_eval(df['Board'][i])
    # print(type(newList))
    # my_list.append(newList.reshape((5, 5)))
    # print(newList)
    train_x.append(newList)
    train_y.append(ast.literal_eval(df['Bombs'][i]))

X_train, X_val, y_train, y_val = train_test_split(
    train_x, train_y, test_size=0.2)

b = np.array([0])
c = np.array(b)

print(type(c))
print(X_train[0])
model = Sequential([
    Dense(1000, input_shape=(
        len(X_train[0]),), activation='relu'),
    Dense(4096, activation='relu'),
    Dense(2048, activation='relu'),
    Dense(512, activation='relu'),
    Dense(100)
])

model.compile(optimizer='adam',
              loss='mean_absolute_error')

X_train = np.array(X_train)
y_train = np.array(y_train)
history = model.fit(X_train,
                    y_train,
                    batch_size=64, epochs=50, verbose=1, validation_data=(X_val, y_val),
                    callbacks=[keras.callbacks.EarlyStopping(patience=5)])

save_model(model, 'modelisFullBoard.h5')
