import matplotlib.pyplot as plt
from tensorflow import keras
from keras.models import load_model
import pandas as pd
import numpy as np
import ast
from minesweeperGameLogic import GameInstance

D_SIZE = 2
BOARD_SIZE = 15

df = pd.read_csv('{id}x{id}TrainData.csv'.format(id=D_SIZE*2+1))

model = load_model('modelis{id}x{id}.h5'.format(id=D_SIZE*2+1))


def getNeighbours(i, j, gm):
    neighbours = []
    for x in range(-D_SIZE, D_SIZE+1):
        for y in range(-D_SIZE, D_SIZE+1):
            if i+x >= 0 and j+y >= 0 and i+x < BOARD_SIZE and j+y < BOARD_SIZE:
                if not gm.revealed[i+x][j+y]:
                    neighbours.append(9/10)
                else:
                    neighbours.append(gm.board[i+x][j+y]/10)
    return neighbours


def FindLowestValue(gm):
    testableTiles = []
    testableTileCoords = []

    for i in range(1, BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if not gm.revealed[i][j]:
                neighbours = getNeighbours(i, j, gm)
                if len(neighbours) == (1+2*D_SIZE)*(1+2*D_SIZE):
                    testableTiles.append(neighbours)
                    testableTileCoords.append((i, j))
    #testableTiles = np.array(testableTiles)
    output = model.predict(testableTiles)

    minIndex = np.argmax(output)

    return testableTileCoords[minIndex]


gm = GameInstance(BOARD_SIZE, 10)
gm.GenerateBoard()
#printOutTHeBoard(board, revealed)

# main game loop
roundIndex = 0
while True:
    roundIndex += 1
    # print the board
    gm.printOutTHeBoard()
    # get input from the user
    (row, col) = FindLowestValue(gm)
    print("Round ", roundIndex, " Chosen: ", col, row)
    #row = int(input("Enter row: "))
    #col = int(input("Enter column: "))

    # reveal the tile at the specified coordinates
    gm.reveal_tile(row, col)

    # check if the game is over
    game_over = False
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if gm.board[i][j] == -1 and gm.revealed[i][j]:
                # if a mine is revealed, the game is over
                game_over = True
                break
        if game_over:
            break
    if game_over:
        print("Game over!")
        break
