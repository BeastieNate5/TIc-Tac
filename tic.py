import random
import os

# 5 = X
# 6 = O

player_mark = 1
computer_mark = 2

error = "\033[91m[X]\033[0m"

def display_board(board):
    # The function accepts one parameter containing the board's current status
    # and prints it out to the console.

    cool_board = '''
+-------+-------+-------+
|       |       |       |
|   1   |   2   |   3   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   4   |   5   |   6   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   7   |   8   |   9   |
|       |       |       |
+-------+-------+-------+'''

    ansii_codes = []
    x = 1
    for r in range(3):
        row = []
        for c in range(3):
            if board[r][c] == computer_mark:
                row.append("\033[91mX\033[0m")
            elif board[r][c] == player_mark:
                row.append("\033[92mO\033[0m")
            else:
                row.append(str(x))
            x += 1
        ansii_codes.append(row)
        row = []

    cool_board = f'''
+-------+-------+-------+
|       |       |       |
|   {ansii_codes[0][0]}   |   {ansii_codes[0][1]}   |   {ansii_codes[0][2]}   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   {ansii_codes[1][0]}   |   {ansii_codes[1][1]}   |   {ansii_codes[1][2]}   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   {ansii_codes[2][0]}   |   {ansii_codes[2][1]}   |   {ansii_codes[2][2]}   |
|       |       |       |
+-------+-------+-------+'''
    print(cool_board)


def enter_move(board):
    # The function accepts the board's current status, asks the user about their move, 
    # checks the input, and updates the board according to the user's decision.

    # yes im that lazy
    valid_inputs = [x for x in range(1,10)]
    user_input = input("Enter move: ")

    # basically it will try to convert the user input into a int
    # if it fails to do that it would normally throw a error which will stop the whole program
    # but instead I told it not to throw a error but to tell the user it bad input and rerun the function
    # Human terms: try to convet user input into a int expect if you get a ValueError then ask for user input again
    try:
        int(user_input)
    except ValueError:
        print("Invalid number")
        return enter_move(board)

    user_input = int(user_input)

    # i hate math
    row = None
    col = None

    if user_input in valid_inputs:
        if user_input > 0 and user_input <= 3:
            row = 0
            col = user_input-1
        elif user_input <= 6:
            row = 1
            col = user_input-4
        elif user_input <= 9:
            row = 2
            col = user_input-7
    else:
        print(f"{error} Invalid position, try again")
        return enter_move(board)
    
    if ([row, col] not in make_list_of_free_fields(board)):
        print(f"{error} That space is already taken")
        return enter_move(board)
    

    board[row][col] = player_mark
    return board
    


def make_list_of_free_fields(board):
    # The function browses the board and builds a list of all the free squares; 
    # the list consists of tuples, while each tuple is a pair of row and column numbers.

    free_spaces = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                free_spaces.append([r,c])
    
    return free_spaces

def victory_for(board, sign):
    # The function analyzes the board's status in order to check if 
    # the player using 'O's or 'X's has won the game
    
    # gonna try to do this a weird way but at least i wont type a thousand if statments
    victory_pattern = [sign for x in range(3)]

    left_and_rights = []
    ups_and_downs = []
    diagonals = []

    for r in range(3):
        left_and_rights.append(board[r])

        current_col = []
        for x in range(3):
            current_col.append(board[x][r])

        ups_and_downs.append(current_col)
        current_col = []
    
    diagonal_right = []
    diagonal_left = []
    for r in range(3):
        diagonal_right.append(board[r][r])
        diagonal_left.append(board[r][abs(r-2)])
    
    diagonals = [diagonal_right, diagonal_left]

    if (victory_pattern in diagonals) or (victory_pattern in ups_and_downs) or (victory_pattern in left_and_rights):
        return True
    else:
        return False


def draw_move(board):
    # The function draws the computer's move and updates the board.
    free_spaces = make_list_of_free_fields(board)

    if len(free_spaces) > 0:
        r, c = random.choice(free_spaces)

        board[r][c] = computer_mark

        return board
    else:
        return -1

board = [[0,0,0], [0,computer_mark,0], [0,0,0]]
playing = True 

# main part of program
while playing:

    if len(make_list_of_free_fields(board)) <= 0:
        playing = False
        break

    display_board(board)
    board = enter_move(board)
    board = draw_move(board)

    player_win = victory_for(board,player_mark)
    computer_win = victory_for(board,computer_mark)

    if player_win == True or computer_win == True:
        playing = False

    print("===================================================\n")

os.system('')
display_board(board)
print("")

if player_win == True:
    print("The player wins!")
elif computer_win == True:
    print("The computer wins!")
else:
    print("It is a draw...")

input("Press enter to terminate")