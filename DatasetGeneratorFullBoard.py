import pandas as pd
import numpy as np
from minesweeperGameLogic import GameInstance

BOARD_SIZE = 10

# Nulis, vienas, du, trys, keturi, penki, sesi, septyni, astuoni, nematomas
dataset_x = []
dataset_y = []  # Bomba = -1, nebomba = 1


def generate_dataset(gm, dataset_x, dataset_y):
    # check if the game is over
    outcome = gm.checkWinCondition()
    if outcome == 1:
        # print("Game WON!")
        return
    elif outcome == -1:
        # print("Game LOST!")
        return

    newBoard, newMines = gm.ConvertGameBoard()
    dataset_x.append(newBoard)
    dataset_y.append(newMines)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not gm.revealed[i][j] and gm.board[i][j] != -1:
                gm.reveal_tile(i, j)
                gm.checked = [[0 for i in range(BOARD_SIZE)]
                              for j in range(BOARD_SIZE)]
                generate_dataset(gm, dataset_x, dataset_y)


gm = GameInstance(BOARD_SIZE, 10)

for i in range(10000):
    if i % 1000 == 0:
        print(i)
    gm.GenerateBoard()
    generate_dataset(gm, dataset_x, dataset_y)


df = pd.DataFrame(list(zip(dataset_x, dataset_y)),
                  columns=['Board', 'Bombs'])
df.to_csv('FullBoardTrainData.csv')
