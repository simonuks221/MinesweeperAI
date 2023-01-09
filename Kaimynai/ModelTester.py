from keras.models import load_model
import pandas as pd
import numpy as np
from minesweeperGameLogic import GameInstance
import matplotlib.pyplot as plt

D_SIZE = 2
num_of_mines = 3
BOARD_SIZE = 5

df = pd.read_csv('{id}x{id}TrainData.csv'.format(id=D_SIZE*2+1))

model = load_model('modelis{id}x{id}.h5'.format(id=D_SIZE*2+1))


def getNeighbours(i, j, gm):
    neighbours = []
    for x in range(-D_SIZE, D_SIZE+1):
        for y in range(-D_SIZE, D_SIZE+1):
            if i+x >= 0 and j+y >= 0 and i+x < BOARD_SIZE and j+y < BOARD_SIZE:
                newTile = []
                if not gm.revealed[i+x][j+y]:
                    newTile += [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                else:
                    for ii in range(0, 9):
                        if gm.board[i+x][j+y] == ii:
                            newTile += [1]
                        else:
                            newTile += [0]
                    newTile += [0]
                neighbours += newTile
            else:  # For edges of board
                neighbours += [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    return neighbours


def FindLowestValue(gm):
    testableTiles = []
    testableTileCoords = []
    for i in range(1, BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if not gm.revealed[i][j]:
                neighbours = getNeighbours(i, j, gm)
                if len(neighbours) == 10*(D_SIZE*2+1)*(D_SIZE*2+1):
                    testableTiles.append(neighbours)
                    testableTileCoords.append((i, j))
    if len(testableTiles) > 0:
        output = model.predict(testableTiles, verbose=0)
        minIndex = np.argmax(output)
        return testableTileCoords[minIndex], output[minIndex]
    return (-1, -1), 999


gm = GameInstance(BOARD_SIZE, num_of_mines)

# main game loop


def PlayGame(printout=False):
    gm.GenerateBoard()
    roundIndex = 0
    while True:
        roundIndex += 1
        # print the board

        # get input from the user
        (row, col), confidence = FindLowestValue(gm)
        if row == -1 and col == -1:
            outcome = -1
        else:
            gm.reveal_tile(row, col)

            outcome = gm.checkWinCondition()

        if outcome == 1:
            print("Game WON!")
            return roundIndex, 1
        elif outcome == -1:
            #print("Game LOST!")
            return roundIndex, 0


generateGraphs = False  # Ar generuoti statistiniu grafikus ar suzaisti viena zaidima
graphAmount = 10000  # Kiek zaidimu suzaisti grafikam nupiesti
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
