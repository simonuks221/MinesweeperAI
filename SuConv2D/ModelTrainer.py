from tensorflow import keras
#import tensorflow as tf
# nuosekliai jungtam neuroniniam tinklui
from keras import Sequential
# sluoksniai kuriuos desim i neuronini tinkla
from keras.layers import Conv2D, Dense, Input, Flatten, MaxPooling2D
from keras.models import save_model
import pandas as pd
import numpy as np
import ast
D_SIZE = 2

# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


df = pd.read_csv('{id}x{id}TrainData.csv'.format(id=D_SIZE*2+1))

my_list = []
for i in range(df['BoardValues'].shape[0]):
    listas = np.array(ast.literal_eval(df['BoardValues'][i]))
    listas = listas.reshape((5, 5, 10))
    listas = listas.tolist()
    my_list.append(listas)

model = Sequential([
    Input(shape=(D_SIZE*2+1, D_SIZE*2+1, 10)),
    Conv2D(1024, (2, 2), padding='same'),
    Conv2D(1024, (2, 2), padding='same'),
    Conv2D(512, (2, 2), padding='same'),
    Conv2D(1, (2, 2), padding='same'),
    MaxPooling2D(pool_size=(D_SIZE*2+1, D_SIZE*2+1)),
    Dense(1, activation='softmax')

    # Flatten(name='flatten')
])
'''Conv2D(64, (3, 3), padding='same', data_format='channels_first',
           activation='relu', use_bias=True),
    Conv2D(64, (3, 3), padding='same', data_format='channels_first',
           activation='relu', use_bias=True),
    Conv2D(1, (1, 1), padding='same', data_format='channels_first',
           activation='sigmoid', use_bias=True)'''


'''Dense(256, input_shape=(
        my_list.shape[1],), activation='elu'),
    Dense(1024, activation='elu'),
    Dense(512, activation='elu'),
    Dense(32, activation='elu'),
    Dense(1, activation='elu')'''


model.compile(optimizer='adam',
              loss='mean_absolute_error')

data_y = []
for i in range(df['BoardValues'].shape[0]):
    data_y.append(int(df['TileValue'][i]))
data_y = df['TileValue']

history = model.fit(np.array(my_list),
                    np.array(data_y),
                    batch_size=4, epochs=20, verbose=1, validation_split=0.2,
                    callbacks=[keras.callbacks.EarlyStopping(patience=5)])

save_model(model, 'modelis{id}x{id}.h5'.format(id=D_SIZE*2+1))
