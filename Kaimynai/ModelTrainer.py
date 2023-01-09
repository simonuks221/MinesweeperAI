from tensorflow import keras
import tensorflow as tf
from keras import Sequential
from keras.layers import Dense
from keras.models import save_model
import pandas as pd
import numpy as np
import ast
from minesweeperGameLogic import GameInstance
import matplotlib.pyplot as plt
gm = GameInstance(1, 1)

D_SIZE = 2  # Kiek kaimynu iš šonų imti, 1 - 3x3, 2 - 5x5 kaimynai.

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


df = pd.read_csv('{id}x{id}TrainData.csv'.format(id=D_SIZE*2+1))

# Apdoroti duomenis i one-hot
my_list = []
for i in range(df.shape[0]):
    if i % 1000 == 0:
        print("{a} / {b}".format(a=i, b=df.shape[0]))
    newList = np.array(ast.literal_eval(df['BoardValues'][i]))
    newnewXlist = []
    for y in range(len(newList)):
        newnewXlist += (gm.ConvertGameTile(newList[y]))
    my_list.append(newnewXlist)
my_list = np.array(my_list)

# Modelis
model = Sequential([
    Dense(4096, input_shape=(
        my_list.shape[1],)),
    Dense(1024),
    Dense(512),
    Dense(1)
])

model.compile(optimizer='adam',
              loss='mean_absolute_error',  metrics=['acc'])

history = model.fit(my_list,
                    df['TileValue'],
                    batch_size=4096, epochs=30, verbose=1, validation_split=0.2,
                    callbacks=[keras.callbacks.EarlyStopping(patience=5)])


save_model(model, 'modelis{id}x{id}.h5'.format(id=D_SIZE*2+1))

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
