"""
File: biasbars.py
---------------------
Add your comments here
"""

import tkinter
import biasbarsdata
import biasbarsgui as gui


# Provided constants to load and plot the word frequency data
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

FILENAME = "data/full-data.txt"

VERTICAL_MARGIN = 30
LEFT_MARGIN = 60
RIGHT_MARGIN = 30
LABELS = ["Low Reviews", "Medium Reviews", "High Reviews"]
LABEL_OFFSET = 10
BAR_WIDTH = 75
LINE_WIDTH = 2
TEXT_DX = 2
NUM_VERTICAL_DIVISIONS = 7
TICK_WIDTH = 15

def get_centered_x_coordinate(width, idx):
    """
    Given the width of the canvas and the index of the current review
    quality bucket to plot, returns the x coordinate of the centered
    location for the bars and label to be plotted relative to.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current label in the LABELS list
    Returns:
        x_coordinate (float): The centered x coordinate of the horizontal line 
                              associated with the specified label.
    >>> round(get_centered_x_coordinate(1000, 0), 1)
    211.7
    >>> round(get_centered_x_coordinate(1000, 1), 1)
    515.0
    >>> round(get_centered_x_coordinate(1000, 2), 1)
    818.3
    """

    line_2 = (LEFT_MARGIN + (width - RIGHT_MARGIN)) / 2

    if idx == 1:
        return line_2
    elif idx == 0:
        return line_2 - ((width - LEFT_MARGIN - RIGHT_MARGIN) / 3)
    else:
        return line_2 + ((width - LEFT_MARGIN - RIGHT_MARGIN) / 3)


def draw_fixed_content(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background border and x-axis labels on it.

    Input:
        canvas (tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing content from the canvas
    width = canvas.winfo_width()    # get the width of the canvas
    height = canvas.winfo_height()  # get the height of the canvas
    # add your code here
    canvas.create_rectangle(LEFT_MARGIN, VERTICAL_MARGIN, width - RIGHT_MARGIN, height - VERTICAL_MARGIN, width=LINE_WIDTH)

    for i in range(len(LABELS)):
        canvas.create_text(get_centered_x_coordinate(width, i), height - VERTICAL_MARGIN + LABEL_OFFSET, text=LABELS[i], anchor=tkinter.N)


def plot_word(canvas, word_data, word):
    """
    Given a dictionary of word frequency data and a single word, plots
    the distribution of the frequency of this word across gender and 
    rating category.

    Input:
        canvas (tkinter Canvas): The canvas on which we are drawing.
        word_data (dictionary): Dictionary holding word frequency data
        word (str): The word whose frequency distribution you want to plot
    """

    draw_fixed_content(canvas)
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # We have provided code to calculate the maximum frequency for the specified
    # word from the provided dict 
    gender_data = word_data[word]
    max_frequency = max(max(gender_data[biasbarsdata.KEY_WOMEN]), max(gender_data[biasbarsdata.KEY_MEN]))

    x_begin = LEFT_MARGIN - (TICK_WIDTH / 2)
    x_end = LEFT_MARGIN + (TICK_WIDTH / 2)
    y = VERTICAL_MARGIN
    frequency = max_frequency


    # Ticks
    for i in range(1, NUM_VERTICAL_DIVISIONS + 2):
        canvas.create_line(x_begin, y, x_end, y, width=LINE_WIDTH)
        canvas.create_text(x_begin - LABEL_OFFSET, y, text=round(frequency), anchor=tkinter.E)
        frequency -= (max_frequency / NUM_VERTICAL_DIVISIONS)
        y += ((height - VERTICAL_MARGIN - VERTICAL_MARGIN) / NUM_VERTICAL_DIVISIONS)

    for i in range(3):
        men_height = height - VERTICAL_MARGIN - (height - VERTICAL_MARGIN - VERTICAL_MARGIN) * (gender_data['M'][i] / max_frequency)
        women_height = height - VERTICAL_MARGIN - (height - VERTICAL_MARGIN - VERTICAL_MARGIN) * (gender_data['W'][i] / max_frequency)

        # Rectangles
        canvas.create_rectangle(get_centered_x_coordinate(width, i) - BAR_WIDTH, women_height, get_centered_x_coordinate(width, i), height - VERTICAL_MARGIN, fill='magenta')
        canvas.create_rectangle(get_centered_x_coordinate(width, i), men_height, get_centered_x_coordinate(width, i) + BAR_WIDTH, height - VERTICAL_MARGIN, fill='lavender')

        # Text (M or W)
        canvas.create_text(get_centered_x_coordinate(width, i) - BAR_WIDTH, women_height, text='W', anchor=tkinter.NW)
        canvas.create_text(get_centered_x_coordinate(width, i), men_height, text='M', anchor=tkinter.NW)


    # Note: You find it helpful to use the KEY_WOMEN and KEY_MEN constants
    # defined in the biasbarsdata file. To see how to use these constants, 
    # reference the example above.


def convert_counts_to_frequencies(word_data):
    """
    This code is provided to you! 

    It converts a dictionary 
    of word counts into a dictionary of word frequencies by 
    dividing each count for a given gender by the total number 
    of words found in reviews about professors of that gender.
    """ 
    K = 1000000
    total_words_men = sum([sum(counts[biasbarsdata.KEY_MEN]) for word, counts in word_data.items()])
    total_words_women = sum([sum(counts[biasbarsdata.KEY_WOMEN]) for word, counts in word_data.items()])
    for word in word_data:
        gender_data = word_data[word]
        for i in range(3):
            gender_data[biasbarsdata.KEY_MEN][i] *= K / total_words_men
            gender_data[biasbarsdata.KEY_WOMEN][i] *= K / total_words_women


# main() code is provided for you
def main():
    import sys
    args = sys.argv[1:]
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    if len(args) == 2:
        WINDOW_WIDTH = int(args[0])
        WINDOW_HEIGHT = int(args[1])

    # Load data
    word_data = biasbarsdata.read_file(FILENAME)
    convert_counts_to_frequencies(word_data)

    # Make window
    top = tkinter.Tk()
    top.wm_title('Bias Bars')
    canvas = gui.make_gui(top, WINDOW_WIDTH, WINDOW_HEIGHT, word_data, plot_word, biasbarsdata.search_words)

    # draw_fixed once at startup so we have the borders and labels
    # even before the user types anything.
    draw_fixed_content(canvas)

    # This needs to be called just once
    top.mainloop()


if __name__ == '__main__':
    main()