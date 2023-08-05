# Chess Project - Junior Design Final Project
Project utilizing the python-chess & pygame libraries.

Allows you to upload PGN files of games you would like to study, and tests your recognition skills. Users can upload a minimum of 3 games, and games cannot be miniatures (<= 20 moves). The program will allow you to select a game to play through, or it will select a random middlegame position from one of the uploaded PGN files and you must correctly identify the players of the game. After that, you will be asked to identify the next move in the position.

## User Guide
In order to use the program, first clone the repo onto your local machine. Next, upload your desired games into the 'games' directory located within the project - this is the filepath that is read from by the pgnReader function. After uploading your games, you are ready to use the program. Just run the below code in the directory containing the project:
  - py ChessProgram.py

This will launch the program, and will prompt you to enter your files.

*NOTES ON CHESSBOARD INTERACTION*: 
When interacting with the chessboard, the proper way to move the pieces is first to click on the piece you desire to move, followed by the desired square. Any misinputs or illegal move attempts will be recognized as incorrect moves, and will end the program. It is best to excercise caution when clicking, as haphazard clicking within the interactive chessboard can be recognized as incorrect moves. 

Additionally, to castle your king the procedure is as follows:
  - Click first on the king.
  - Click second on either the rook or the square adjacent to the rook.

## Game Modes
The program offers two game modes to choose from: Selected Game mode, and Random Challenge mode. 

For selected game mode, you will be given the option to choose a desired game from the list of those you uploaded, and then you must attempt to play through each move of the game from start to finish. If you make an incorrect move, the program will exit and you will be required to start over.

For the Random Challenge mode, one of the games you've uploaded will be chosen at random, and you will be given a random middlegame position. From here, before attempting to make any moves on the chessboard, you are required to identify the players of the game. You will continue to be prompted until you get the correct answer for both sides (white & black). The chess board will be inaccessible until you correctly identify the players. After you identify the players, you will then be required to play out the remainder of the moves of the game. If you make an incorrect move, it behaves the same as the selected game mode.

For either game mode, if you make it to the end of the game, you will be greeted by a congratulatory message. After this, you may restart the program to play again.
