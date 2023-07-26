#File containing loop that reads games until the minimum number has been reached#
import chess
import chess.pgn


def gameRead():
    print("***You must enter a minimum of 3 games to choose from (2 games would be too easy to guess from!)")
    
    #Create an empty list for loaded games/filenames
    gameList = []
    moveCounts = []
    fileList = [] 
    filename = ''

    #While loop based on counter
    while(len(gameList) < 3):

        #grab files from user and check if there is an error
        filename = input("\nPlease enter the name of your PGN file (without the .pgn at the end): ")
        
        if(filename in fileList):
            print("\nGame has already been entered, please choose a different file!")
            continue
        file = f"{filename}.pgn"
        try:
            pgn = open("games/"+file)
        except FileNotFoundError:
            print("\nFile not found, Try another filename")
            continue
        game = chess.pgn.read_game(pgn)

        #check to make sure it is over the required move count (20)
        movect = 0
        for move in game.mainline_moves():
            movect = movect+.5
        
        if(movect <= 20):
            print("\nNot enough moves in this game, miniatures (<=20 moves) are not allowed!")
            continue
        else:
            print("\nSuccess! Game added to collection")
            gameList.append(game)
            moveCounts.append(movect)
            fileList.append(filename)
    
    
    while(1):
        userAns = input("\nWould you like to enter additional games?(Y/N)")
        if(userAns.upper() != 'N' and userAns.upper() != 'Y'):
            print("\nPlease choose either yes(Y) or no(N)")
            continue
        elif(userAns.upper() == 'Y'):
            #grab files from user and check if there is an error
            filename = input("\nPlease enter the name of your PGN file (without the .pgn at the end): ")
        
            if(filename in fileList):
                print("\nGame has already been entered, please choose a different file!")
                continue
            file = f"{filename}.pgn"
            try:
                pgn = open("games/"+file)
            except FileNotFoundError:
                print("\nFile not found, Try another filename")
                continue
            game = chess.pgn.read_game(pgn)

        #check to make sure it is over the required move count (20)
            movect = 0
            for move in game.mainline_moves():
                movect = movect+.5
        
            if(movect <= 20):
                print("\nNot enough moves in this game, miniatures (<=20 moves) are not allowed!")
                continue
            else:
                print("\nSuccess! Game added to collection")
                gameList.append(game)
                moveCounts.append(movect)
                fileList.append(filename)
                continue
    
    
        else:
            return gameList, moveCounts