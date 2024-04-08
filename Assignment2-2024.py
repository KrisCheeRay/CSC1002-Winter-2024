import turtle
import random
import numpy as np

#Constants for the game's design
BOARD_SIZE = 0  
EMPTY_TILE = (0, 0)    
TILES = np.array([])
#Setting up the turtle screen for the users
t = turtle.Turtle()
screen = turtle.Screen()
t.speed(0)
t.hideturtle()

def initial_game()-> None:
    """
    Initializes the sliding puzzle game.

    This function sets up the game window, prompts the user for the puzzle's dimensions,
    generates a solvable puzzle, and draws the initial puzzle configuration.

    Parameters:
    None

    Returns:
    None
    """
    global BOARD_SIZE, TILES, color
    color = 'Pale Green'  
    screen.setup(width=600, height=600)
    turtle.title("Dylan's Sliding Puzzle Game")
    BOARD_SIZE = screen.numinput("Dylan's Sliding Puzzle Game", "Enter the puzzle's dimensions (3, 4, 5):", default=3, minval=3, maxval=5)
    if BOARD_SIZE is not None:
        BOARD_SIZE = int(BOARD_SIZE)  
        TILES = np.arange(BOARD_SIZE ** 2).reshape((BOARD_SIZE, BOARD_SIZE))
        generate_solvable_puzzle(BOARD_SIZE)
        draw_puzzle()
    else:
        turtle.bye()

def generate_move() -> list[int, int]:
    """
    Generates a random move in the form of a tuple (x_dir, y_dir).

    Returns:
        list[int, int]: A list containing the x and y directions of the move.
    """
    x_dir, y_dir = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
    return x_dir, y_dir

def execute_move(x_dir: int, y_dir: int) -> None:
    """
    Executes a move in the sliding puzzle game.

    This function takes the x and y directions of the move and updates the puzzle configuration accordingly.

    Parameters:
    x_dir (int): The x direction of the move.
    y_dir (int): The y direction of the move.

    Returns:
    None
    """
    global BOARD_SIZE, TILES, EMPTY_TILE 
    new_blank_pos = (EMPTY_TILE[0] + y_dir, EMPTY_TILE[1] + x_dir)
    if 0 <= new_blank_pos[0] < BOARD_SIZE and 0 <= new_blank_pos[1] < BOARD_SIZE:
        swap_TILES(EMPTY_TILE, new_blank_pos)
        EMPTY_TILE = new_blank_pos

def shuffle_puzzle(steps: int = 75) -> None:
    """
    Shuffles the puzzle by executing a series of random moves.

    This function takes an optional parameter 'steps' which determines the number of random moves to execute.
    Each move is generated using the 'generate_move' function and executed using the 'execute_move' function.

    Parameters:
    steps (int): The number of random moves to execute. Default is 75.

    Returns:
    None
    """
    for _ in range(steps):
        x_dir, y_dir = generate_move()
        execute_move(x_dir, y_dir)

def generate_solvable_puzzle(size: int) -> None:
    """
    Generates a solvable puzzle of the given size.

    This function takes the size of the puzzle as input and generates a solvable puzzle configuration.
    The puzzle configuration is stored in the global variable TILES.

    Parameters:
    size (int): The size of the puzzle.

    Returns:
    None
    """
    puzzle = np.arange(size ** 2).reshape((size, size))
    shuffle_puzzle()

def determine_direction(pos_1: tuple[int, int], pos_2: tuple[int, int]) -> str:
    """
    Determines the direction between two positions in the sliding puzzle game.

    This function takes two positions as input and returns the direction ('up', 'down', 'left', 'right')
    in which pos_2 is relative to pos_1.

    Parameters:
    pos_1 (tuple[int, int]): The first position.
    pos_2 (tuple[int, int]): The second position.

    Returns:
    str: The direction between the two positions.
    """
    direction = ''
    if pos_1[0] == pos_2[0]:
        direction = 'right' if pos_1[1] > pos_2[1] else 'left'
    elif pos_1[1] == pos_2[1]:
        direction = 'down' if pos_1[0] > pos_2[0] else 'up'
    return direction

def perform_swap(pos_1: tuple[int, int], pos_2: tuple[int, int]) -> None:
    """
    Swaps the values of two positions in the TILES array.

    This function takes two positions as input and swaps the values of those positions in the TILES array.

    Parameters:
    pos_1 (tuple[int, int]): The first position.
    pos_2 (tuple[int, int]): The second position.

    Returns:
    None
    """
    temp = TILES[pos_1[0]][pos_1[1]]
    TILES[pos_1[0]][pos_1[1]] = TILES[pos_2[0]][pos_2[1]]
    TILES[pos_2[0]][pos_2[1]] = temp

def swap_TILES(pos_1: tuple[int, int], pos_2: tuple[int, int]) -> str:
    """
    Swaps the values of two positions in the TILES array and returns the direction of the swap.

    This function takes two positions as input and swaps the values of those positions in the TILES array.
    It also determines the direction of the swap based on the positions.

    Parameters:
    pos_1 (tuple[int, int]): The first position.
    pos_2 (tuple[int, int]): The second position.

    Returns:
    str: The direction of the swap ('up', 'down', 'left', 'right').
    """
    direction = determine_direction(pos_1, pos_2)
    perform_swap(pos_1, pos_2)
    return direction

def check_ifsolved() -> bool:
    """
    Checks if the puzzle is solved.

    This function compares the current puzzle configuration with the solution configuration
    and returns True if they are equal, indicating that the puzzle is solved.

    Returns:
        bool: True if the puzzle is solved, False otherwise.
    """
    solution = np.arange(1, BOARD_SIZE ** 2)
    solution = np.append(solution, 0).reshape((BOARD_SIZE, BOARD_SIZE))
    return np.array_equal(TILES, solution)

def check_solved_and_notify() -> None:
    """
    Checks if the puzzle is solved and notifies the user.

    This function checks if the puzzle is solved by calling the 'check_ifsolved' function.
    If the puzzle is solved, it updates the color of the puzzle, redraws the puzzle, and displays a congratulatory message.

    Parameters:
    None

    Returns:
    None
    """
    if check_ifsolved():
        global color, t
        color = 'red'
        draw_puzzle()
        turtle.tracer(1, 10)
        t.penup()
        t.color("black")
        t.goto(0, 0)
        t.write("Congratulations!", align="center", font=("Times", 24, "bold"))
        screen.onclick(None)


def draw_all_TILES() -> None:
    """
    Draws all the tiles on the puzzle board.

    This function iterates over the TILES array and calls the draw_tile function for each tile.

    Parameters:
    None

    Returns:
    None
    """
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            draw_tile(i, j, TILES[i, j])

def draw_puzzle(tile=None,direction=None) -> None:
    """
    Draws the puzzle board.

    This function draws the puzzle board by calling the 'draw_all_TILES' function.
    If 'tile' and 'direction' are provided, it animates the movement of the tile.

    Parameters:
    tile ([int]): The number of the tile to animate. Default is None.
    direction ([str]): The direction of the tile movement. Default is None.

    Returns:
    None
    """
    turtle.tracer(0, 0)
    t.clear()
    if tile and direction:
        animate_tile_movement(tile, direction)
    else:
        draw_all_TILES()
    turtle.update()

def take_tile_positition(row: int, col: int, additional_offset: tuple[int, int] = (0, 0)) -> tuple[int, int, int]:
    """
    Calculates the position and size of a tile on the puzzle board.

    This function takes the row and column indices of a tile, along with an optional additional offset,
    and calculates the x and y coordinates of the tile's top-left corner, as well as the size of the tile.

    Parameters:
    row (int): The row index of the tile.
    col (int): The column index of the tile.
    additional_offset (tuple[int, int]): An optional additional offset for the tile position. Default is (0, 0).

    Returns:
    tuple[int, int, int]: A tuple containing the x and y coordinates of the tile's top-left corner, and the size of the tile.
    """
    tile_size = 600 // BOARD_SIZE
    draw_size = tile_size - 8
    x = col * tile_size - 300 + 4 + additional_offset[0]
    y = 300 - row * tile_size - 4 + additional_offset[1]
    return x, y, draw_size

def draw_square(x: int, y: int, draw_size: int) -> None:
    """
    Draws a square on the turtle canvas.

    This function takes the x and y coordinates of the top-left corner of the square,
    as well as the size of the square, and draws it on the turtle canvas.

    Parameters:
    x (int): The x coordinate of the top-left corner of the square.
    y (int): The y coordinate of the top-left corner of the square.
    draw_size (int): The size of the square.

    Returns:
    None
    """
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(draw_size)
        t.right(90)
    t.end_fill()

def write_number(x: int, y: int, draw_size: int, number: int) -> None:
    """
    Writes the number on the tile.

    This function takes the x and y coordinates of the top-left corner of the tile,
    the size of the tile, and the number to be written.
    It writes the number on the tile using the turtle graphics library.

    Parameters:
    x (int): The x coordinate of the top-left corner of the tile.
    y (int): The y coordinate of the top-left corner of the tile.
    draw_size (int): The size of the tile.
    number (int): The number to be written.

    Returns:
    None
    """
    t.penup()
    t.goto(x + draw_size / 2, y - draw_size / 2 - 20)
    t.write(number, align="center", font=("Times", 18, "normal"))

def draw_tile(row: int, col: int, number: int, additional_offset: tuple[int, int] = (0, 0)) -> None:
    """
    Draws a tile on the puzzle board.

    This function takes the row and column indices of the tile, the number to be drawn on the tile,
    and an optional additional offset, and draws the tile on the puzzle board.

    Parameters:
    row (int): The row index of the tile.
    col (int): The column index of the tile.
    number (int): The number to be drawn on the tile.
    additional_offset (tuple[int, int]): An optional additional offset for the tile position. Default is (0, 0).

    Returns:
    None
    """
    x, y, draw_size = take_tile_positition(row, col, additional_offset)
    if number > 0:
        draw_square(x, y, draw_size)
        write_number(x, y, draw_size, number)

def check_tile_click(x: int, y: int) -> None:
    """
    Checks if a tile is clicked and performs the necessary actions.

    This function takes the x and y coordinates of the click and determines the row and column indices of the clicked tile.
    It then checks if the clicked tile can be swapped with the empty tile and performs the swap if possible.
    After the swap, it updates the puzzle board and checks if the puzzle is solved.

    Parameters:
    x (int): The x coordinate of the click.
    y (int): The y coordinate of the click.

    Returns:
    None
    """
    global EMPTY_TILE
    tile_size = 600 // BOARD_SIZE
    row = int((300 - y) // tile_size)
    col = int((x + 300) // tile_size)
    clicked_number = TILES[row, col]
    if (abs(EMPTY_TILE[0] - row) == 1 and EMPTY_TILE[1] == col) or \
            (abs(EMPTY_TILE[1] - col) == 1 and EMPTY_TILE[0] == row):
        direction = swap_TILES(EMPTY_TILE, (row, col))
        EMPTY_TILE = (row, col)
        draw_puzzle(clicked_number, direction)
        check_solved_and_notify()

def animate_tile_movement(tile_number: int, direction: str) -> None:
    """
    Animates the movement of a tile on the puzzle board.

    This function takes the tile number and the direction of the movement as input.
    It animates the movement of the tile by redrawing the puzzle board with the tile in its new position.

    Parameters:
    tile_number (int): The number of the tile to animate.
    direction (str): The direction of the tile movement.

    Returns:
    None
    """
    steps: int = 10
    tile_size: int = 600 // BOARD_SIZE
    x_dir: float = tile_size / steps
    y_dir: float = tile_size / steps
    for step in range(steps):
        t.clear()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if TILES[i, j] == tile_number:
                    if direction == "up":
                        draw_tile(i, j, tile_number, additional_offset=(0, y_dir * step - tile_size))
                    elif direction == "down":
                        draw_tile(i, j, tile_number, additional_offset=(0, -y_dir * step + tile_size))
                    elif direction == "right":
                        draw_tile(i, j, tile_number, additional_offset=(x_dir * step - tile_size, 0))
                    elif direction == "left":
                        draw_tile(i, j, tile_number, additional_offset=(-x_dir * step + tile_size, 0))
                else:
                    draw_tile(i, j, TILES[i, j])
        turtle.update()
    t.clear()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            draw_tile(i, j, TILES[i, j])
    turtle.update()

def main() -> None:
    """
    The main function of the program.

    This function initializes the game, sets up the click event handler, and starts the turtle main loop.

    Parameters:
    None

    Returns:
    None
    """
    initial_game()
    screen.onclick(check_tile_click)
    turtle.mainloop()


if __name__ == "__main__":
    main()
