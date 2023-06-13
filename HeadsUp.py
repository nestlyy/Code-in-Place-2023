from graphics import Canvas
import random

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

# Name of the file to read in!
FILE_NAME = 'wordlist.10000.txt'

def get_words_from_file():
    f = open(FILE_NAME)
    lines = []
    for line in f:
        # removes whitespace characters (\n) from the start and end of the line
        line = line.strip() 
        # if the line was only whitespace characters, skip it 
        if line != "":
            lines.append(line)
    return lines


def main():
    #print(random.choice(get_words_from_file()))
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    text_1 = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/4, text='Press Enter to generate a new word!', anchor='center')
    list_of_words = get_words_from_file()
    random_word = random.choice(list_of_words)
    text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, font_size = 30, text=random_word, anchor='center')
    
    while True:
        key = canvas.get_last_key_press()
        if key == 'Enter':
            new_random_word = random.choice(list_of_words)
            canvas.change_text(text, str(new_random_word))

if __name__ == '__main__':
    main()
