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
from sklearn.preprocessing import StandardScaler

# define the size of the board
BOARD_SIZE = 10
D_SIZE = 2

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
    # print(board)
    #printOutTHeBoard(board, revealed)


#GenerateBoard(board, revealed)
#printOutTHeBoard(board, revealed)

# main game loop
while False:
    # print the board
    printOutTHeBoard(board, revealed)
    # get input from the user
    row = int(input("Enter row: "))
    col = int(input("Enter column: "))

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

dataset_x = []

dataset_y = []

# function to generate a dataset of game states and scores


def generateDatasetEntry(board, revealed, i, j):
    visible = 0
    neighbours = []
    if board[i][j] == -1:
        trueMember = 0
    else:
        trueMember = 1
    for x in range(-D_SIZE, D_SIZE+1):
        for y in range(-D_SIZE, D_SIZE+1):
            if i+x >= 0 and j+y >= 0 and i+x < BOARD_SIZE-1 and j+y < BOARD_SIZE-1:
                if not revealed[i+x][j+y]:
                    neighbours.append(9/10)
                else:
                    visible += 1
                    neighbours.append(board[i+x][j+y]/10)
            else:
                return False, neighbours, trueMember
    if visible > 2:  # viso 25
        return True, neighbours, trueMember
    else:
        return False, neighbours, trueMember


def generate_dataset(board, revealed, dataset_x, dataset_y):
    global checked
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
        return

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if revealed[i][j] and board[i][j] != 0:
                for x in range(-D_SIZE, D_SIZE+1):
                    for y in range(-D_SIZE, D_SIZE+1):
                        if i+x >= 0 and j+y >= 0 and i+x < BOARD_SIZE and j+y < BOARD_SIZE:
                            if not revealed[i+x][j+y] and checked[i+x][j+y] == 0:
                                success, neighbours, trueMembers = generateDatasetEntry(
                                    board, revealed, i+x, j+y)
                                if success:
                                    checked[i+x][j+y] = 1
                                    dataset_x.append(neighbours)
                                    dataset_y.append(trueMembers)
            # go through the board and generate a dataset for each empty space of the largest size
    '''for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not revealed[i][j]:
                reveal_tile(board, revealed, i, j)
                checked = [[0 for i in range(BOARD_SIZE)]
                           for j in range(BOARD_SIZE)]
                generate_dataset(board, revealed, dataset_x, dataset_y)
'''


for i in range(20000):
    if i % 1000 == 0:
        print(i)
    GenerateBoard()
    generate_dataset(board, revealed, dataset_x, dataset_y)


df = pd.DataFrame(list(zip(dataset_x, dataset_y)),
                  columns=['BoardValues', 'TileValue'])
df.to_csv('{id}x{id}TrainData.csv'.format(id=D_SIZE*2+1))
