
from keras.models import load_model
import pandas as pd
import numpy as np
from minesweeperGameLogic import GameInstance
import matplotlib.pyplot as plt

BOARD_SIZE = 5
BOMB_NUM = 3

model = load_model('modelisFullBoard.h5')


gm = GameInstance(BOARD_SIZE, BOMB_NUM)
# printOutTHeBoard(board, revealed)

# main game loop


def FindLowestValue(gm):
    oldBoard, newMines = gm.ConvertGameBoard()
    newBoard = np.array(oldBoard).reshape(
        (BOARD_SIZE, BOARD_SIZE, 10)).tolist()
    # print(newBoard.shape)
    # print()
    output = model.predict([newBoard], verbose=0)[0]  # [0][0][0]
    maxIndex = 0
    maxValue = 0
    # print(output)
    # print()
    for i in range(len(output)):
        if oldBoard[i*10+9] == 1:
            if output[i] > maxValue:
                maxIndex = i
                maxValue = output[i]
    row = maxIndex / (BOARD_SIZE)
    col = maxIndex % (BOARD_SIZE)
    # gm.printOutTheBoard()
    #print(row, col, maxIndex)
    return ((int(row)), int(round(col))), output[maxIndex]


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
            return roundIndex, 1
        elif outcome == -1:
            # print("Game LOST!")
            return roundIndex, 0


generateGraphs = True
graphAmount = 300
if generateGraphs:
    allRounds = []
    winlost = [0, 0]
    for i in range(graphAmount):
        print("Round checked: ", i)
        newRound, won = PlayGame(False)
        winlost[won] += 1
        allRounds.append(newRound)

    maxRound = max(allRounds)

    plt.hist(allRounds, bins=maxRound)
    plt.title(
        "Ėjimų skaičius per {g} žaidimų".format(g=graphAmount))
    plt.xlabel("Spėjimų skaičius")
    plt.ylabel("Žaidimų skaičius")
    plt.xticks(range(1, maxRound))
    plt.show()

    plt.bar(['Pralaimėta', 'Laimėta'], winlost, color='r', width=0.4)
    plt.ylabel('Žaidimų skaičius')
    plt.title(
        "Kiek kartų laimėta iš testuotų {g} zaidimu".format(g=graphAmount))
    plt.show()

    print("Laimėjimo tikimybė: {}%".format(
        winlost[1]*100/graphAmount))
else:
    PlayGame(True)
