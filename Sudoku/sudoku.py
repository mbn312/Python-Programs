import random
import copy

counter = 0

#generates a random sudoku board
def create():

    global counter

    #blank is the desired amount of blank spots for the puzzle
    blank = 60
    #fail is the maximum amount of failures allowed
    fail = 10
    
    valid = False

    #creates a random valid sudoku solution
    while ( not valid ):
        board = [[0 for i in range(9)] for x in range(9)]
        #calls on the solve function to fill in the grid and make sure that it is valid
        valid = solve(board,False)
  
    #keeps removing spaces until wanted number of blank spots or maximum amount of failures is reached
    while (fail > 0 and blank > 0):
        counter = 0
        test_board = copy.deepcopy(board)

        #randomly chooses a filled in spot to remove
        while True:
            rand = random.randint(0,80)
            rem = (rand//9,rand%9)
            if(test_board[rem[0]][rem[1]] != 0):
                test_board[rem[0]][rem[1]] = 0
                break
        
        #tests to see if board with the random spot removed has only one solution
        solve(test_board,True)

        #if it only has one solution it will keep the change or else it will count as a failure
        if(counter == 1):
            board[rem[0]][rem[1]] = 0
            blank -= 1
        else:
            fail -= 1

    #returns the created board
    return board

#function prints out an inputted board
def printboard(board):
    print("-------------------------------------")
    for r in range(9):
        if( ( r % 3 ) ==  0 and r != 0):
            print("|-----------|-----------|-----------|")
        row = "|  "
        for c in range(9):
            if ( c == 0 ):
                sep = ""
            elif ( (c % 3) == 0 ):
                sep = "  |  "
            else:
                sep = "  "
            if (board[r][c] == 0):
                v = " "
            else:
                v = str(board[r][c])
            row = row + sep + v
        print(row + "  |")
    print("-------------------------------------")


#function returns whether or not the board is solvable, solves the board, and/or gets the number of solutions
def solve(board,c): #c paramater determines whether or not to get the number of possible solutions
    idx = (0,0)
    while(board[idx[0]][idx[1]] != 0): #loops through the board looking for an empty spot
        if (idx[1] + 1 > 8):
            idx = (idx[0] + 1, 0)
        else:
            idx = (idx[0], idx[1] + 1)

        if (idx == (9,0)): #if the board is filled, returns that the board is solvable
            return True

    numList = [i for i in range(1,10)] 
    random.shuffle(numList) #shuffles the domain to generate a random puzzle
    for check in numList:
        if isValid(board, idx[0],idx[1],check): #checks to see if a number is valid for that spot
            board[idx[0]][idx[1]] = check
            if ( solve(board,c) ): #recursively calls the function to see if the number leads to a solution
                if( c ):  
                    #if it is and the function is looking for number of solutions, it will increment possible solutions by 1
                    global counter 
                    counter += 1
                else:
                    return True #returns that the board is solvable

            board[idx[0]][idx[1]] = 0

    return False #returns that the board is not solvable if it isn't

#function checks to see if a number is valid for a certain position
def isValid(b,row,col,check):

    #checks to see if any spots in the same row have the same value
    for c in range(9):
        if( b[row][c] == check and c != col):
            return False

    #checks to see if any spots in the same column have the same value
    for r in range(9):
        if (b[r][col] == check and r != row):
            return False

    #checks to see if any spots in the same box have the same value
    x = 3 * ( col // 3 )
    y = 3 * ( row // 3 )
    for r in range(3):
        for c in range(3):
            if( b[y+r][x+c] == check and (y+r,x+c) != (row,col)):
                return False

    return True

#function that returns whether or not a board is valid
def validBoard(board):

    global counter
    counter = 0

    test_board = copy.deepcopy(board)
    solve(test_board,True)
    
    if ( counter > 1 ): #if a board has more than one possible solution, it is not valid
        print("\nBoard is not valid.\n")
        return False 
    else:
        solve(test_board,False)
        for row in range(9):
            for col in range(9):
                if (not isValid(test_board,row,col,test_board[row][col])):
                    print("\nBoard is not valid.\n")
                    return False
    print("\nBoard is valid.\n")
    return True

#runs the program
def run():

    print("\n===============================================\n")
    print("\tSudoku")
    print("\n===============================================\n")

    board = create()
    printboard(board)
    solve(board,False)
    #waits for the user to hit enter to show the solution
    input("\nPress <Enter> to show solution.\n")
    printboard(board)
    print()

run()
