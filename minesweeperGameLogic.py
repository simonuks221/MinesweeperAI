import random
from termcolor import colored

num_mines = 10


class GameInstance:
    def __init__(self, board_size, num_mines):
        self.BOARD_SIZE = board_size
        self.num_mines = num_mines

    def placeMines(self):
        # place the mines randomly on the board
        num_mines = 25
        while num_mines > 0:
            i = random.randint(0, self.BOARD_SIZE-1)
            j = random.randint(0, self.BOARD_SIZE-1)
            if self.board[i][j] != -1:
                # if i > 1 and j > 1 and i < self.BOARD_SIZE-1 and j < self.BOARD_SIZE-1:
                self.board[i][j] = -1
                num_mines -= 1

    def count_adjacent_mines(self, i, j):
        count = 0
        for x in range(i-1, i+2):
            for y in range(j-1, j+2):
                if x >= 0 and x < self.BOARD_SIZE and y >= 0 and y < self.BOARD_SIZE and self.board[x][y] == -1:
                    count += 1
        return count

    def checkWinCondition(self):
        hiddenTiles = 0
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == -1 and self.revealed[i][j]:
                    # if a mine is revealed, the game is over
                    return -1
                if not self.revealed[i][j]:
                    hiddenTiles += 1
        if hiddenTiles == self.num_mines:
            return 1
        else:
            return 0

    def reveal_tile(self, i, j):
        if i >= 0 and i < self.BOARD_SIZE and j >= 0 and j < self.BOARD_SIZE and not self.revealed[i][j]:
            self.revealed[i][j] = True
            if self.board[i][j] == 0:
                # if the tile is a blank space, also reveal all adjacent tiles
                self.reveal_tile(i-1, j)
                self.reveal_tile(i+1, j)
                self.reveal_tile(i, j-1)
                self.reveal_tile(i, j+1)
                self.reveal_tile(i-1, j-1)
                self.reveal_tile(i-1, j+1)
                self.reveal_tile(i+1, j+1)
                self.reveal_tile(i+1, j-1)

    def printOutTheBoard(self):
        for i in range(self.BOARD_SIZE+1):
            print("--", end="")
        print()
        for i in range(self.BOARD_SIZE):
            print("|", end="")
            for j in range(self.BOARD_SIZE):
                if self.revealed[i][j]:
                    if self.board[i][j] == -1:
                        print("*", end=" ")
                    elif self.board[i][j] == 0:
                        print(" ", end=" ")
                    elif self.board[i][j] == 1:
                        print(colored("1", "blue"), end=" ")
                    elif self.board[i][j] == 2:
                        print(colored("2", "green"), end=" ")
                    elif self.board[i][j] == 3:
                        print(colored("3", "red"), end=" ")
                    elif self.board[i][j] == 4:
                        print(colored("4", "yellow"), end=" ")
                    elif self.board[i][j] == 5:
                        print(colored("5", "magenta"), end=" ")
                    else:
                        print(colored(self.board[i][j], "cyan"), end=" ")
                else:
                    print("#", end=" ")
            print("|")
        for i in range(self.BOARD_SIZE+1):
            print("--", end="")
        print()

    def GenerateBoard(self):
        self.revealed = [[False for i in range(self.BOARD_SIZE)]
                         for j in range(self.BOARD_SIZE)]
        # initialize the board with all zeroes
        self.board = [[0 for i in range(self.BOARD_SIZE)]
                      for j in range(self.BOARD_SIZE)]
        self.checked = [[0 for i in range(self.BOARD_SIZE)]
                        for j in range(self.BOARD_SIZE)]

        self.placeMines()
        # go through the board and count the number of mines adjacent to each non-mine cell
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] != -1:
                    self.board[i][j] = self.count_adjacent_mines(i, j)

        # Start with empty spaces revealed
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == 0:
                    self.reveal_tile(i, j)

    def ConvertGameBoard(self):
        newBoard = []
        newMines = []
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                newTile = []

                if not self.revealed[i][j]:
                    newTile += [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                else:
                    for ii in range(0, 9):
                        if self.board[i][j] == ii:
                            newTile += [1]
                        else:
                            newTile += [0]
                    newTile += [0]
                newBoard += newTile
                if self.board[i][j] == -1:
                    newMines.append(0)
                else:
                    newMines.append(1)
        return newBoard, newMines
