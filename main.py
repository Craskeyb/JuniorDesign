#Utilizes python-chess library (listed in requirements.txt file)#
import chess
import chess.pgn
from pgnReader import gameRead


print("Welcome to the Chess Recall Program!")
print("\n-------------------------------------")

gameList, moveCounts = gameRead()

board = chess.Board()

print(gameList[0])
print(moveCounts[0])