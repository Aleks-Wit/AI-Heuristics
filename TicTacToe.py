'''
Tic Tac Toe
This is a scalable n x n game of tic tac toe. 
At the start, the player chooses a board size between 3 and 100 inclusive.
Then the player chooses whether to play against an AI or watch two AI players compete.
The AI uses simple heuristics, making it both defensive and offensive.
In human vs AI mode, winning, losing, and draw conditions are represented with ASCII art;
In AI vs AI mode, only draws are accompanied by ASCII art.
The game ends when a player wins or the game is a draw.
The player is asked if they want to play again at the end of each game.

Name: Aleksandra Witkowska
'''

import numpy as np #making the game more efficient and concise
import random #to help randomize AI moves
import time #to make ai moves more natural

'''
List of Functions for Tic Tac Toe Game
'''

#ask the player for board size and verify it is an integer greater than 2
def get_board_size():
    while True:
        try:
            size = int(input("Please enter your board size between 3 and 100 (3 for 3x3, 4 for 4x4, etc...): "))
            if size >= 3 and size <= 100:
                return size
            else:
                print("Please enter a number between 3 and 100, inclusive.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

#determine if you want the game to be human vs. ai or ai vs ai
def get_game_mode():
    while True:
        print("Choose game mode:")
        print("1. Play as a human vs AI")
        print("2. Watch two AI play")
        
        choice = input("Enter 1 or 2: ")
        if choice == '1':
            return "human_vs_ai"
        elif choice == '2':
            return "ai_vs_ai"
        else:
            print("Invalid choice, please try again.")

#creating n x n board filled with spaces ' ' which represent empty cells
def create_board(size):
    return np.full((size, size), ' ')

#these are the hash lines in the board
def display_board(board):
    board_size = len(board)

    #print the column numbers at the top and column indices
    print("   " + "   ".join([str(i) for i in range(board_size)]))

    #print row numbers on the side for each row
    for i, row in enumerate(board):
        print(f"{i}  " + ' | '.join(row))
        if i < len(board) - 1: #only print between rows, not last
            print("   "+ '-' * (len(row) * 4 - 1))  #divider line between rows
    print("\n" * 2)  #print two empty lines to add space between turns

#how moves are made
def make_move(board, row, col, player):
    if board[row, col] == ' ': #checks for empty cell
        board[row, col] = player #places player's mark
        return True #valid move
    else:
        print("The cell is already taken.")
        return False  #invalid move

#move selection validation
def get_valid_move(board, board_size):
    while True:
        try:
            #asks for row and column input
            row, col = map(int, input("Enter row and column with one space between the two: ").split())

            #check if input is within parameters
            if row < 0 or row >= board_size or col < 0 or col >= board_size:
                print(f"Invalid move! Row and column must be between 0 and {board_size - 1}.")
            elif board[row, col] != ' ': #checks if the cell is already taken
                print("Invalid move! That spot is already taken.")
            else:
                return row, col #valid move
        except ValueError: #don't mess with my code
            print("Invalid input! Please enter two integers separated by a space.")

#check for row win
def check_row_win(board, player):
    return np.any(np.all(board == player, axis=1))

#check for column win
def check_column_win(board, player):
    return np.any(np.all(board == player, axis=0))

#check for diagonal win
def check_diagonal_win(board, player):
    #check main diagonal
    main_diag = np.all(np.diag(board) == player)
    
    #check anti-diagonal
    anti_diag = np.all(np.diag(np.fliplr(board)) == player)
    
    return main_diag or anti_diag

#check for a draw
def is_board_full(board):
    return not np.any(board == ' ') #returns True if no empty cells remain

#defensive AI
def find_near_winning_move(board, player, n):
    for row in range(n): #check for n-1 in rows
        if np.sum(board[row, :] == player) == n - 1 and np.any(board[row, :] == ' '):
            empty_col = np.where(board[row, :] == ' ')[0][0]
            return row, empty_col

    for col in range(n): #check for n-1 in columns
        if np.sum(board[:, col] == player) == n - 1 and np.any(board[:, col] == ' '):
            empty_row = np.where(board[:, col] == ' ')[0][0]
            return empty_row, col
    
    #check for n-1 in diagonal
    if np.sum(np.diag(board) == player) == n - 1 and np.any(np.diag(board) == ' '):
        empty_diag = np.where(np.diag(board) == ' ')[0][0]
        return empty_diag, empty_diag

    #check for n-1 in anti-diagonal
    if np.sum(np.diag(np.fliplr(board)) == player) == n - 1 and np.any(np.diag(np.fliplr(board)) == ' '):
        empty_anti_diag = np.where(np.diag(np.fliplr(board)) == ' ')[0][0]
        return empty_anti_diag, n - empty_anti_diag - 1

    return None #no near-winning move found

def smart_ai_move(board, player, opponent, n):
    time.sleep(0.7) #short paus before AI moves
    #offensive move: AI tries to win first
    move = find_near_winning_move(board, player, n)
    if move:
        make_move(board, move[0], move[1], player)
        return

    #defensive move: AI blocks opponent's win
    move = find_near_winning_move(board, opponent, n)
    if move:
        make_move(board, move[0], move[1], player)
        return
    
    #fallback to random move
    random_ai_move(board, player)

#simple AI random move assignment
def random_ai_move(board, player):
    empty_cells = np.argwhere(board == ' ') #argwhere finds all empty cells
    empty_cells = [tuple(cell) for cell in empty_cells]#convert numpy array to a list of tuples
    if empty_cells: #checks for empty cells
        move = random.choice(empty_cells)
        make_move(board, move[0], move[1], player)

#champion
def display_trophy():
    print("\n" + " " * 10 + "CONGRATULATIONS!".center(30))
    print(" " * 5 + "You are the ultimate champion!".center(40))
    print(" " * 5 + "Here's your well-deserved trophy:".center(40))
    trophy = """
              .-=========-.
               '-=======-'
              _|   .=.   |_
             ((|   [#1]  |))
              \|   /|\   |/
               \__ '`' __/
                 _`) (`_
               _/_______\_
              |___________|

       """
    print(trophy)

def display_loser():
    loser = """
┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
███▀▀▀██┼███▀▀▀███┼███▀█▄█▀███┼██▀▀▀
██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼█┼┼┼██┼██┼┼┼
██┼┼┼▄▄▄┼██▄▄▄▄▄██┼██┼┼┼▀┼┼┼██┼██▀▀▀
██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██┼┼┼
███▄▄▄██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██▄▄▄
┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
███▀▀▀███┼▀███┼┼██▀┼██▀▀▀┼██▀▀▀▀██▄┼
██┼┼┼┼┼██┼┼┼██┼┼██┼┼██┼┼┼┼██┼┼┼┼┼██┼
██┼┼┼┼┼██┼┼┼██┼┼██┼┼██▀▀▀┼██▄▄▄▄▄▀▀┼
██┼┼┼┼┼██┼┼┼██┼┼█▀┼┼██┼┼┼┼██┼┼┼┼┼██┼
███▄▄▄███┼┼┼─▀█▀┼┼─┼██▄▄▄┼██┼┼┼┼┼██▄
┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼██┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼██┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼████▄┼┼┼▄▄▄▄▄▄▄┼┼┼▄████┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼┼▀▀█▄█████████▄█▀▀┼┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼┼┼┼█████████████┼┼┼┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼┼┼┼██▀▀▀███▀▀▀██┼┼┼┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼┼┼┼██┼┼┼███┼┼┼██┼┼┼┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼┼┼┼█████▀▄▀█████┼┼┼┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼┼┼┼┼███████████┼┼┼┼┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼▄▄▄██┼┼█▀█▀█┼┼██▄▄▄┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼▀▀██┼┼┼┼┼┼┼┼┼┼┼██▀▀┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼┼┼▀▀┼┼┼┼┼┼┼┼┼┼┼▀▀┼┼┼┼┼┼┼┼┼┼┼
┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
"""
    print(loser)
    print("The only winning move is not to play.")

def display_draw():
    print("""
    ________
    |      | 
    |  DRAW! 
    |______|
    """)

'''
Tic Tac Toe Main Game Loop
'''

#new board creation and players
def play_game():
    print("Welcome to Aleksandra's Tic Tac Toe Game!" "\n"
          "***** Have fun! *****")
    
    while True:  #loops for repeating the game
        board_size = get_board_size() #asks user for board size
        board = create_board(board_size) #creates a board size based on user input
        players = ['X', 'O']
        current_player = 0
        game_over = False  #game_over flag to control when the game ends


        #get the game mode from player
        game_mode = get_game_mode()    
        
        while not game_over:
            display_board(board)
            
            if game_mode == "human_vs_ai": #human player
                if current_player == 0:
                    row, col = get_valid_move(board, board_size) #calling validation function
                    if make_move(board, row, col, players[current_player]):
                        if check_row_win(board, players[current_player]) or \
                        check_column_win(board, players[current_player]) or \
                        check_diagonal_win(board, players[current_player]):
                            display_board(board)
                            print(f"Player {players[current_player]} wins!")
                            display_trophy()  #shows ASCII trophy when the human wins
                            break
                        elif is_board_full(board):
                            display_board(board)
                            print("It's a draw! Better luck next time.")
                            display_draw()
                            break
                        current_player = (current_player + 1) % 2 #using modulo operator to determine player turn

                else: #ai player's turn
                    smart_ai_move(board, players[current_player], players[(current_player + 1) % 2], board_size)
                    if check_row_win(board, players[current_player]) or \
                    check_column_win(board, players[current_player]) or \
                    check_diagonal_win(board, players[current_player]):
                        display_board(board)
                        print(f"Player {players[current_player]} wins!")
                        display_loser() #shows the game over losing ascii to the human player
                        break
                    elif is_board_full(board):
                            display_board(board)
                            print("It's a draw! Better luck next time.")
                            display_draw()
                            break
                    current_player = (current_player + 1) % 2 #switch to human player
        
            elif game_mode == "ai_vs_ai": #no humans
                smart_ai_move(board, players[current_player], players[(current_player + 1) % 2], board_size)
                if check_row_win(board, players[current_player]) or \
                check_column_win(board, players[current_player]) or \
                check_diagonal_win(board, players[current_player]):
                    display_board(board)
                    print(f"AI Player {players[current_player]} wins!")
                    break
                elif is_board_full(board):
                    display_board(board)
                    print("It's a draw!") #the only acii i'm giving the ai
                    display_draw()
                    break
                current_player = (current_player + 1) % 2
            
        play_again = input("Would you like to play another game? (yes/no): ").lower()
        if play_again != 'yes' and play_again != 'y':  #exit the loop if not "yes"
            print("Thanks for playing. See you next time.")
            break

if __name__ == "__main__":
    play_game() #executes the game
