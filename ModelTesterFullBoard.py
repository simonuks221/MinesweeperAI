
from keras.models import load_model
import pandas as pd
import numpy as np
from minesweeperGameLogic import GameInstance
import matplotlib.pyplot as plt

BOARD_SIZE = 10


model = load_model('modelisFullBoard.h5')


gm = GameInstance(BOARD_SIZE, 10)
# printOutTHeBoard(board, revealed)

# main game loop


def FindLowestValue(gm):
    newBoard = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not gm.revealed[i][j]:
                newBoard.append(0.9)
            else:
                newBoard.append(gm.board[i][j])
    newBoard = [newBoard]
    newBoard = np.array(newBoard)
    output = model.predict(newBoard, verbose=0)
    maxIndex = 0
    maxValue = 0
    # print(len(output[0]))
    for i in range(len(output[0])):
        if newBoard[0][i] == 0.9:
            if output[0][i] > maxValue:
                maxIndex = i
                maxValue = output[0][i]
    row = maxIndex / (BOARD_SIZE)
    col = maxIndex % (BOARD_SIZE)
    # gm.printOutTheBoard()
    #print(row, col, maxIndex)
    return ((int(row)), int(round(col))), output[0][maxIndex]


def PlayGame(printout=False):
    gm.GenerateBoard()
    roundIndex = 0
    while True:
        roundIndex += 1
        # print the board

        # get input from the user
        (row, col), confidence = FindLowestValue(gm)
        if printout:
            gm.printOutTheBoard()
            print("Round ", roundIndex, " Chosen: col row",
                  col, row, " Confidence: ", confidence)
        # row = int(input("Enter row: "))
        # col = int(input("Enter column: "))

        # reveal the tile at the specified coordinates
        gm.reveal_tile(row, col)

        outcome = gm.checkWinCondition()
        if outcome == 1:
            print("Game WON!")
            return roundIndex
        elif outcome == -1:
            # print("Game LOST!")
            return roundIndex


generateGraphs = True
if generateGraphs:
    allRounds = []
    for i in range(0, 100):
        print("Round checked: ", i)
        newRound = PlayGame(False)
        allRounds.append(newRound)
    maxRound = max(allRounds)
    plt.hist(allRounds, bins=maxRound)
    plt.title("Kiek teisingu spejimu padaryta per 100 zaidimu")
    plt.xlabel("Teisingu spejimu skaicius")
    plt.ylabel("Zaidimu skaicius")
    plt.xticks(range(1, maxRound))
    plt.show()
else:
    PlayGame(True)
