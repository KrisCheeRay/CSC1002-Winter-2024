import random

def display_introductions():
    """Display an introduction message to the player about the game."""
    
    print("Welcome to Dylan's 8-tile puzzle game, you will be prompted to solve a shuffled 8-tile puzzle. Hope you enjoy it!")
    print("You will enter four letters to use for moving tiles left, right, up, and down.")


def get_valid_moves() -> tuple[str, str, str, str]:
    """
    Prompt the player to enter four unique letters representing moves.
    
    Validates the input to ensure it consists of four unique alphabetic characters.
    Returns a tuple of the characters representing left, right, up, and down moves.
    """
    
    while True:
        user_input = input("Enter 4 letters (a-z) for left, right, up, down moves > ").lower().replace(" ", "")
        if len(user_input) == 4 and len(set(user_input)) == 4 and user_input.isalpha():
            return user_input[0], user_input[1], user_input[2], user_input[3]
        else:
            print("Invalid input. Please ensure four unique letters, no repetitions or non-letter characters.")


def initialize_chessboard() -> list[int, str]:
    """
    Initialize and return a solvable 8-tile puzzle chessboard.
    
    The chessboard is a list with numbers 1 through 8 and a blank space represented by ' '.
    The function ensures the generated chessboard is solvable for the user.
    """
    
    chessboard = list(range(1, 9)) + [' ']
    random.shuffle(chessboard)
    while not is_solvable(chessboard):
        random.shuffle(chessboard)
    return chessboard


def is_solvable(chessboard: list[str, int]) -> bool:
    """
    Check if a given chessboard configuration is solvable for the user.
    
    Counts the total number of inversions in the chessboard. A solvable configuration
    has an even number of inversions.
    """
    
    inversion_count = 0
    for i in range(len(chessboard)):
        for j in range(i + 1, len(chessboard)):
            if chessboard[i] != ' ' and chessboard[j] != ' ' and chessboard[i] > chessboard[j]:
                inversion_count += 1
    return inversion_count % 2 == 0


def get_possible_moves(index: int) -> list[str]:
    """
    Determine the possible moves based on the empty tile's position.
    
    Returns a list of possible moves ('left', 'right', 'up', 'down') depending on where
    the empty tile (' ') is located on the chessboard.
    """
    
    moves = {'left': index % 3 != 0, 'right': index % 3 != 2, 'up': index >= 3, 'down': index < 6}
    possible_moves = [k for k, v in moves.items() if v]
    return possible_moves


def print_chessboard(chessboard: list[str, int]):
    """Print the current state of the chessboard."""
    
    for i in range(0, 9, 3):
        print(f"{chessboard[i]} {chessboard[i+1]} {chessboard[i+2]}")


def move_tile(chessboard: list, move: str, moves: tuple[str, str, str, str]):
    """
    Move a tile based on the player's input, adjusting the logic to reflect the movement of numbers towards the specified direction.
    """
    
    index = chessboard.index(' ')
    move_direction = moves.index(move)

    # Mapping the index of the move to the actual direction
    if move_direction == 0:  # Left
        target_index = index + 1
    elif move_direction == 1:  # Right
        target_index = index - 1
    elif move_direction == 2:  # Up
        target_index = index + 3
    elif move_direction == 3:  # Down
        target_index = index - 3

    # Make sure that the target index is within the bounds of the chessboard and the move is valid
    if 0 <= target_index < len(chessboard) and (target_index // 3 == index // 3 or target_index % 3 == index % 3):
        chessboard[index], chessboard[target_index] = chessboard[target_index], chessboard[index]
    else:
        print("Invalid move. Please follow the prompt and try again.")


def is_solved(chessboard: list[str, int]) -> bool:
    """
    Check if the current chessboard configuration matches the solved state.
    
    A solved chessboard has tiles in numerical order with the blank space at the end.
    """
    
    return chessboard == list(range(1, 9)) + [' ']


def ask_for_next_round(moves: tuple[str, str, str, str]):
    """Prompt the player to play another game or quit."""
    
    while True:
        decision = input('Enter "n" for another game, or "q" to end the game > ').lower()
        if decision == 'n':
            play_game(moves)
            break
        elif decision == 'q':
            print("Thanks for playing Dylan's 8-tile puzzle game!")
            break
        else:
            print("Invalid input. Please enter 'n' to start another game or 'q' to end the game.")


def play_game(moves: tuple[str, str, str, str]):
    """
    Main game loop.
    
    Initializes the chessboard, processes player moves, and checks for game completion.
    Prompts the player for moves until the puzzle is solved, then offers a new game or exit.
    """
    
    chessboard = initialize_chessboard()
    move_count = 0

    while not is_solved(chessboard):
        print_chessboard(chessboard)
        index = chessboard.index(' ')
        possible_moves = get_possible_moves(index)

        # Adjusting move prompts based on the position of the blank space and the fact that players move numbers
        available_moves_prompt = []
        if 'right' in possible_moves and index % 3 != 2:  # Can move number to the left, blank moves right
            available_moves_prompt.append(f"left-{moves[0]}")
        if 'left' in possible_moves and index % 3 != 0:  # Can move number to the right, blank moves left
            available_moves_prompt.append(f"right-{moves[1]}")
        if 'down' in possible_moves and index < 6:  # Can move number up, blank moves down
            available_moves_prompt.append(f"up-{moves[2]}")
        if 'up' in possible_moves and index >= 3:  # Can move number down, blank moves up
            available_moves_prompt.append(f"down-{moves[3]}")

        move_prompt = ", ".join(available_moves_prompt)

        move = input(f"Enter your move ({move_prompt})> ").lower()
        chessboard_before_move = chessboard[:]  # Copy the chessboard before attempting the move
        if move in moves:
            move_tile(chessboard, move, moves)
            if chessboard_before_move != chessboard:  # Check if the move was valid
                move_count += 1
            else:
                print("Invalid move. That direction is not possible from the current position.")
        else:
            print("Invalid move. Please follow the prompt and try again.")

        print()

    print_chessboard(chessboard)
    print(f"Congratulations! You have solved the puzzle in {move_count} moves!")
    ask_for_next_round(moves)

def main():
    """Run the game."""
   
    display_introductions()
    moves = get_valid_moves()
    play_game(moves)

if __name__ == "__main__":
    main()
