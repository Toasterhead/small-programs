#A solution to Chapter 1, Exercise 15 of the book Problem Solving with Algorithms and Data Structures Using Python.

#Simulates a Sudoku board and can solve very simple Sudoku puzzles.

class Sudoku(object):
    """Class for a sudoku puzzle."""

    DIMENSIONS_BOARD = 9
    DIMENSIONS_NONET = 3

    ROW     = 0
    COLUMN  = 1

    def __init__(self, board):

        assert type(board) is list and len(board) == Sudoku.DIMENSIONS_BOARD
        for row in board:
            assert type(row) is list and len(row) == Sudoku.DIMENSIONS_BOARD
            for space in row:
                assert type(space) is int and space >= 0 and space <= 9
            
        self.board = board

    def extract_row(self, index):       return self.board[index]
    
    def extract_column(self, index):    return [row[index] for row in self.board]
    
    def extract_nonet(self, nonetRowIndex, nonetColumnIndex):
        
        nonetRows = []

        for rowIndex in range(
             nonetRowIndex      * Sudoku.DIMENSIONS_NONET,
            (nonetRowIndex + 1) * Sudoku.DIMENSIONS_NONET):

            nonetRows.append([])
            
            for columnIndex in range(
                 nonetColumnIndex       * Sudoku.DIMENSIONS_NONET,
                (nonetColumnIndex + 1)  * Sudoku.DIMENSIONS_NONET):

                nonetRows[rowIndex % Sudoku.DIMENSIONS_NONET].append(
                    self.board[rowIndex][columnIndex])

        return nonetRows

    def get_unmarked(self, nonet):

        marked  = [False for i in range(10)]
        found   = False

        for i in range(1, 10):
            found = False
            for row in nonet:
                for space in row:
                    if i == space:
                        marked[i] = True
                        found = True
                        break
                if found: break

        return [i for i in range(1, 10) if not marked[i]]

    def solve(self, printingOn = False):

        DIMENSIONS = int(Sudoku.DIMENSIONS_BOARD / Sudoku.DIMENSIONS_NONET)
        
        while not self.__is_solved():

            for nonetRowIndex in range(DIMENSIONS):
                for nonetColumnIndex in range(DIMENSIONS):

                    if printingOn: print(
                        "\nAnalyzing nonet (" + \
                        str(nonetRowIndex) + ", " + \
                        str(nonetColumnIndex) + \
                        ")...\n")
                    nonet = self.extract_nonet(nonetRowIndex, nonetColumnIndex)
                    self.__analyze_nonet(
                        nonet,
                        nonetRowIndex,
                        nonetColumnIndex,
                        printingOn)

        if printingOn:
            print("\nSolved.")
            print(self)

    def __analyze_nonet(self, nonet, nonetRow, nonetColumn, printingOn):

        ROW     = Sudoku.ROW
        COLUMN  = Sudoku.COLUMN

        unmarked = self.get_unmarked(nonet)

        for number in unmarked:

            if printingOn: print("Checking for " + str(number) + "...")

            possiblePositions = []

            for relativeRowIndex in range(Sudoku.DIMENSIONS_NONET):
                for relativeColumnIndex in range(Sudoku.DIMENSIONS_NONET):

                    if nonet[relativeRowIndex][relativeColumnIndex] == 0:

                        absolute = Sudoku.absolute_position(
                            relativeRowIndex,
                            relativeColumnIndex,
                            nonetRow,
                            nonetColumn)
                            
                        if (not number in self.extract_row(absolute[ROW])) and \
                           (not number in self.extract_column(absolute[COLUMN])):

                            if printingOn:
                                print(str(number) + " is possible at (" + \
                                      str(absolute[ROW]) + ", " + \
                                      str(absolute[COLUMN]) + ").")
                            possiblePositions.append(absolute)
                            
            if len(possiblePositions) == 1:
                
                row     = possiblePositions[0][ROW]
                column  = possiblePositions[0][COLUMN]
                self.board[row][column] = number

                if printingOn:
                    print("Marked " + str(number) + " at (" + \
                          str(row) + ", " + \
                          str(column) + ").")               
                    print(self)
                    input("Press any key to continue...")

    def __is_solved(self):

        solved = True
        
        for i in range(Sudoku.DIMENSIONS_BOARD):
            for j in range(Sudoku.DIMENSIONS_BOARD):

                if self.board[i][j] == 0:
                    solved = False
                    break
            if not solved: break

        return solved
                            
    def __str__(self):

        s = ""
        
        for rowIndex in range(Sudoku.DIMENSIONS_BOARD):
            if rowIndex % Sudoku.DIMENSIONS_NONET == 0: s += "\n"
            for columnIndex in range(Sudoku.DIMENSIONS_BOARD):
                if columnIndex % Sudoku.DIMENSIONS_NONET == 0: s += "  "
                if self.board[rowIndex][columnIndex] == 0:
                    s += "# "
                else: s += str(self.board[rowIndex][columnIndex]) + " "
            s += "\n"

        return s

    def absolute_position(relativeRow, relativeColumn, nonetRow, nonetColumn):

        return (
            nonetRow    * Sudoku.DIMENSIONS_NONET + relativeRow,
            nonetColumn * Sudoku.DIMENSIONS_NONET + relativeColumn)

board_1 = \
[
    [0, 0, 2,  9, 8, 0,  5, 0, 0],
    [4, 0, 0,  0, 7, 0,  0, 1, 3],
    [0, 3, 9,  6, 0, 4,  0, 7, 0],
    
    [2, 0, 0,  0, 5, 6,  4, 0, 0],
    [8, 4, 0,  3, 0, 0,  2, 0, 1],
    [9, 0, 7,  0, 0, 1,  0, 8, 6],
    
    [6, 0, 0,  7, 0, 5,  1, 3, 0],
    [0, 9, 1,  4, 0, 0,  0, 0, 5],
    [0, 2, 0,  0, 3, 0,  6, 0, 8]
]

board_2 = \
[
    [0, 0, 9,  0, 0, 0,  6, 0, 2],
    [1, 0, 0,  7, 2, 0,  0, 0, 9],
    [0, 0, 3,  9, 0, 0,  0, 0, 0],
    
    [4, 0, 0,  0, 3, 0,  0, 6, 0],
    [0, 0, 0,  5, 0, 9,  0, 0, 0],
    [0, 1, 0,  0, 6, 0,  0, 0, 3],
    
    [0, 0, 0,  0, 0, 5,  2, 0, 0],
    [5, 0, 0,  0, 4, 7,  0, 0, 8],
    [9, 0, 8,  0, 0, 0,  3, 0, 0]
]

board_3 = \
[
    [0, 8, 0,  0, 9, 4,  0, 0, 0],
    [0, 0, 9,  1, 7, 0,  0, 0, 0],
    [4, 0, 1,  0, 0, 0,  0, 0, 3],
    
    [0, 0, 8,  0, 0, 0,  0, 2, 0],
    [5, 0, 0,  9, 1, 3,  0, 0, 8],
    [0, 9, 0,  0, 0, 0,  4, 0, 0],
    
    [3, 0, 0,  0, 0, 0,  8, 0, 6],
    [0, 0, 0,  0, 5, 8,  2, 0, 0],
    [0, 0, 0,  2, 3, 0,  0, 4, 0]
]

board_4 = \
[
    [0, 9, 0,  0, 0, 7,  6, 0, 0],
    [0, 0, 6,  9, 0, 0,  4, 0, 8],
    [7, 0, 0,  0, 6, 0,  9, 2, 0],
    
    [3, 8, 9,  0, 0, 0,  0, 5, 6],
    [0, 4, 0,  3, 9, 0,  0, 0, 1],
    [2, 0, 0,  0, 0, 8,  3, 0, 4],
    
    [0, 0, 0,  2, 8, 9,  0, 4, 7],
    [0, 2, 0,  1, 0, 0,  5, 3, 0],
    [9, 0, 4,  0, 0, 3,  0, 6, 0]
]

board_empty = \
[
    [0, 0, 0,  0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0,  0, 0, 0],
    
    [0, 0, 0,  0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0,  0, 0, 0],
    
    [0, 0, 0,  0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0,  0, 0, 0]
]
