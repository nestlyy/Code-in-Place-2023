"""
Game can be accessed here: https://codeinplace.stanford.edu/cip3/share/PyFgjbfptw3kODVIpD2I

This code and game can still be improved by:
- changing the delay time every time the "snake" eats the goal to make the snake go faster
- lengthening the size of the player to mimic a snake
- add high scores at the end of the game
- add obstacles
"""

from graphics import Canvas
import time
import random
    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
SIZE = 20
PLAYER_START_X = 0
PLAYER_START_Y = 0

# if you make this larger, the game will go slower
DELAY = 0.15

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.create_rectangle(0, 0,
                    CANVAS_WIDTH,
                    CANVAS_HEIGHT, 'black') 

    # New game card
    intro_card = canvas.create_rectangle(CANVAS_WIDTH/4, CANVAS_HEIGHT/4, (CANVAS_WIDTH/4)+200, (CANVAS_HEIGHT/4)+200, 'white', outline ='green')
    intro_text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, font = 'Arial bold', font_size=25, text='New Game?', anchor='center', color='green')
    intro_subtext = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/1.8, font = 'Helvetica', font_size=10, text='Click anywhere to start', anchor='center')
    snake_image = canvas.create_image_with_size(170, 130, 50, 50, 'snake_img.png')

    
    #create score card
    score_text = canvas.create_text(0, 380, font = 'Arial bold', font_size=15, text='SCORE:', color='white')
    score_number = canvas.create_text(100, 380, font = 'Arial bold', font_size=15, text='0', color='white')
    new_score = 0
    
    canvas.wait_for_click()
    start_game = canvas.get_new_mouse_clicks()
    if start_game != None:
        is_hidden = True
        hide_intro_card(canvas, intro_card, intro_text, intro_subtext, snake_image, is_hidden)


    #create goal
    goal_start_x = 360
    goal_start_y = 360
    goal_x = goal_start_x
    goal_y = goal_start_y
    goal = canvas.create_rectangle(goal_x, goal_y,
                    goal_x + SIZE,
                    goal_y + SIZE, 'salmon')
    canvas.set_outline_color(goal, 'red')

    
    #create player
    velocity_x = 0
    velocity_y = 0
    player_x = PLAYER_START_X
    player_y = PLAYER_START_X
    player = canvas.create_rectangle(player_x, player_y,
                    player_x + SIZE,
                    player_y + SIZE, 'green') 
    canvas.set_outline_color(player, 'white')
    axis = 'x'
    last_key = 'ArrowRight'
    plus_or_minus = 1
    key = ''
    
    # player movement
    while (velocity_x >= 0) and (velocity_x + SIZE < CANVAS_WIDTH) and (velocity_y >= 0) and (velocity_y + SIZE < CANVAS_HEIGHT):
        input = canvas.get_last_key_press()
        if input != None:
            key = input
        else:
            key = last_key
        # Determine axis direction
        if (key == 'ArrowRight') or (key == 'ArrowLeft'):
            axis = 'x'
        else:
            axis = 'y'
        
        # Determine axis movement (up/down or left/right)
        if key == 'ArrowRight' or key == 'ArrowDown':
            plus_or_minus = 1
        else:
            plus_or_minus = -1
        
        # Use axis direction (axis) + movement (plus_or_minus)
        if axis == 'x':
            velocity_x += (plus_or_minus * SIZE)
        else:
            velocity_y += (plus_or_minus * SIZE)

        canvas.moveto(player, velocity_x, velocity_y)
        last_key = key
        
        # detect if the snake reaches the goal 
        # then move the goal to a random location
        # generate a list for random numbers that are multiples of 20
        random_number = random_num_gen(canvas)
        random_x = random.choice(random_number)
        random_y = random.choice(random_number)

        if  (velocity_x == goal_x) and (velocity_y == goal_y):
            goal_x = random_x
            goal_y = random_y
            canvas.moveto(goal, goal_x, goal_y)
            new_score += 1
            canvas.change_text(score_number, str(new_score))
        time.sleep(DELAY)
        
    is_hidden = False
    hide_intro_card(canvas, intro_card, intro_text, intro_subtext, snake_image, is_hidden)

    
# generate a list for random numbers that are multiples of 20
def random_num_gen(canvas):
    random_list = []
    for i in range(0,CANVAS_WIDTH):
        if (i % 20) == 0:
            random_list.append(i)
    return random_list

# hide/unhide the intro and gameover text
def hide_intro_card(canvas, intro_card, intro_text, intro_subtext, snake_image, is_hidden):
    canvas.set_hidden(intro_card, is_hidden)
    canvas.set_hidden(intro_text, is_hidden)
    canvas.set_hidden(intro_subtext, is_hidden)
    canvas.set_hidden(snake_image, is_hidden)

    if is_hidden == False:
        canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2.5, font = 'Helvetica bold', font_size=25, text='GAME OVER!', anchor='center', color = 'red')
        canvas.change_text(intro_subtext, 'Click Run to restart')
        canvas.delete(snake_image)
        
"""
    bg_image = canvas.create_image_with_size(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 'snake_bg.jpeg')
    canvas.create_rectangle(0, 0,
                    CANVAS_WIDTH,
                    CANVAS_HEIGHT, bg_image) 
"""

if __name__ == '__main__':
    main()
