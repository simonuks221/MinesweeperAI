# sluoksniai kuriuos desim i neuronini tinkla
import pandas as pd
import numpy as np
from minesweeperGameLogic import GameInstance


D_SIZE = 2
num_of_mines = 3
BOARD_SIZE = 5

dataset_x = []
dataset_y = []


def generateDatasetEntry(gm, i, j):
    visible = 0
    neighbours = []
    if gm.board[i][j] == -1:
        trueMember = 0
    else:
        trueMember = 1
    for x in range(-D_SIZE, D_SIZE+1):
        for y in range(-D_SIZE, D_SIZE+1):
            if i+x >= 0 and j+y >= 0 and i+x < BOARD_SIZE-1 and j+y < BOARD_SIZE-1:
                if not gm.revealed[i+x][j+y]:
                    neighbours.append(-1)
                else:
                    visible += 1
                    neighbours.append(gm.board[i+x][j+y])
            else:
                neighbours.append(-1)  # Add not revealed
                # neighbours.append(0) #for edges of board
                # return False, neighbours, trueMember
    if (visible > 5):
        return True, neighbours, trueMember
    else:
        return False, neighbours, trueMember


def generate_dataset(gm, dataset_x, dataset_y):
    # check if the game is over
    outcome = gm.checkWinCondition()
    if outcome == 1:
        # print("Game WON!")
        return
    elif outcome == -1:
        # print("Game LOST!")
        return

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not gm.revealed[i][j]:
                # print("a")
                success, neighbours, trueMembers = generateDatasetEntry(
                    gm, i, j)
                if success:
                    gm.checked[i][j] = 1
                    dataset_x.append(neighbours)
                    dataset_y.append(trueMembers)
            '''
            if gm.revealed[i][j] and gm.board[i][j] != 0:
                for x in range(-D_SIZE, D_SIZE+1):
                    for y in range(-D_SIZE, D_SIZE+1):
                        if i+x >= 0 and j+y >= 0 and i+x < BOARD_SIZE and j+y < BOARD_SIZE:
                            if not gm.revealed[i+x][j+y] and gm.checked[i+x][j+y] == 0:
                                success, neighbours, trueMembers = generateDatasetEntry(
                                    gm, i+x, j+y)
                                if success:
                                    gm.checked[i+x][j+y] = 1
                                    dataset_x.append(neighbours)
                                    dataset_y.append(trueMembers)'''
            # go through the board and generate a dataset for each empty space of the largest size
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not gm.revealed[i][j]:
                gm.reveal_tile(i, j)
                gm.checked = [[0 for i in range(BOARD_SIZE)]
                              for j in range(BOARD_SIZE)]
                generate_dataset(gm, dataset_x, dataset_y)


gm = GameInstance(BOARD_SIZE, num_of_mines)

for i in range(500000):
    if i % 1000 == 0:
        print(i)
    gm.GenerateBoard()
    # gm.printOutTheBoard()
    generate_dataset(gm, dataset_x, dataset_y)


df = pd.DataFrame(list(zip(dataset_x, dataset_y)),
                  columns=['BoardValues', 'TileValue'])
df.to_csv('{id}x{id}TrainData.csv'.format(id=D_SIZE*2+1))
