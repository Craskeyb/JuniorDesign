### IMPLEMENTATION FOR CHESS BOARD FOUND AT: https://www.youtube.com/watch?v=o24J3WcBGLg ###
### SUBSEQUENT VIDEOS FROM ABOVE SERIES WERE USED FOR MOVE LOGIC AS WELL ###

import pygame as p
import chess
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
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = gameState.GameState()
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
                    print(move.getChessNotation())
                    newMove = convertNotation(move)
                    print(newMove)
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []
                    
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

def convertNotation(move):    
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

if __name__ == "__main__":
    main()