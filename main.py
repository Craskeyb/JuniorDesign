# DEPRECATED FILE, WAS USED DURING TESTING FOR PGNREADER FUNCTIONALITY & FEN VISUALIZATION WITH CHESS-BOARD LIBRARY #

#Utilizes python-chess & chess-board libraries (listed in requirements.txt file)#
import chess
import chess.pgn
from pgnReader import gameRead
from chessboard import display


print("Welcome to the Chess Recall Program!")
print("\n-------------------------------------")

gameList, moveCounts = gameRead()

board = chess.Board()

moveArr = []
for moves in gameList[0].mainline_moves():
    moveArr.append(moves)
    #print(board.board_fen())

for i in range(0,len(moveArr)):
    board.push(moveArr[i])

valid_fen = board.board_fen()
print(valid_fen)

game_board = display.start()

while True:
    display.check_for_quit()
    display.update(valid_fen, game_board)
