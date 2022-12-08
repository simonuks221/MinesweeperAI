import random
import matplotlib.pyplot as plt
from tensorflow import keras
# nuosekliai jungtam neuroniniam tinklui
from keras import Sequential, Input, Model
# sluoksniai kuriuos desim i neuronini tinkla
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from keras.layers import Dense, Concatenate, Embedding, Flatten, LSTM
from keras.utils import plot_model
from keras.models import save_model, load_model
import pandas as pd
import numpy as np
from minesweeperGameLogic import GameInstance

BOARD_SIZE = 10

dataset_x = []
dataset_y = []


def generateDatasetEntry(gm, i, j):
    visible = 0
    neighbours = []
    if gm.board[i][j] == -1:
        trueMember = 0
    else:
        trueMember = 1


def generate_dataset(gm, dataset_x, dataset_y):
    # check if the game is over
    outcome = gm.checkWinCondition()
    if outcome == 1:
        #print("Game WON!")
        return
    elif outcome == -1:
        #print("Game LOST!")
        return

    newBoard = []
    newMines = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not gm.revealed[i][j]:
                newBoard.append(0.9)
            else:
                newBoard.append(gm.board[i][j])

            if gm.board[i][j] == -1:
                newMines.append(0)
            else:
                newMines.append(1)
    dataset_x.append(newBoard)
    dataset_y.append(newMines)

    '''for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not gm.revealed[i][j] and gm.board[i][j] != -1:
                gm.reveal_tile(i, j)
                gm.checked = [[0 for i in range(BOARD_SIZE)]
                              for j in range(BOARD_SIZE)]
                generate_dataset(gm, dataset_x, dataset_y)'''


gm = GameInstance(BOARD_SIZE, 10)

for i in range(100000):
    if i % 1000 == 0:
        print(i)
    gm.GenerateBoard()
    generate_dataset(gm, dataset_x, dataset_y)


df = pd.DataFrame(list(zip(dataset_x, dataset_y)),
                  columns=['Board', 'Bombs'])
df.to_csv('FullBoardTrainData.csv')
