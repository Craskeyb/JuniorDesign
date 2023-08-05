### IMPLEMENTATION FOR CHESS BOARD FOUND AT: https://www.youtube.com/watch?v=o24J3WcBGLg ###

### Junior Design Project 3 - Brett Craskey ###

import pygame as p
import chess
import chess.pgn
from pgnReader import gameRead
from chessboard import display
import gameState
import random

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp','wR','wN','wB','wK','wQ','bp','bR','bB','bN','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def main():
    print("Welcome to the Chess Recall Program!")
    print("\n-------------------------------------")

    #Read in files from user, and then prompt for game mode
    gameList, moveCounts = gameRead()
    mode = ''
    while(1):
        mode = input("Would you like to (S)elect a game, or have a (R)andom challenge? ")

        if(mode.upper() != 'S' and mode.upper() != 'R'):
            print("Please choose either \'S\' to select a game, or \'R\' for a random game!")
            continue
        else:
            break
    
    #initializing the GameState object
    gs = gameState.GameState()
    userGame = None
    #initialize board for the gameState object
    checkBoard = chess.Board()


    if(mode.upper() == 'S'):
        print("Available games: ")
        for i in range(0,len(gameList)):
            white = gameList[i].headers['White']
            black = gameList[i].headers['Black']
            print('('+str(i+1)+') '+white+' vs. '+black)
        index = input("Please select a number from the list of available games: ")
        userGame = gameList[int(index)-1]
        convertedBoard = fenToBoard(checkBoard.board_fen())
        gs.board = convertedBoard

        print('You selected: '+userGame.headers['White']+ ' vs. ' + userGame.headers['Black'])
        moveArr = []
        for moves in userGame.mainline_moves():
            moveArr.append(moves)
        curMove = 0
        #Driving code for the game
        p.init()
        screen = p.display.set_mode((WIDTH,HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        loadImages()
        running = True
        sqSelected = ()
        playerClicks = []
        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    col = location[0]//SQUARE_SIZE
                    row = location[1]//SQUARE_SIZE
                    if(sqSelected == (row,col)):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = gameState.Move(playerClicks[0],playerClicks[1],gs.board)
                        #Checking only columns because from 4 to 0,1 or 6,7 would normally be illegal, so the squares do not really matter for a player using legal moves
                        #Col also needs to be passed to the function so we can tell what side is attempting to be castled to
                        if (move.pieceMoved == 'bK' and move.startCol == 4 and move.startRow == 0 and (move.endCol == 1 or move.endCol == 0 or move.endCol == 6 or move.endCol == 7)):
                            gs.board = castling(gs.board, move.endCol, 'b')
                            gs.whiteToMove = not gs.whiteToMove
                            checkBoard.push(moveArr[curMove])
                            curMove+=1
                            if(boardToFen(gs.board) != checkBoard.board_fen()):
                                print('That move was incorrect! The correct move was: ' + str(moveArr[curMove-1]) + ' Please restart the program to try again')
                                running = False
                            sqSelected = ()
                            playerClicks = []
                        elif (move.pieceMoved == 'wK' and move.startCol == 4 and move.startRow == 7 and (move.endCol == 1 or move.endCol == 0 or move.endCol == 6 or move.endCol == 7)):
                            gs.board = castling(gs.board, move.endCol, 'w')
                            gs.whiteToMove = not gs.whiteToMove
                            checkBoard.push(moveArr[curMove])
                            curMove+=1
                            if(boardToFen(gs.board) != checkBoard.board_fen()):
                                print(boardToFen(gs.board))
                                print(checkBoard.board_fen())
                                print('That move was incorrect! The correct move was: ' + str(moveArr[curMove-1]) + ' Please restart the program to try again')
                                running = False
                            sqSelected = ()
                            playerClicks = []
                        else:
                            gs.makeMove(move)
                            checkBoard.push(moveArr[curMove])
                            curMove+=1
                            if(boardToFen(gs.board) != checkBoard.board_fen()):
                                print('That move was incorrect! The correct move was: ' + str(moveArr[curMove-1]) + ' Please restart the program to try again')
                                running = False
                            sqSelected = ()
                            playerClicks = []
                        if(curMove == len(moveArr)):
                            print("\n\n----------------------------------\nCongratulations! You have a great memory.\n----------------------------------")
                            running = False
            drawGameState(screen,gs)
            clock.tick(MAX_FPS)
            p.display.flip()

    else:        
        gameIndex = random.randint(0, len(gameList)-1)
        userGame = gameList[gameIndex]
        moveArr = []
        for moves in userGame.mainline_moves():
            moveArr.append(moves)

        startingMove = random.randint(6,len(moveArr)-12)
        curMove = startingMove-1
        for i in range(startingMove-1):
            checkBoard.push(moveArr[i])
        gs.board = fenToBoard(checkBoard.board_fen())
        #Driving code for the game
        p.init()
        screen = p.display.set_mode((WIDTH,HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        loadImages()
        running = True
        sqSelected = ()
        playerClicks = []
        
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

        #First prompt user for the name of the players in the game
        while(1):
            whitePl = input("Before making any moves, please identify the players in the game starting with the white side: ")
            if(whitePl.upper() != userGame.headers['White'].upper()):
                print("That is incorrect, please try again!")
                continue
            blackPl = input("That is correct! Now please identify the player for the black pieces: ")
            if(blackPl.upper() != userGame.headers['Black'].upper()):
                print('That is incorrect, please try again!')
                continue
            else:
                print("That is correct, good luck with the remaining moves!")
                break

        while running:
            
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    col = location[0]//SQUARE_SIZE
                    row = location[1]//SQUARE_SIZE
                    if(sqSelected == (row,col)):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = gameState.Move(playerClicks[0],playerClicks[1],gs.board)
                        #Checking only columns because from 4 to 0,1 or 6,7 would normally be illegal, so the squares do not really matter for a player using legal moves
                        #Col also needs to be passed to the function so we can tell what side is attempting to be castled to
                        if (move.pieceMoved == 'bK' and move.startCol == 4 and move.startRow == 0 and (move.endCol == 1 or move.endCol == 0 or move.endCol == 6 or move.endCol == 7)):
                            gs.board = castling(gs.board, move.endCol, 'b')
                            gs.whiteToMove = not gs.whiteToMove
                            checkBoard.push(moveArr[curMove])
                            curMove+=1
                            if(boardToFen(gs.board) != checkBoard.board_fen()):
                                print('That move was incorrect! The correct move was: ' + str(moveArr[curMove-1]) + ' Please restart the program to try again')
                                running = False
                            sqSelected = ()
                            playerClicks = []
                        elif (move.pieceMoved == 'wK' and move.startCol == 4 and move.startRow == 7 and (move.endCol == 1 or move.endCol == 0 or move.endCol == 6 or move.endCol == 7)):
                            gs.board = castling(gs.board, move.endCol, 'w')
                            gs.whiteToMove = not gs.whiteToMove
                            checkBoard.push(moveArr[curMove])
                            curMove+=1
                            if(boardToFen(gs.board) != checkBoard.board_fen()):
                                print('That move was incorrect! The correct move was: ' + str(moveArr[curMove-1]) + ' Please restart the program to try again')
                                running = False
                            sqSelected = ()
                            playerClicks = []
                        else:
                            gs.makeMove(move)
                            checkBoard.push(moveArr[curMove])
                            curMove+=1
                            if(boardToFen(gs.board) != checkBoard.board_fen()):
                                print('That move was incorrect! The correct move was: ' + str(moveArr[curMove-1]) + ' Please restart the program to try again')
                                running = False
                            sqSelected = ()
                            playerClicks = []
                        if(curMove == len(moveArr)):
                            print("\n\n----------------------------------\nCongratulations! You have a great memory.\n----------------------------------")
                            running = False
            drawGameState(screen,gs)
            clock.tick(MAX_FPS)
            p.display.flip()

    

def drawGameState(screen,gs):
    drawBoard(screen) #draw squares on board
    drawPieces(screen,gs.board) #draw pieces on squares

def drawBoard(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

def drawPieces(screen,board):
      for r in range(DIMENSION):
          for c in range(DIMENSION):
              piece = board[r][c]
              if piece != "--":
                  screen.blit(IMAGES[piece],p.Rect(c*SQUARE_SIZE,r*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

#Function to convert FEN format to a board usable with our interface
def fenToBoard(fen):
    boardState = []
    curRow = []
    for i in range(len(fen)): 
        if fen[i] == 'r':
            curRow.append("bR")
        elif fen[i] == 'k':
            curRow.append("bK")
        elif fen[i] == 'q':
            curRow.append("bQ")
        elif fen[i] == 'n':
            curRow.append("bN")
        elif fen[i] == 'p':
            curRow.append("bp") 
        elif fen[i] == 'b':
            curRow.append("bB") 
        elif fen[i] == 'K':
            curRow.append("wK")    
        elif fen[i] == 'R':
            curRow.append("wR")
        elif fen[i] == 'Q':
            curRow.append("wQ")
        elif fen[i] == 'N':
            curRow.append("wN")
        elif fen[i] == 'P':
            curRow.append("wp") 
        elif fen[i] == 'B':
            curRow.append("wB")
        elif fen[i] == '/':
            boardState.append(curRow)
            curRow = []
        else:
            count = int(fen[i])
            for k in range(count):
                curRow.append("--")
    boardState.append(curRow)
    return boardState 

#Function to convert our usable board into a FEN
def boardToFen(board):
    fen = ''
    for i in range(0,len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'bR':
                fen+="r"
            elif board[i][j] == 'bK':
                fen+="k"
            elif board[i][j] == 'bQ':
                fen+="q"
            elif board[i][j] == 'bN':
                fen+="n"
            elif board[i][j] == 'bp':
                fen+="p" 
            elif board[i][j] == 'bB':
                fen+="b" 
            elif board[i][j] == 'wK':
                fen+="K"    
            elif board[i][j] == 'wR':
                fen+="R"
            elif board[i][j] == 'wQ':
                fen+="Q"
            elif board[i][j] == 'wN':
                fen+="N"
            elif board[i][j] == 'wp':
                fen+="P" 
            elif board[i][j] == 'wB':
                fen+="B"    
            else:
                if(len(fen) > 0):
                    curFen = fen[len(fen)-1]
                    if(curFen=='1' or curFen=='2' or curFen=='3' or curFen=='4' or curFen=='5' or curFen=='6' or curFen=='7' or curFen=='8'):
                        continue
                    else:
                        counter = 0
                        for k in range(j,len(board[i])):
                            if board[i][k]=='--':
                                counter+=1
                            else:
                                break
                        fen+=str(counter)
                else:
                    counter = 0
                    for k in range(j,len(board[i])):
                        if board[i][k]=='--':
                            counter+=1
                        else:
                            break
                    fen+=str(counter)
        fen+='/'
    return fen[:-1]

#Function that generates a board that is a castled version of the previous position to solve the castling issue
def castling(uncastled_board, endCol, color):
    if color == 'b':
        if endCol == 6 or endCol == 7:
            uncastled_board[0][4] = "--"
            uncastled_board[0][5] = "bR"
            uncastled_board[0][6] = "bK"
            uncastled_board[0][7] = "--"
        else:
            uncastled_board[0][4] = "--"
            uncastled_board[0][3] = "bR"
            uncastled_board[0][2] = "bK"
            uncastled_board[0][1] = "--"
            uncastled_board[0][0] = "--"
    if color == 'w':
        if endCol == 6 or endCol == 7:
            uncastled_board[7][4] = "--"
            uncastled_board[7][5] = "wR"
            uncastled_board[7][6] = "wK"
            uncastled_board[7][7] = "--"
        else:
            uncastled_board[7][4] = "--"
            uncastled_board[7][3] = "wR"
            uncastled_board[7][2] = "wK"
            uncastled_board[7][1] = "--"
            uncastled_board[7][0] = "--"
    return uncastled_board

if __name__ == "__main__":
    main()
