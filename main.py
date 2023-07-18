#Utilizes python-chess library (listed in requirements.txt file)#
import chess
import chess.pgn
from pgnReader import gameRead


print("Welcome to the Chess Recall Program!")
print("\n-------------------------------------")

gameList = gameRead()

for move in gameList[0].mainline_moves():
    print(move)