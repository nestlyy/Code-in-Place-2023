from graphics import Canvas
import time
import random

"""
JumPurr
Hello! I made this final project for Code in Place 2023! 
This game was inspired by my cats and Google Chrome's offline Dino Game.
Gaps between obstacles as well as obstacle colors are randomized. Game also speeds up when you reach the scores 10 and 20. 
(Suggested browser: Chrome)
Link to the game: https://codeinplace.stanford.edu/cip3/share/rtsQ0EMyZnzCxHHd1sBs

Click Run to play!

"""


CANVAS_WIDTH = 500
CANVAS_HEIGHT = 200
CAT_SIZE = 50
OBSTACLE_WIDTH = 28
OBSTACLE_HEIGHT = 40
GRASS_WIDTH = 10
VELOCITY = 12 # will increase if score reaches 10
CAT_VELOCITY = 10 
DELAY = 0.1    # lower = faster 

def main():
    #create canvas + sky + static grassland
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    sky_bg = canvas.create_rectangle(CANVAS_WIDTH, CANVAS_HEIGHT, 0, 0, 'lightblue')
    grass = canvas.create_rectangle(0, CANVAS_HEIGHT-GRASS_WIDTH, CANVAS_WIDTH, CANVAS_HEIGHT, 'green')

    # New game card
    intro_card = canvas.create_rectangle(70, 150, 430, 30, 'white', outline ='black')
    intro_text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/3, font = 'Helvetica bold', font_size=50, text='JumPurr!', anchor='center', color='Salmon')
    intro_subtext1 = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, font = 'Helvetica', font_size=15, text='Help Jumpurr the cat to jump over obstacles!', anchor='center')
    intro_subtext2 = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/1.7, font = 'Helvetica italic', font_size=12, text='Click anywhere to start. Press space or click anywhere to jump.', anchor='center', color='Green')
    
    # Score card
    score_text = canvas.create_text(5, 0, font = 'Arial bold', font_size=18, text='SCORE:', color='black')
    score_number = canvas.create_text(80, 0, font = 'Arial bold', font_size=18, text='0', color='black')
    new_score = 0
    
    #Create Jumpurr
    start_x_cat = 10
    start_y_cat = CANVAS_HEIGHT-CAT_SIZE
    end_x_cat = CAT_SIZE
    end_y_cat = CAT_SIZE
    cat_jumper = canvas.create_image_with_size(start_x_cat, start_y_cat, end_x_cat, end_y_cat, 'cat.png')
    top_y_cat = canvas.get_top_y(cat_jumper)
    get_down = False
    jump_up = False
    
    #Create obstacle
    obstacles = []
    start_x_obs = CANVAS_WIDTH - OBSTACLE_WIDTH
    start_y_obs = CANVAS_HEIGHT - OBSTACLE_HEIGHT
    end_x_obs = CANVAS_WIDTH
    end_y_obs = CANVAS_HEIGHT
    obstacles.append(canvas.create_rectangle(start_x_obs, start_y_obs, end_x_obs, end_y_obs, 'salmon', outline='black'))

    # Start of game
    canvas.wait_for_click()
    start_game = canvas.get_new_mouse_clicks()
    if start_game != None:
        is_hidden = True
        hide_intro_card(canvas, intro_card, intro_text, intro_subtext1, intro_subtext2, is_hidden)
   
    # Actual gameplay
    while True:
        # if leading obstacle is out of view, remove it, then add 1 to score
        leading_obstacle = obstacles[0]
        if (canvas.get_left_x(leading_obstacle) + canvas.get_object_width(leading_obstacle) <= 0):
            obstacles.pop(0)
            new_score += 1
            canvas.change_text(score_number, str(new_score))
            
        # if JumPurr hits/overlaps with leading obstacle, stop game and show game over card
        overlap = canvas.find_overlapping(17, 150, 40, 190) 
        if len(overlap) == 2:
            game_over(canvas, intro_card, intro_text, intro_subtext1, intro_subtext2, is_hidden)
            break

        # if last obstacle is a distance of 50, spawn a new one
        trailing_obstacle = obstacles[-1]
        if (canvas.get_left_x(trailing_obstacle) + canvas.get_object_width(trailing_obstacle) <= CANVAS_WIDTH - random_gap_len()):
            obstacles.append(canvas.create_rectangle(CANVAS_WIDTH, start_y_obs, CANVAS_WIDTH+20, end_y_obs, random_color(), outline='black'))

        # obstacle movement
        # speed up movement if score is >= 10 and >=20
        if (int(new_score) >= 10) and (int(new_score) <= 19):
            new_velocity = 18
            for obs in obstacles:
               canvas.moveto(obs, canvas.get_left_x(obs) - new_velocity, start_y_obs)
        elif (int(new_score) >= 20):
            new_velocity = 23
            for obs in obstacles:
               canvas.moveto(obs, canvas.get_left_x(obs) - new_velocity, start_y_obs)
        else:
            for obs in obstacles:
               canvas.moveto(obs, canvas.get_left_x(obs) - VELOCITY, start_y_obs)
        
        #cat jump
        if jump_up is False and get_down is False:
            key = canvas.get_new_key_presses() 
            mouse_click = canvas.get_new_mouse_clicks()
            if str(key) == ' ' or len(mouse_click) == 1:
                jump_up = True
        if jump_up == True:
            if top_y_cat <= (130-CAT_SIZE):
                jump_up = False
                get_down = True
            else:
                top_y_cat -= CAT_VELOCITY
        if get_down == True:
            if top_y_cat >= (start_y_cat):
                get_down = False
            else:
                top_y_cat += CAT_VELOCITY
        canvas.moveto(cat_jumper, 10, top_y_cat)
        time.sleep(DELAY)
        
#random gap length generator
def random_gap_len():
    return random.randint(250,700)
    
#random color generator
def random_color():
    colors = ['blue', 'purple', 'salmon', 'cyan', 'brown', 'red', 'pink']
    return random.choice(colors)

def game_over(canvas, intro_card, intro_text, intro_subtext1, intro_subtext2, is_hidden):
    is_hidden = False
    hide_intro_card(canvas, intro_card, intro_text, intro_subtext1, intro_subtext2, is_hidden)
    
# hide/unhide the intro and gameover text
def hide_intro_card(canvas, intro_card, intro_text, intro_subtext1, intro_subtext2, is_hidden):
    canvas.set_hidden(intro_card, is_hidden)
    canvas.set_hidden(intro_text, is_hidden)
    canvas.set_hidden(intro_subtext1, is_hidden)
    canvas.set_hidden(intro_subtext2, is_hidden)
    if is_hidden == False:
        canvas.change_text(intro_text, 'GAME OVER!')
        canvas.change_text(intro_subtext1, 'Click Run to restart')
        canvas.delete(intro_subtext2)


if __name__ == '__main__':
    main()
