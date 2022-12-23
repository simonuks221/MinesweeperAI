from keras.models import load_model
import pandas as pd
import numpy as np
from minesweeperGameLogic import GameInstance
import matplotlib.pyplot as plt

D_SIZE = 4
num_of_mines = 20
BOARD_SIZE = 20

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
            # else: #For edges of board
                # neighbours.append(0)
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
    #testableTiles = np.array(testableTiles)
    output = model.predict(testableTiles, verbose=0)
    minIndex = np.argmax(output)
    return testableTileCoords[minIndex], output[minIndex]


gm = GameInstance(BOARD_SIZE, num_of_mines)
#printOutTHeBoard(board, revealed)

# main game loop


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
            print("Round ", roundIndex, " Chosen: ",
                  col, row, " Confidence: ", confidence)
        #row = int(input("Enter row: "))
        #col = int(input("Enter column: "))

        # reveal the tile at the specified coordinates
        gm.reveal_tile(row, col)

        outcome = gm.checkWinCondition()
        if outcome == 1:
            print("Game WON!")
            return roundIndex
        elif outcome == -1:
            #print("Game LOST!")
            return roundIndex


generateGraphs = False
if generateGraphs:
    allRounds = []
    for i in range(0, 100):
        print("Round checked: ", i)
        newRound = PlayGame()
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
