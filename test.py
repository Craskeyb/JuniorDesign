#Utilizes python-chess library (listed in requirements.txt file)#
import chess
import chess.pgn
from pgnReader import gameRead
from chessboard import display

print("Running accuracy checks for pgnReader functionality...")
print("\n-------------------------------------")

gameList, moveCounts = gameRead()

#Run through games to make sure they have the correct moves after being loaded in
