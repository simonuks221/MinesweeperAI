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
D_SIZE = 4

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


df = pd.read_csv('{id}x{id}TrainData.csv'.format(id=D_SIZE*2+1))

my_list = []
for i in range(df.shape[0]):
    newList = np.array(ast.literal_eval(df['BoardValues'][i]))
    #my_list.append(newList.reshape((5, 5)))
    # print(newList)
    my_list.append(newList)
my_list = np.array(my_list)
print(my_list.shape)
print()

model = Sequential([
    Dense(4096, input_shape=(
        my_list.shape[1],)),
    Dense(2048),
    Dense(512),
    Dense(1)
])

model.compile(optimizer='adam',
              loss='mean_absolute_error')

history = model.fit(my_list,
                    df['TileValue'],
                    batch_size=32, epochs=50, verbose=1, validation_split=0.2,
                    callbacks=[keras.callbacks.EarlyStopping(patience=5)])

save_model(model, 'modelis{id}x{id}.h5'.format(id=D_SIZE*2+1))
