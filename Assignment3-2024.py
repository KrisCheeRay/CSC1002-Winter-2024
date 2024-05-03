import turtle
from random import randrange 
from random import sample
# CONSTANTS

HEAD_CURR_POS = [12, 12] # Snake head position
HEAD_TARGET_POS = [] # Snake head target position
SNAKE_TAIL_POS = [] # Snake tail position
SNAKE_TAIL_LENGTH = 0 # Snake tail length
SNAKE_TAIL_DEFAULT = 5 # Snake tail default length
MONSTER_TARGET_POS = [12, 12] # Monster target position
MONSTER_CURR_POS = [] # Monster current position
GAME_TIME = 0 # Game time
GAME_CONTACT = 0 # Game contact
SNAKE_MOTION = 'Paused' # Snake motion
PREVIOUS_MOTION = 'Paused' # Previous motion
SNAKE_SPEED = 250 # Snake speed by default
MONSTER_SPEED = 400 # Monster speed by default
IS_START_TIME = True # Start time flag
IS_END_TIME = False # End time flag
FOOD_TO_EAT = [1, 2, 3, 4, 5] # Food to eat
FOOD_TO_HIDE = [] # Food to hide
ONLY_COUNT = 0 



def setup_screen() -> None:
    '''
    Set up the game screen by creating a turtle screen object.
    Configure the screen size and title. Initializes the game status bar to display game metrics.
    Uses turtle.tracer(0) to turn off animation for manual screen updates.

    Args: None
    Returns: None
    '''
    global game_screen, game_status
    turtle.tracer(0)
    game_screen = turtle.Screen()
    game_screen.setup(width=580, height=660)
    game_screen.title('Hungry Snake By Dylan.CAI')

    game_status = turtle.Turtle()
    game_status.hideturtle()
    game_status.penup()
    game_status.goto(-240, 240)



def setup_snake()-> None:
    '''
    Set up the snake.
    The head of the snake is red and the tail is black.
    The snake head is set to face up.  

    Args: None
    Returns: None
    '''
    
    global snake_head, snake_tail

    
    snake_tail = turtle.Turtle(shape="square") # Set up the snake tail
    snake_tail.color('black')
    snake_tail.hideturtle()
    snake_tail.penup()
    snake_tail.pencolor('blue')
    
    
    snake_head = turtle.Turtle(shape="square") # Set up the snake head
    snake_head.color('red')
    snake_head.setheading(90)  
    snake_head.penup()



def setup_monsters()-> None:
    '''
    Set up the monsters.
    The monsters are purple squares.
    Randomly set the target position of the monsters.
    Ensure that the monsters are not placed in the center of the screen.
    And that the monsters are not placed on top of each other.
    Record the current position of the monsters.

    Args: None
    Returns: None
    '''
    
    global monsters, monster_target_pos, monster_curr_pos
    monsters = []
    monster_target_pos = []
    monster_curr_pos = []
    
    # Set up the monsters
    for _ in range(4):  
        monster = turtle.Turtle(shape='square')
        monster.color('purple')
        monster.penup()
        
        target_pos = [randrange(0, 24), randrange(0, 24)]
        while 7 <= target_pos[0] <= 17 and 7 <= target_pos[1] <= 17:
            target_pos = [randrange(0, 24), randrange(0, 24)]
        
        monsters.append(monster)
        monster_target_pos.append(target_pos)
        monster_curr_pos.append(target_pos)



def refresh_status_bar()-> None:
    '''
    Refresh the game status bar.
    Record the game contact, time, and snake motion.
    Update the game status bar.

    Args: None
    Returns: None
    '''
    
    game_status.clear()
    game_status.write('Contact:' + str(GAME_CONTACT) + ' Time: ' + str(GAME_TIME)+ 's'
                   + ' Motion:' + SNAKE_MOTION, font=('Arial', 16, 'bold'))
    # Update the game status bar


def refresh_time()-> None:
    '''
    Refresh the game time.
    Refresh the game time every second.
    If the game is not paused, increment the game time.
    If the game is over, return.

    Args: None
    Returns: None
    '''
        
    global GAME_TIME
    global IS_START_TIME
    global IS_END_TIME

    # Refresh the game time
    if IS_START_TIME:
        IS_START_TIME = False
        game_screen.ontimer(refresh_time, 1000)
    else:
        if not IS_END_TIME:
            GAME_TIME += 1
            refresh_status_bar()
            game_screen.ontimer(refresh_time, 1000)
        else:
            return


def display_frame()-> None:
    '''
    Display the game frame.
    Set up the game screen frame with a black border.
    Display the game introduction.
    The pen size is set to 2.
    The game screen frame is 500x500.

    Args: None
    Returns: None
    '''
    
    global game_introduction

    # Display the game frame
    game_screen_frame = turtle.Turtle()
    game_screen_frame.hideturtle()
    game_screen_frame.pensize(2)
    game_screen_frame.penup()
    game_screen_frame.goto(-250, -290)
    game_screen_frame.pendown()
    game_screen_frame.fd(500)
    game_screen_frame.left(90)
    game_screen_frame.fd(500)
    game_screen_frame.left(90)
    game_screen_frame.fd(500)
    game_screen_frame.left(90)
    game_screen_frame.fd(500)
    game_screen_frame.penup()
    game_screen_frame.goto(-250, 210)
    game_screen_frame.pendown()
    game_screen_frame.left(180)
    game_screen_frame.fd(80)
    game_screen_frame.right(90)
    game_screen_frame.fd(500)
    game_screen_frame.right(90)
    game_screen_frame.fd(80)

    # Display the game introduction
    game_introduction = turtle.Turtle()
    game_introduction.hideturtle()
    game_introduction.penup()
    game_introduction.goto(-200, 100)
    game_introduction.write('Snake by Dylan.CAI\n\nClick anywhere to start, have fun!', font=('Arial', 18, 'normal'))
    
    # Display the game introduction
    refresh_status_bar()
    game_screen.update()


def display_snake()-> None:
    '''
    Display the snake.
    Set the snake head to the current position.
    Set the snake tail to the current position.
    The tail blocks are displayed as stamps.
    The size of each block is 20x20. 

    Args: None
    Returns: None
    '''
    
    # Display the snake
    snake_head.goto(-240 + HEAD_CURR_POS[0] * 20, -280 + HEAD_CURR_POS[1] * 20)
    
    # Display the snake tail
    for each_block_location in SNAKE_TAIL_POS:
        snake_tail.goto(-240 + each_block_location[0] * 20, -280 + each_block_location[1] * 20)
        snake_tail.stamp()
    game_screen.update()


def display_food()-> None:
    '''
    Display the food.
    Set the food to the current position.
    Randomly set the food position.
    Ensure that the food is not placed in the center of the screen.
    Ensure that the food is not placed on top of each other.
    The format of the food is a number from 1 to 5.
    The font is Arial, size 13, and normal.

    Args: None
    Returns: None
    '''
    
    global food_1
    global food_2
    global food_3
    global food_4
    global food_5

    # Display the food
    food_1 = turtle.Turtle()
    food_1.penup()
    food_1.hideturtle()
    food_1.goto(-240 + food_pos_1[0] * 20, -290 + food_pos_1[1] * 20)
    food_1.write('1', font=('Arial', 13, 'normal'))

    food_2 = turtle.Turtle()
    food_2.penup()
    food_2.hideturtle()
    food_2.goto(-240 + food_pos_2[0] * 20, -290 + food_pos_2[1] * 20)
    food_2.write('2', font=('Arial', 13, 'normal'))

    food_3 = turtle.Turtle()
    food_3.penup()
    food_3.hideturtle()
    food_3.goto(-240 + food_pos_3[0] * 20, -290 + food_pos_3[1] * 20)
    food_3.write('3', font=('Arial', 13, 'normal'))

    food_4 = turtle.Turtle()
    food_4.penup()
    food_4.hideturtle()
    food_4.goto(-240+ food_pos_4[0] * 20, -290 + food_pos_4[1] * 20)
    food_4.write('4', font=('Arial', 13, 'normal'))

    food_5 = turtle.Turtle()
    food_5.penup()
    food_5.hideturtle()
    food_5.goto(-240 + food_pos_5[0] * 20, -290 + food_pos_5[1] * 20)
    food_5.write('5', font=('Arial', 13, 'normal'))


def display_monsters()-> None:
    '''
    Display the monsters.
    Set the monster to the current position.
    The monster use goto to move to the current position.
    
    Args: None
    Returns: None
    '''
    
    for monster, pos in zip(monsters, monster_curr_pos):
        monster.goto(-230 + pos[0] * 20, -270 + pos[1] * 20)
    game_screen.update()



def display_game_over()-> None:
    '''
    Display the game over sign.
    When the game is over, display the game over sign.
    Set the game over sign to red.
    Set the game over sign in the center of the screen.
    The font is Arial, size 18, and bold.
    
    Args: None
    Returns: None
    '''
    
    game_over_sign = turtle.Turtle()
    game_over_sign.penup()
    game_over_sign.hideturtle()
    game_over_sign.pencolor('red')
    
    # Display the game over sign
    game_over_sign.goto(-100,0)
    game_over_sign.write('Game Over!!!', font=('Arial', 18, 'bold'))


def display_game_win()-> None:
    '''
    Display the game win sign.
    When the game is won, display the game win sign.
    Set the game win sign to red.
    The font is Arial, size 18, and bold.
    
    Args: None
    Returns: None
    '''
    
    # Display the game win sign
    game_win_congratulation = turtle.Turtle()
    game_win_congratulation.penup()
    game_win_congratulation.hideturtle()
    game_win_congratulation.pencolor('red')
    game_win_congratulation.goto(-100,0)
    game_win_congratulation.write('Winner!!!', font=('Arial', 18, 'bold'))


def is_food_valid(pos_1, pos_2, pos_3, pos_4, pos_5)-> bool:
    '''
    Check if the food is valid.
    If the food is not placed in the center of the screen and not placed on top of each other, return True.
    Use a list to store the food positions.
    Compare the length of the list with 5.
    
    Args: pos_1, pos_2, pos_3, pos_4, pos_5
    Returns: bool
    '''
    
    # Check if the food is valid
    pos_list = []
    for pos in [pos_1, pos_2, pos_3, pos_4, pos_5]:
        if pos not in pos_list:
            pos_list.append(pos)
    if len(pos_list) == 5 and [12, 12] not in pos_list:
        return True
    else:
        
        return 


def set_food()-> None:
    '''
    Set up the food.
    Set the food positions.
    Use a list to store the food positions.
    Randomly set the food positions.
    Ensure that the food is not placed in the center of the screen.
    Ensure that the food is not placed on top of each other.
    Record the original food positions.
    Set boundary, status bar upper boundary, and game area lower boundary.
    
    Args: None
    Returns: None
    '''
    
    global food_pos_1, food_pos_2, food_pos_3, food_pos_4, food_pos_5
    global original_food_pos_1, original_food_pos_2, original_food_pos_3, original_food_pos_4, original_food_pos_5

    # Set up the food
    boundary = 3 # Boundary
    
    status_bar_upper_boundary = 1 # Status bar upper boundary
    
    game_area_lower_boundary = 3 # Game area lower boundary

    # Set up the food positions
    food_positions = []

    for _ in range(5):
        pos_x = randrange(boundary, 25 - boundary)
        pos_y = randrange(game_area_lower_boundary, 25 - status_bar_upper_boundary)
        food_positions.append([pos_x, pos_y])

    
    food_pos_1, food_pos_2, food_pos_3, food_pos_4, food_pos_5 = food_positions

    # Set up the original food positions
    original_food_pos_1 = list(food_pos_1)
    original_food_pos_2 = list(food_pos_2)
    original_food_pos_3 = list(food_pos_3)
    original_food_pos_4 = list(food_pos_4)
    original_food_pos_5 = list(food_pos_5)

    # Check if the food is valid
    if not is_food_valid(food_pos_1, food_pos_2, food_pos_3, food_pos_4, food_pos_5):
        set_food()  



def set_snake_direction_up()-> None:
    global SNAKE_MOTION
    SNAKE_MOTION = 'Up'

def set_snake_direction_down()-> None:
    global SNAKE_MOTION
    SNAKE_MOTION = 'Down'

def set_snake_direction_left()-> None:
    global SNAKE_MOTION
    SNAKE_MOTION = 'Left'

def set_snake_direction_right()-> None:
    global SNAKE_MOTION
    SNAKE_MOTION = 'Right'


def set_snake_paused()-> None:
    '''
    Set the snake paused.
    If the snake is not paused, set the snake to paused.
    If the snake is paused, set the snake to the previous motion.
    
    Args: None
    Returns: None
    '''
    
    global SNAKE_MOTION
    global PREVIOUS_MOTION
    
    # Set the snake paused
    if SNAKE_MOTION != 'Paused':
        PREVIOUS_MOTION = SNAKE_MOTION
        SNAKE_MOTION = 'Paused'  
    else:
        SNAKE_MOTION = PREVIOUS_MOTION  


def is_snake_movable(target_position):
    '''
    Check if the snake is movable to the target position.
    If the target position is within the bounds of the game screen, return True.
    
    Args: target_position: The target position as a list [x, y]
    Returns: bool indicating if the move is allowed.
    '''
    
    # Allow snake to move anywhere on the board that is within bounds
    return 0 <= target_position[0] <= 24 and 0 <= target_position[1] <= 24

    
def snake_move()-> None:
    '''
    Move the snake.
    Catch the snake motion.
    If the snake is paused, return.
    If the snake is not paused, move the snake.
    Update the snake tail position.
    Expand the snake tail.
    Check if the snake has eaten the food.
    Check if the snake has contacted the monster.
    
    Args: None
    Returns: None
    '''
    
    global SNAKE_MOTION, SNAKE_SPEED, HEAD_TARGET_POS, HEAD_CURR_POS, SNAKE_TAIL_LENGTH, SNAKE_TAIL_POS, SNAKE_TAIL_DEFAULT
    tail_to_expand_pos = [12, 12]

    # Move the snake
    if is_game_over():
        return
    else:
        if SNAKE_MOTION != 'Paused':
            if SNAKE_MOTION == 'Up':
                HEAD_TARGET_POS = [HEAD_CURR_POS[0], HEAD_CURR_POS[1] + 1]
            elif SNAKE_MOTION == 'Down':
                HEAD_TARGET_POS = [HEAD_CURR_POS[0], HEAD_CURR_POS[1] - 1]
            elif SNAKE_MOTION == 'Left':
                HEAD_TARGET_POS = [HEAD_CURR_POS[0] - 1, HEAD_CURR_POS[1]]
            elif SNAKE_MOTION == 'Right':
                HEAD_TARGET_POS = [HEAD_CURR_POS[0] + 1, HEAD_CURR_POS[1]]

            if is_snake_movable(HEAD_TARGET_POS):
                if SNAKE_TAIL_LENGTH > 0:
                    tail_to_expand_pos = SNAKE_TAIL_POS[-1]
                    SNAKE_TAIL_POS = [HEAD_CURR_POS] + SNAKE_TAIL_POS[:-1]

                HEAD_CURR_POS = HEAD_TARGET_POS

                if SNAKE_TAIL_DEFAULT > 0:
                    snake_expand(tail_to_expand_pos)

                snake_tail.clearstamps()
                display_snake()
                eat_food()
                check_contact()  # Check contact after the snake moves
            game_screen.ontimer(snake_move, SNAKE_SPEED)
        else:
            game_screen.ontimer(snake_move, SNAKE_SPEED)

def snake_expand(to_expand_pos)-> None:
    '''
    Expand the snake tail.
    Expand the snake by one block.
    If the snake is expanded, set the snake speed to 400.
    Slow down the snake speed.
    
    Args: to_expand_pos
    Returns: None
    '''
    
    global SNAKE_TAIL_LENGTH
    global SNAKE_TAIL_DEFAULT
    global SNAKE_TAIL_POS
    global SNAKE_SPEED

    SNAKE_TAIL_POS.append(to_expand_pos)
    SNAKE_TAIL_LENGTH += 1
    SNAKE_TAIL_DEFAULT -= 1

    update_snake_speed()


def update_snake_speed()-> None:
    '''
    Update the snake speed.
    If the snake is not fully extended, set the snake speed to 400.
    If the snake is fully extended, set the snake speed to 200.
    
    Args: None
    Returns: None
    '''
    
    global SNAKE_SPEED
    if SNAKE_TAIL_DEFAULT > 0:
        SNAKE_SPEED = 400  # Slower speed when the snake is not fully extended
    else:
        SNAKE_SPEED = 200  # Faster speed when the snake is fully extended


def is_monster_movable(target_position)-> bool:
    '''
    Check if the monster is movable.
    If the target position is within the bounds of the game screen, return True.
    Return False otherwise.
       
    Args: target_position
    Returns: bool
    '''
    
    if 0 <= target_position[0] <= 23 and 0 <= target_position[1] <= 23:
        return True
    else:
        return False


def set_MONSTER_SPEED()-> None:
    '''
    Set the monster speed.
    
    Args: None
    Returns: None
    '''
    
    global MONSTER_SPEED
    MONSTER_SPEED = 500
    

def monsters_move()-> None:
    '''
    Move the monsters.
    Move the monsters to the target position.
    If the game is over, return.
    If the monster is movable, move the monster.
    Use the precise pixel measurements to check the contact with the monster.
    If the monster contacts with the snake, increment the game contact.
    Randomly set the target position of the monsters.
    Ensure that the monsters are not placed in the center of the screen.
    Ensure that the monsters are not placed on top of each other.
       
    Args: None
    Returns: None
    '''
    global MONSTER_SPEED
    if is_game_over():
        return

    # Randomly choose 1 or 2 monsters to move
    num_monsters_to_move = min(len(monsters), randrange(1, 3))
    monsters_to_move = sample(list(enumerate(monsters)), num_monsters_to_move)

    for index, monster in monsters_to_move:
        curr_pos = monster_curr_pos[index]
        target_pos = monster_target_pos[index]

        dx = HEAD_CURR_POS[0] - curr_pos[0]
        dy = HEAD_CURR_POS[1] - curr_pos[1]

        suggested_moves = []
        if dy >= dx and dy >= -dx and dy >= 0:
            suggested_moves.append([curr_pos[0], curr_pos[1] + 1])
        if dy <= dx and dy <= -dx and dy <= 0:
            suggested_moves.append([curr_pos[0], curr_pos[1] - 1])
        if -dx <= dy <= dx and dx >= 0:
            suggested_moves.append([curr_pos[0] + 1, curr_pos[1]])
        if dx <= dy <= -dx and dx <= 0:
            suggested_moves.append([curr_pos[0] - 1, curr_pos[1]])

        for move in suggested_moves:
            if is_monster_movable(move) and move not in monster_curr_pos:
                monster_curr_pos[index] = move
                monster.goto(-230 + move[0] * 20, -270 + move[1] * 20)

    turtle.update()  # Force screen update to reflect changes
    if not IS_END_TIME:
        game_screen.ontimer(monsters_move, MONSTER_SPEED)  # Continue moving monsters at a set interval




def check_contact_with_monster(monster_index)-> None:
    '''
    Check the contact with the monster using precise pixel measurements.
    If the monster is contact with the snake, increment the game contact.
    
    Args: monster_index
    Returns: None
    '''
    
    global GAME_CONTACT
    curr_pos = monster_curr_pos[monster_index]
    monster_pixel_x = -230 + curr_pos[0] * 20
    monster_pixel_y = -270 + curr_pos[1] * 20

    # Check the contact with the monster using pixel distance
    for block in SNAKE_TAIL_POS:
        snake_pixel_x = -240 + block[0] * 20
        snake_pixel_y = -280 + block[1] * 20

        if -10 < (monster_pixel_x - snake_pixel_x) < 10 and -10 < (monster_pixel_y - snake_pixel_y) < 10:
            GAME_CONTACT += 1
            refresh_status_bar()
            return



def eat_food()-> None:
    '''
    Eat the food.
    Check if the snake has eaten the food.
    If the snake has eaten the food, clear the food.
    Increment the snake tail length.
    
    Args: None
    Returns: None
    '''
    
    global SNAKE_TAIL_DEFAULT

    if food_pos_1 == HEAD_CURR_POS:
        food_1.clear()
        food_pos_1[0] = -1  
        food_pos_1[1] = -1
        FOOD_TO_EAT.remove(1)
        SNAKE_TAIL_DEFAULT += 1
    if food_pos_2 == HEAD_CURR_POS:
        food_2.clear()
        food_pos_2[0] = -1
        food_pos_2[1] = -1
        FOOD_TO_EAT.remove(2)
        SNAKE_TAIL_DEFAULT += 2
    if food_pos_3 == HEAD_CURR_POS:
        food_3.clear()
        food_pos_3[0] = -1
        food_pos_3[1] = -1
        FOOD_TO_EAT.remove(3)
        SNAKE_TAIL_DEFAULT += 3
    if food_pos_4 == HEAD_CURR_POS:
        food_4.clear()
        food_pos_4[0] = -1
        food_pos_4[1] = -1
        FOOD_TO_EAT.remove(4)
        SNAKE_TAIL_DEFAULT += 4
    if food_pos_5 == HEAD_CURR_POS:
        food_5.clear()
        food_pos_5[0] = -1
        food_pos_5[1] = -1
        FOOD_TO_EAT.remove(5)
        SNAKE_TAIL_DEFAULT += 5


def is_game_over()-> bool:
    '''
    Check if the game is over due to collision with a monster.
    If the snake head is within 10 pixels of a monster, display the game over sign.
    If the snake tail length is 20, display the game win sign.

    Args: None   
    Returns: bool indicating if the game is over.
    '''
    
    global IS_END_TIME
    
    # Check collision with monsters only
    for pos in monster_curr_pos:
        if -10 < (pos[0] * 20 - HEAD_CURR_POS[0] * 20) < 10 and \
           -10 < (pos[1] * 20 - HEAD_CURR_POS[1] * 20) < 10:
            display_game_over()
            IS_END_TIME = True
            return True

    # Check if the player has won the game (optional winning condition)
    if SNAKE_TAIL_LENGTH == 20:
        display_game_win()
        IS_END_TIME = True
        return True
    
    return False


def check_contact()-> None:
    '''
    Check the contact.
    Determine if the snake has contacted the monster.
    Use precise pixel measurements to check the contact.
       
    Args: None
    Returns: None
    '''
    
    # Check the contact
    global GAME_CONTACT
    for monster_pos in monster_curr_pos:
        monster_pixel_x = -230 + monster_pos[0] * 20
        monster_pixel_y = -270 + monster_pos[1] * 20
        for snake_block in SNAKE_TAIL_POS:
            snake_pixel_x = -240 + snake_block[0] * 20
            snake_pixel_y = -280 + snake_block[1] * 20
            if -20 <= (monster_pixel_x - snake_pixel_x) <= 20 and -20 <= (monster_pixel_y - snake_pixel_y) <= 20:
                GAME_CONTACT += 1
                refresh_status_bar()
                return


def start_game(x, y)-> None:
    '''
    Start the game.
    
    Args: x, y
    Returns: None
    '''

    global game_introduction
    global GAME_TIME
    game_introduction.clear()
    game_screen.onclick(None)

    display_food() 
    game_screen.ontimer(relocate_food, 5000)
    refresh_time() 
    snake_move()  
    set_MONSTER_SPEED()  
    monsters_move()  
    return x, y



def relocate_food()-> None:
    '''
    Relocate the food.
    Use a list to store the food positions.
    And a list to store the food objects.
    Randomly set the food positions.
    Ensure that the food is not placed in the center of the screen.
    Ensure that the food is not placed on top of each other.
    
    Args: None
    Returns: None
    '''
    
    global food_pos_1, food_pos_2, food_pos_3, food_pos_4, food_pos_5
    global food_1, food_2, food_3, food_4, food_5
    global IS_END_TIME  

    
    if IS_END_TIME:
        return

    food_positions = [food_pos_1, food_pos_2, food_pos_3, food_pos_4, food_pos_5]
    food_objects = [food_1, food_2, food_3, food_4, food_5]
    new_positions = []  

    
    for i, pos in enumerate(food_positions):
        if pos != [-1, -1]:  
            
            food_objects[i].clear()

            
            new_pos = [randrange(0, 25), randrange(0, 25)]
            while new_pos in food_positions or not is_food_valid(new_pos, *(food_positions[:i] + new_positions[i+1:])):
                new_pos = [randrange(0, 25), randrange(0, 25)]
            new_positions.append(new_pos)

           
            food_objects[i].goto(-240 + new_pos[0] * 20, -290 + new_pos[1] * 20)
            food_objects[i].write(str(i+1), font=('Arial', 13, 'normal'))
        else:
            new_positions.append(pos)  

   
    food_pos_1, food_pos_2, food_pos_3, food_pos_4, food_pos_5 = new_positions

    
    game_screen.ontimer(relocate_food, 5000)

def is_food_valid(pos, *other_positions)-> bool:
    '''
    Check if the food is valid.
    If the food is not placed in the center of the screen and not placed on top of each other, return True.
    And return False otherwise.

    Args: pos, *other_positions
    Returns: bool
    '''
    
    return all(pos != other for other in other_positions if other != [-1, -1])

def main()-> None:
    '''
    Main function.
    
    Args: None
    Returns: None
    '''
    setup_screen()
    setup_monsters()  
    setup_snake()
    display_frame()
    display_snake()
    display_monsters()  
    set_food()
    game_screen.onkey(set_snake_direction_up, 'Up')
    game_screen.onkey(set_snake_direction_down, 'Down')
    game_screen.onkey(set_snake_direction_left, 'Left')
    game_screen.onkey(set_snake_direction_right, 'Right')
    game_screen.onkey(set_snake_paused, 'space')
    game_screen.onclick(start_game)
    game_screen.listen()

if __name__ == '__main__':
    main()
    game_screen.listen()
    game_screen.mainloop()