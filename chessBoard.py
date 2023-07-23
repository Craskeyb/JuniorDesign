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
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
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



if __name__ == "__main__":
    main()