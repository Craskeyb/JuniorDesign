### IMPLEMENTATION FOR CHESS BOARD FOUND AT: https://www.youtube.com/watch?v=o24J3WcBGLg ###
### SUBSEQUENT VIDEOS FROM ABOVE SERIES WERE USED FOR MOVE LOGIC AS WELL ###

import pygame as p
import chess
import chess.pgn
from pgnReader import gameRead
from chessboard import display
import gameState

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
    #initialize one board for the interactive board, and one board to check the moves against
    checkBoard = chess.Board()
    gameBoard = chess.Board()

    if(mode.upper() == 'S'):
        print("Available games: ")
        for i in range(0,len(gameList)):
            white = gameList[i].headers['White']
            black = gameList[i].headers['Black']
            print('('+str(i+1)+') '+white+' vs. '+black)
        index = input("Please select a number from the list of available games: ")
        userGame = gameList[int(index)-1]
        convertedBoard = fenToBoard(gameBoard.board_fen())
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
                        gs.makeMove(move)
                        checkBoard.push(moveArr[curMove])
                        curMove+=1
                        if(boardToFen(gs.board) != checkBoard.board_fen()):
                            print('That move was incorrect! Please restart the program to try again')
                            running = False
                        sqSelected = ()
                        playerClicks = []
                        
            drawGameState(screen,gs)
            clock.tick(MAX_FPS)
            p.display.flip()

    else:        
            gs = gameState.GameState()

    

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

def convertNotation(move):    
    #Extracting necessary information from the move object
    pieceMoved = move.pieceMoved
    pieceCaptured = move.pieceCaptured
    startSq = (move.getChessNotation())[0:1]
    endSq = (move.getChessNotation())[2:]
    
    if int(pieceMoved == 'wp') | int(pieceMoved == 'bp'):
        #Notation for pawn moves is only the square rank+file
        if(pieceCaptured == '--'):
            newNotation = endSq
            return newNotation
        else:
            startSq = startSq[0]
            newNotation = startSq+'x'+endSq
            return newNotation
    else:
        #Other pieces have a letter indicating which piece it is
        if(pieceCaptured == '--'):
            pieceMoved = pieceMoved[1]
            newNotation = pieceMoved + endSq
            return newNotation
        else:
            pieceMoved = pieceMoved[1]
            newNotation = pieceMoved +'x' + endSq
            return newNotation

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


if __name__ == "__main__":
    main()