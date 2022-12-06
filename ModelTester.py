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
import random

df = pd.read_csv('3x3TrainData.csv')

model = load_model('modelis1.h5')

BOARD_SIZE = 15
D_SIZE = 1

# initialize the revealed tiles list with all False values
revealed = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

# initialize the board with all zeroes
board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
checked = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

# define the number of mines on the board
num_mines = 10


def placeMines(board):
    # place the mines randomly on the board
    num_mines = 25
    while num_mines > 0:
        i = random.randint(0, BOARD_SIZE-1)
        j = random.randint(0, BOARD_SIZE-1)
        if board[i][j] != -1:
            board[i][j] = -1
            num_mines -= 1

# function to count the number of mines in the 8 surrounding cells


def count_adjacent_mines(board, i, j):
    count = 0
    for x in range(i-1, i+2):
        for y in range(j-1, j+2):
            if x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE and board[x][y] == -1:
                count += 1
    return count


# function to reveal a tile


def reveal_tile(board, revealed, i, j):
    if i >= 0 and i < BOARD_SIZE and j >= 0 and j < BOARD_SIZE and not revealed[i][j]:
        revealed[i][j] = True
        if board[i][j] == 0:
            # if the tile is a blank space, also reveal all adjacent tiles
            reveal_tile(board, revealed, i-1, j)
            reveal_tile(board, revealed, i+1, j)
            reveal_tile(board, revealed, i, j-1)
            reveal_tile(board, revealed, i, j+1)
            reveal_tile(board, revealed, i-1, j-1)
            reveal_tile(board, revealed, i-1, j+1)
            reveal_tile(board, revealed, i+1, j+1)
            reveal_tile(board, revealed, i+1, j-1)


def printOutTHeBoard(board, revealed):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if revealed[i][j]:
                if board[i][j] == -1:
                    print("*", end=" ")
                else:
                    print(board[i][j], end=" ")
            else:
                print("#", end=" ")
        print()


def GenerateBoard():
    global board
    global revealed
    global checked
    revealed = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    # initialize the board with all zeroes
    board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    checked = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

    placeMines(board)
    # go through the board and count the number of mines adjacent to each non-mine cell
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != -1:
                board[i][j] = count_adjacent_mines(board, i, j)

    # Start with empty spaces revealed
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                reveal_tile(board, revealed, i, j)


def getNeighbours(i, j):
    D_SIZE = 1
    global board
    global revealed
    neighbours = []
    for x in range(-D_SIZE, D_SIZE+1):
        for y in range(-D_SIZE, D_SIZE+1):
            if i+x >= 0 and j+y >= 0 and i+x < BOARD_SIZE and j+y < BOARD_SIZE:
                if not revealed[i+x][j+y]:
                    neighbours.append(9/10)
                else:
                    neighbours.append(board[i+x][j+y]/10)
    return neighbours


def FindLowestValue():
    global board
    global revealed

    testableTiles = []
    testableTileCoords = []

    for i in range(1, BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if not revealed[i][j]:
                neighbours = getNeighbours(i, j)
                if len(neighbours) == 9:
                    testableTiles.append(neighbours)
                    testableTileCoords.append((i, j))
    #testableTiles = np.array(testableTiles)
    # print(testableTiles)
    output = model.predict(testableTiles)

    minIndex = np.argmax(output)

    return testableTileCoords[minIndex]


GenerateBoard()
#printOutTHeBoard(board, revealed)

# main game loop
roundIndex = 0
while True:
    roundIndex += 1
    # print the board
    printOutTHeBoard(board, revealed)
    # get input from the user
    (row, col) = FindLowestValue()
    print("Round ", roundIndex, " Chosen: ", col, row)
    #row = int(input("Enter row: "))
    #col = int(input("Enter column: "))

    # reveal the tile at the specified coordinates
    reveal_tile(board, revealed, row, col)

    # check if the game is over
    game_over = False
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == -1 and revealed[i][j]:
                # if a mine is revealed, the game is over
                game_over = True
                break
        if game_over:
            break
    if game_over:
        print("Game over!")
        break
