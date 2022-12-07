import matplotlib.pyplot as plt
from tensorflow import keras
# nuosekliai jungtam neuroniniam tinklui
from keras import Sequential, Input, Model
# sluoksniai kuriuos desim i neuronini tinkla
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from keras.layers import Dense, Concatenate, Embedding, Flatten, LSTM
from keras.models import save_model, load_model
import pandas as pd
import numpy as np
import ast
D_SIZE = 2

df = pd.read_csv('{id}x{id}TrainData.csv'.format(id=D_SIZE*2+1))

my_list = []
for i in range(df.shape[0]):
    newList = np.array(ast.literal_eval(df['BoardValues'][i]))
    #my_list.append(newList.reshape((5, 5)))
    # print(newList)
    my_list.append(newList)
my_list = np.array(my_list)

model = Sequential([
    Dense(128, input_shape=(
        my_list.shape[1],), activation='elu'),
    Dense(32, activation='elu'),
    Dense(1, activation='elu')
])

model.compile(optimizer='adam',
              loss='mean_absolute_error')

history = model.fit(my_list,
                    df['TileValue'],
                    batch_size=16, epochs=50, verbose=1, validation_split=0.1,
                    callbacks=[keras.callbacks.EarlyStopping(patience=10)])

save_model(model, 'modelis{id}x{id}.h5'.format(id=D_SIZE*2+1))
