import random
import time
import os

# Loads the board from "gameboard.txt"
def load_board(filename="gameboard.txt"):
    with open(filename, encoding='utf8') as file_object:
        board = file_object.readlines()
    return board

# Saves the current state of the board to "gameboard.txt"
def save_board(board, filename="gameboard.txt"):
    with open(filename, "w") as file:
        file.writelines(board)

# Displays the current state of the board with screen clearing
def display_board(board, message=""):
    os.system('cls' if os.name == 'nt' else 'clear')
    if message:
        print(message)
    for line in board:
        print(line, end='')
    print("\n")

# Defines section and cell coordinates based on layout in gameboard.txt
section_coordinates = {
    'A': (1, 4), 'B': (1, 16), 'C': (1, 28),
    'D': (13, 4), 'E': (13, 16), 'F': (13, 28),
    'G': (25, 4), 'H': (25, 16), 'I': (25, 28)
}

# Cell offsets within each mini-board
cell_offsets = {
    1: (0, 1), 2: (0, 7), 3: (0, 13),
    4: (4, 1), 5: (4, 7), 6: (4, 13),
    7: (8, 1), 8: (8, 7), 9: (8, 13)
}

# Stores the status of each mini-board
mini_board_status = {section: None for section in section_coordinates.keys()}

# Game instructions and introduction
def start_game():
    print("Welcome to Ultimate Tic-Tac-Toe!")
    print("Game by Dasha")
    print("Instructions:")
    print("- This game is played against a bot.")
    print("- Choose a section (A-I) and a cell (1-9) to make your move.")
    print("- Each section is a smaller Tic-Tac-Toe game. Win three in a row to win a section!")
    print("- When a player wins a section, that section is claimed with their symbol and locked from further moves.")
    print("- The goal is to win three sections in a row on the big board.")
    print("Difficulty levels:")
    print("- Easy: Bot makes random moves.")
    print("- Hard: Bot will try to block your moves.")
    input("\nType OK and press Enter to start the game.")
    os.system('cls' if os.name == 'nt' else 'clear')

# Choose difficulty level
def choose_difficulty():
    while True:
        difficulty = input("Choose difficulty level - Easy or Hard (E/H): ").upper()
        if difficulty in ['E', 'H']:
            return 'hard' if difficulty == 'H' else 'easy'
        print("Invalid choice. Please enter E or H.")

# Easy bot move function
def easy_bot(board):
    available_sections = [sec for sec, status in mini_board_status.items() if status is None]
    if not available_sections:
        return None  # No available sections to play
    section = random.choice(available_sections)
    available_cells = [
        pos for pos in range(1, 10)
        if board[get_cell_coordinates(section, pos)[0]][get_cell_coordinates(section, pos)[1]] not in ['X', 'O']
    ]
    if not available_cells:
        return None
    cell = random.choice(available_cells)
    return section, cell

# Hard bot move function with winning and blocking strategy
def hard_bot(board):
    bot = 'O'
    opponent = 'X'
    available_sections = [sec for sec, status in mini_board_status.items() if status is None]

    # Step 1: Check if bot can win in any available section
    for section in available_sections:
        for combo in winning_combinations:
            bot_cells = [
                pos for pos in combo
                if board[get_cell_coordinates(section, pos)[0]][get_cell_coordinates(section, pos)[1]] == bot
            ]
            empty_cells = [
                pos for pos in combo
                if board[get_cell_coordinates(section, pos)[0]][get_cell_coordinates(section, pos)[1]] not in ['X', 'O']
            ]
            if len(bot_cells) == 2 and len(empty_cells) == 1:
                # Win by taking the third cell
                return section, empty_cells[0]

    # Step 2: Check if bot can block the player in any available section
    for section in available_sections:
        for combo in winning_combinations:
            player_cells = [
                pos for pos in combo
                if board[get_cell_coordinates(section, pos)[0]][get_cell_coordinates(section, pos)[1]] == opponent
            ]
            empty_cells = [
                pos for pos in combo
                if board[get_cell_coordinates(section, pos)[0]][get_cell_coordinates(section, pos)[1]] not in ['X', 'O']
            ]
            if len(player_cells) == 2 and len(empty_cells) == 1:
                # Block the player by taking the third cell
                return section, empty_cells[0]

    # Step 3: If no win or block is needed, make a random move (like easy_bot)
    return easy_bot(board)

# These are the winning combinations for mini-boards
winning_combinations = [
    (1, 2, 3), (4, 5, 6), (7, 8, 9),
    (1, 4, 7), (2, 5, 8), (3, 6, 9),
    (1, 5, 9), (3, 5, 7)
]

def get_cell_coordinates(section, cell):
    section_to_position = {
        'A': (1, 0), 'B': (1, 4), 'C': (1, 8),
        'D': (5, 0), 'E': (5, 4), 'F': (5, 8),
        'G': (9, 0), 'H': (9, 4), 'I': (9, 8)
    }
    if section not in section_to_position:
        raise ValueError(f"Invalid section: {section}. Choose a letter A-I.")
    if cell < 1 or cell > 9:
        raise ValueError(f"Invalid cell: {cell}. Choose a number 1-9.")
    section_row, section_col = section_to_position[section]
    row = section_row + (cell - 1) // 3
    col = section_col + (cell - 1) % 3
    return row, col

def make_move(board, section, cell, player):
    if mini_board_status[section]:  # Checks if the section is already won
        return f"Section {section} is already won by {mini_board_status[section]}."
    row, col = get_cell_coordinates(section, cell)
    if board[row][col] in ['X', 'O']:  # Cell already taken
        return "This cell is already taken."
    board[row] = board[row][:col] + player + board[row][col+1:]
    save_board(board)  # Saves board after each move
    if check_win(board, section, player):  # Checks if the section is won
        mini_board_status[section] = player  # Marks section as won by the player
        for pos in range(1, 10):  # Marks the entire section with the winner's symbol
            row, col = get_cell_coordinates(section, pos)
            board[row] = board[row][:col] + player + board[row][col+1:]
    return None

def check_win(board, section, player):
    for combo in winning_combinations:
        if all([
            board[get_cell_coordinates(section, pos)[0]][get_cell_coordinates(section, pos)[1]] == player
            for pos in combo
        ]):
            return True
    return False

def check_game_winner():
    winning_sections = [
        ('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', 'I'),
        ('A', 'D', 'G'), ('B', 'E', 'H'), ('C', 'F', 'I'),
        ('A', 'E', 'I'), ('C', 'E', 'G')
    ]
    for combo in winning_sections:
        if all(mini_board_status[section] == 'X' for section in combo):
            return 'X'
        elif all(mini_board_status[section] == 'O' for section in combo):
            return 'O'
    return None

# Main game loop with difficulty selection and replay option
def game_loop():
    while True:  # Main loop to allow replaying the game if the player chooses to
        board = load_board()  # Load a new/clear board for each game
        start_game()
        difficulty = choose_difficulty()
        player = 'X'
        
        while True:  # Game play loop
            display_board(board, f"Player {player}'s turn.")
            
            if player == 'X':
                section = input("Choose a section (A-I): ").upper()
                cell = int(input("Choose a cell (1-9): "))
            else:
                if difficulty == 'easy':
                    move = easy_bot(board)
                else:
                    move = hard_bot(board)
                
                if not move:
                    print("No available moves. It's a draw!")
                    break
                section, cell = move
            
            error_message = make_move(board, section, cell, player)
            if error_message:
                if player == 'X':
                    print(error_message)
                    time.sleep(1)
                continue

            game_winner = check_game_winner()
            if game_winner:
                display_board(board, f"Player {game_winner} wins the game!")
                break

            player = 'O' if player == 'X' else 'X'
        
        # Asks if the player wants to play again
        play_again = input("Would you like to play again? (Y/N): ").upper()
        if play_again != 'Y':
            print("Thank you for playing!")
            break

# Game loop
game_loop()
