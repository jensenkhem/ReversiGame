from reversi import Reversi
def main():
    game = None
    continueGame = True

    # Create a new Reversi object to play games with for the duration of the program
    try:
        game = Reversi(8, 8)
    except AssertionError:
        print("Error occurred when creating Reversi class!")
        raise
    # If game was successfully created, set up the game!
    else:
        while(continueGame):
            gameReady = False
            smartMode = False
            playerColour = ''

            # Let the user choose between smart/dumb AI
            print("Starting new game!")
            print("Black goes first, then white")
            smartChoice = input("Enter '1' to choose easy computer opponent, '2' for hard computer opponent: ")
            while smartChoice not in ['1', '2']:
                smartChoice = input("Enter '1' to choose easy computer opponent, '2' for hard computer opponent: ")
            if(smartChoice == '2'):
                game.smartMode = True
                smartMode = True
            elif(smartChoice == '1'):
                game.smartMode = False
                smartMode = False
            # Let the player chose their starting colour!
            playerColour =  input("Would you like to play as white, or black? (w/b)")
            while playerColour not in ['w', 'b']:
                playerColour = input("Would you like to play as white, or black? (w/b)")
            game.setPlayerColour(playerColour)
            print("You have chosen to play as " + game.playerColour + "\n")
            gameReady = True
            currentTurn = 'b'
            game.displayBoard()
            # Once the player has chosen difficulty and colour, carry out the game!
            while(gameReady):
                # Check if the game is over before each move
                if not game.isGameOver():

                    game.gameOverSearch = False

                    # Let the player pick coordinates for a move, and carry out that move - switch turns once completed
                    if game.playerColour == currentTurn:
                        validMove = False
                        print("Please enter a valid move! (Numbers from 0-7 seperated by a space,\n first number is the row, second number is the column!)")
                        while not validMove:
                            print("Enter 'q' to immediately quit the game!")
                            playerPosition = []
                            move = ''
                            validSyntax = False
                            while not validSyntax:
                                move = input("Enter a move: ")
                                if(move == ""):
                                    print("Please enter a valid move!")
                                elif move == 'q':
                                    print("Ending game...")
                                    return
                                elif move[0] not in ['0','1','2','3','4','5','6','7']:
                                    print("Out of bounds! Choose a row number between 0-7")
                                elif move[1] != " ":
                                    print("Please separate the numbers with a space!")
                                elif move[2] not in ['0','1','2','3','4','5','6','7']:
                                    print("Out of bounds! Choose a column number between 0-7")
                                else:
                                    playerPosition.append(int(move[0]))
                                    playerPosition.append(int(move[2]))
                                    validSyntax = True

                            validMove = game.isPositionValid(playerPosition, game.playerColour)
                            if(type(validMove) is tuple):
                                validMove = validMove[0]

                        game.makeMovePlayer(playerPosition)
                            
                        currentTurn = game.computerColour
                        game.currentTurn = game.computerColour

                    # If it is NOT the player's turn and smart AI is on, carry out a smart move for the computer
                    elif game.playerColour != currentTurn and game.smartMode == True:
                        game.makeMoveSmart()
                        currentTurn = game.playerColour
                        game.currentTurn = game.playerColour

                    # If it is NOT the player's turn and the computer is NOT on smart mode, carry out a random move for the computer
                    else:
                        game.makeMoveNaive()
                        currentTurn = game.playerColour
                        game.currentTurn = game.playerColour

                # If the game has ended, print out the conclusion/results of the game, and ask the player if they would like to play again.
                else:
                    gameReady = False
                    print("Game over!! Final scores:\nPlayer score: " + str(game.getScore(game.playerColour)) + "\nComputer score: " + str(game.getScore(game.computerColour)))
                    if(game.getScore(game.playerColour) > (game.getScore(game.computerColour))):
                        print("You win!!")
                    elif(game.getScore(game.playerColour) == (game.getScore(game.computerColour))):
                        print("Tie game! :)")
                    else:
                        print("The computer wins!")

                    playAgain = input("Would you like to play again? (y/n)")
                    while playAgain not in ['y', 'n']:
                        playAgain = input("Would you like to play again? (y/n)")

                    if(playAgain == 'n'):
                        continueGame = False
                        print("Thanks for playing!")
                        return

                    else:
                        print("Setting up a new game...\n")
                        game.newGame()
main()
