import pandas as pd
import numpy as np
from minesweeperGameLogic import GameInstance

BOARD_SIZE = 5
BOMB_NUM = 3

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

    newBoard, newMines = gm.GetGameBoard()
    dataset_x.append(newBoard)
    dataset_y.append(newMines)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not gm.revealed[i][j] and gm.board[i][j] != -1:
                gm.reveal_tile(i, j)
                gm.checked = [[0 for i in range(BOARD_SIZE)]
                              for j in range(BOARD_SIZE)]
                generate_dataset(gm, dataset_x, dataset_y)


gm = GameInstance(BOARD_SIZE, BOMB_NUM)

for i in range(500000):  # Kiek zaidimu suzaisti
    if i % 1000 == 0:
        print(i)
    gm.GenerateBoard()
    generate_dataset(gm, dataset_x, dataset_y)


df = pd.DataFrame(list(zip(dataset_x, dataset_y)),
                  columns=['Board', 'Bombs'])
df.to_csv('FullBoardTrainData.csv')
