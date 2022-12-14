import numpy as np
from keras.layers import Input, Conv2D
from keras import Sequential
from tensorflow import keras
import pandas as pd
import ast

D_SIZE = 2
df = pd.read_csv('{id}x{id}TrainData.csv'.format(id=D_SIZE*2+1))


my_list = []
for i in range(11):
    listas = np.array(ast.literal_eval(df['BoardValues'][i]))
    listas = listas.reshape((5, 5, 10))
    listas = listas.tolist()
    my_list.append(listas)
# reshape the list into a 3-dimensional array


model = Sequential([
    Input(shape=(5, 5, 10)),
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    Conv2D(1, (3, 3), padding='same', activation='relu'),
])

model.compile(optimizer='adam',
              loss='mean_absolute_error')

data_y = []
for i in range(11):
    data_y.append(int(df['TileValue'][i]))

history = model.fit(np.array(my_list),
                    np.array(data_y),
                    batch_size=64, epochs=10, verbose=1, validation_split=0.2,
                    callbacks=[keras.callbacks.EarlyStopping(patience=5)])
