'''
This program creates a 2D game board and runs a two player game called 'Reversi'
Players take turns placing their disks on the board with their assigned colour (Black and White).
Black is the first player to move.
A player may place their disk anywhere on the board, as long as it surrounds a group of the opponents disks,
(vertically, horizontally, or diagonally) on opposite sides.
Any disks that you surround will become yours and will flip over to your colour.
The goal of the game is to occupy the most tiles when there is no more legal moves for ANY player

Written by Jensen Khemchandani - CMPUT 175
'''

class Reversi:
    # Reversi class -> Responsible for the construction of game instances
    def __init__(self, rows, columns):
        # self - instance of the Reversi class
        # rows - length of tiles in the createBoard
        # columns - width of tiles in the board
        # Check for immediate errors upon creation of a game instance!
        assert isinstance(rows, int) and isinstance(columns, int), "TypeError -> Rows/columns need to be integers!"
        assert rows > 1 and columns > 1, "Requested board size is too small! Must by 2 by 2 or larger!"
        assert rows % 2 == 0 and columns % 2 == 0, "Rows and columns must be even numbers!"

        # Board variables/data
        self.rows = rows
        self.columns = columns
        self.board = self.createBoard()

        # Player variables/data
        self.playerColour = ''
        self.computerColour = ''
        self.currentTurn = 'b'
        self.playerScore = 2
        self.computerScore = 2
        self.smartMode = False
        self.gameOverSearch = False
              
    def createBoard(self):
        # self - instance of the Reversi class!
        # Creates a 2D grid representing the Reversi game board and returns it as a nested list.

        grid = []
        for row in range(self.rows):
            gridRow = []
            for column in range(self.columns):
                gridRow.append(".")
            grid.append(gridRow)

        '''
        Fills out the first 4 spaces in the grid as shown in the example
        '''

        grid[(self.rows // 2) - 1][(self.rows // 2) - 1] = 'w'
        grid[(self.rows // 2)][(self.rows // 2)] = 'w'
        grid[(self.rows // 2) - 1][(self.rows // 2)] = 'b'
        grid[(self.rows // 2)][(self.rows // 2) - 1] = 'b'

        return grid

    def displayBoard(self):
        # self - instance of the Reversi class!
        # Prints the Reversi board in a formatted manner with margin numbers to represent each space
        print("     ", end = "")
        for i in range(self.rows):
            print(i, end="    ")
        print("\n")

        for i in range(len(self.board)):
            print(i, end="    ")
            for j in range(len(self.board[i])):
                print(self.board[i][j], end="    ")
            print("\n")

    def newGame(self):
        # self - instance of the Reversi class!
        # Reset all game/Reversi values and set up a new game!
        self.board = self.createBoard()
        self.playerColour = ''
        self.computerColour = ''
        self.playerScore = 2
        self.computerScore = 2
        return

    def getScore(self, colour):
        # self - instance of the Reversi class!
        # colour - The colour of the player the user wants to get the score for
        score = 0
        if colour == self.computerColour:
            score = self.computerScore
        else:
            score = self.playerScore
        return score

    def isPositionValid(self, position, colour):
        # self - instance of the Reversi class!
        # colour - The colour of the player the user wants to check for
        # position - A list [i,j] where i is the row and j is the column
        otherColour = ''
        if colour == 'w':
            otherColour = 'b'
        else:
            otherColour = 'w'

        '''
        A move is only valid if it is touching a piece of the other colour in any direction, and somehow creates a 'sandwich'
        around the other colour's pieces.
        '''
        valid = False

        # If the space provided is empty, check to see if the choseb position is touching a position occupied by the other player
        if self.board[position[0]][position[1]] == ".":

            touchingOtherColour = self.checkAdjacent(position, colour, otherColour)
            if(not touchingOtherColour and not self.gameOverSearch):
                print("Invalid position: Piece doesn't surround line of opponent pieces")
                return valid

            # Loop through all the straight lines from the chosen position and count the amount of tiles to be flipped

            if(touchingOtherColour):
                pointsToEarn = 0
                row = position[0] 
                column = position[1] 
                
                searchList = [(0, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                
                for i in range(len(searchList)):
                    startRow = (row + searchList[i][0])
                    startColumn = (column + searchList[i][1])
                    currentRow = startRow
                    currentColumn = startColumn
                    points = 0
                    while currentRow >= 0 and currentRow < self.rows and currentColumn >= 0 and currentColumn < self.columns:
                        if(self.board[currentRow][currentColumn] == "."):
                            break
                        if(self.board[currentRow][currentColumn] == otherColour):
                            points += 1
                        if(self.board[currentRow][currentColumn] == colour):
                            pointsToEarn += points
                            break
                        currentRow += searchList[i][0]
                        currentColumn += searchList[i][1]
                
                if(pointsToEarn > 0):
                    valid = True

                # elif pointsToEarn == 0 and not gameOverSearch:
                    # print("Invalid position: Piece doesn't surround line of opponent pieces")

                elif pointsToEarn == 0 and not self.gameOverSearch:
                    print("Invalid position: Piece doesn't surround line of opponent pieces")

                if(self.smartMode):
                    return valid, pointsToEarn

        elif self.board[position[0]][position[1]] != '.' and colour == self.playerColour and not self.gameOverSearch:
            print("Invalid position: Occupied tile!")

        return valid

    def setPlayerColour(self, colour):
        # Set the colour for the human player to the designated colour, giving the compter the other colour
        # colour - The colour of the player the user wants to play as ("b" or "w")
        if colour == 'w':
            self.playerColour = 'w'
            self.computerColour = 'b'
        else:
            self.playerColour = 'b'
            self.computerColour = 'w'
        return

    def isGameOver(self):
        # Return true if the game is over, false otherwise
        # The game is over if the current player cannot make a move, no matter whose turn it is
        
        gameOver = False
        self.gameOverSearch = True
        for i in range(self.rows):
            for j in range(self.columns):   
                isValid = ''
                if self.currentTurn == 'w':
                    isValid = self.isPositionValid([i, j], 'w')
                    
                else:
                    isValid = self.isPositionValid([i, j], 'b')
                
                if self.smartMode:
                    if(type(isValid) is tuple and isValid[0] is True):
                        return False
                    
                    elif isValid == True:
                        return False
                else:
                    if(isValid):
                        return False
        return True     
                    
    def flipTiles(self, listOfTiles, colour):
        # Takes a list of tiles to 'flip', and changes them to the opposite colour.abs
        # listOfTiles - A list containing coordinates of a grid to flip
        # colour - The colour to 'flip' the tiles to.
        for i in range(len(listOfTiles)):
            row = listOfTiles[i][0]
            column = listOfTiles[i][1]
            self.board[row][column] = colour
            if colour == self.playerColour:
                self.playerScore += 1
                self.computerScore -= 1
            else:
                self.computerScore += 1
                self.playerScore -= 1

    def makeMovePlayer(self, position):
        # Make the move given by 'position' for the current player.
        # This function also handles the capturing of pieces

        colour = self.currentTurn
        otherColour = ''
        if(colour == self.playerColour):
            otherColour = self.computerColour
        else:
            otherColour = self.playerColour

        isValid = self.isPositionValid(position, colour)
        if(isValid):
            # Place the new tile
            self.board[position[0]][position[1]] = colour
            if(colour == self.playerColour):
                self.playerScore += 1
            else:
                self.computerScore += 1
                
            row = position[0] 
            column = position[1]     
            
            # Loops through all possible directions from the position to find tiles to flip
            # This list contains the coordinates to 'jump' by each iteration
            searchList = [(0, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]                       
            for i in range(len(searchList)):
                tempTileHolder = []
                startRow = (row + searchList[i][0])
                startColumn = (column + searchList[i][1])
                currentRow = startRow
                currentColumn = startColumn
                while currentRow >= 0 and currentRow < self.rows and currentColumn >= 0 and currentColumn < self.columns:
                    # If the current tile we are checking is the current turn's colour -> Stop and flip the apprpriate tiles
                    if(self.board[currentRow][currentColumn] == colour):
                        self.flipTiles(tempTileHolder, colour)
                        break
                    # If the current tile is the other player's colour, add it to the list of tiles to be flipped
                    if(self.board[currentRow][currentColumn] == otherColour):
                        tempTileHolder.append([currentRow, currentColumn])
                    
                    # If the current tile is empty, Stop the loop and move to next path.
                    if(self.board[currentRow][currentColumn] == "."):
                        break
                    
                    # Increment the row/column by the specified amount
                    currentRow += searchList[i][0]
                    currentColumn += searchList[i][1]            
            
            self.displayBoard()
            print("Player score: (" + self.playerColour + ")" , self.playerScore)
            print("Computer score: (" + self.computerColour + ")", self.computerScore)
            
        else:
            print("Not a valid move!")
        return

    def makeMoveNaive(self):
        # This function makes a naive (no strategy involved) move for the computer.
        # Loop through possible moves until the first valid one is found, then play it.
        self.gameOverSearch = True
        for i in range(self.rows):
            for j in range(self.columns):

                isValid = self.isPositionValid([i, j], self.computerColour)

                if(isValid):

                    print("Computer moving: " + str([i,j]))
                    self.makeMovePlayer([i, j])
                    return
        self.isGameOver()

    def makeMoveSmart(self):
        # This function makes a smart (strategy involved) move for the computer.
        # Gets a list of all valid moves, and picks the move that immediately earns the most points for the computer
        validMoves = []
        self.gameOverSearch = True
        for i in range(self.rows):
            for j in range(self.columns):

                isValid = self.isPositionValid([i, j], self.computerColour)

                if(type(isValid) is tuple and isValid[0] is True):
                    validMoves.append([isValid[1], [i, j]])
        # print(validMoves)
        if(len(validMoves) != 0):
            maxScore = validMoves[0][0]
            maxCoords = validMoves[0][1]
            for i in range(len(validMoves)):
                if(validMoves[i][0] > maxScore):
                    maxScore = validMoves[i][0]
                    maxCoords = validMoves[i][1]

            print("Computer moving: " + str(maxCoords))
            self.makeMovePlayer(maxCoords)
            self.gameOverSearch = False
        else:
            self.isGameOver()

    def checkAdjacent(self, position, colour, otherColour):
        # This method checks to see if a position is touching another tile of opposite colour in the grid!
        touchingOtherColour = False

        if((position[0] != self.rows - 1 and self.board[position[0] + 1][position[1]] == otherColour)): # Down
            touchingOtherColour = True

        if((position[0] != 0 and self.board[position[0] - 1][position[1]] == otherColour)): # Up
            touchingOtherColour = True

        if((position[1] != self.columns - 1 and self.board[position[0]][position[1] + 1] == otherColour)): # Right
            touchingOtherColour = True

        if((position[1] != 0 and self.board[position[0]][position[1] - 1] == otherColour)): # Left
            touchingOtherColour = True

        if((position[0] != self.rows - 1 and position[1] != self.columns - 1 and self.board[position[0] + 1][position[1] + 1] == otherColour)): # Down/Right
            touchingOtherColour = True

        if((position[0] != 0 and position[1] != 0 and self.board[position[0] - 1][position[1] - 1] == otherColour)): # Up/Left
            touchingOtherColour = True

        if((position[0] != self.rows - 1 and position[1] != 0 and self.board[position[0] + 1][position[1] - 1] == otherColour)): # Down/Left
            touchingOtherColour = True

        if((position[0] != 0 and position[1] != self.columns - 1 and self.board[position[0] - 1][position[1] + 1] == otherColour)): # Up/Right
            touchingOtherColour = True

        return touchingOtherColour
