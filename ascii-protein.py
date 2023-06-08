import numpy as np
from PIL import Image
import os
from rich import print

"""
Author: Gabe
Date: 6/8/23
Description: This program converts images that are 50x25 pixels into ASCII terminal art. The goal is to do this sequentially,
and then use those new ASCII image strings to create terminal ASCII movies of proteins. These will then be used as visuals
for my full ptop application.
"""

# Constants
gscale = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
ncols = 50
nrows = 25

def average(tile):
    """
    Author: Gabe Miles
    Date: 6/8/23
    Description: This function turns a portion of an image (or a whole image) into a numpy array,
                 and then computes the average value of that array.

    Input:       PIL image of any size

    Output:      int average brightness
    """
    pix = np.array(tile)
    return int(pix.mean())

def gen_movie(file_prefix, num_frames):
    """
    Author: Gabe Miles
    Date: 6/8/23
    Description: This function takes a directory full of 50x25 pixel images, and converts them to ASCII
                 strings. These array of strings are then added together to make a full image, which is added to a full
                 movie.

    TODO:        Fix string coloring. The console markup keeps appearing and it's inconvenient (makes image look bad
                 and also should not happen)

    Input:       file_prefix, or the filename path excluding number for frames. Make sure the images are .png and of
                 the form "frame000.png

                 num_frames, or the number of frames in the movie

    Output:      2D array of ASCII string images
    """
    global nrows, ncols
    ascii_movie = []

    for i in range(1,num_frames+1):
        ascii_image = []
        frame_num = str(i).rjust(3,"0")
        filename = file_prefix + frame_num + ".png"

        image = Image.open(filename).convert('L')
        width, height = image.size[0], image.size[1]

        col_width = width / ncols
        row_width = height / nrows

        for row in range(nrows):
            ascii_row = ""
            # Tile height
            y1 = row * row_width
            y2 = (row + 1) * row_width
            for col in range(ncols):
                # Tile width
                x1 = col * col_width
                x2 = (col + 1) * col_width
                # Crop image to get tile
                tile = image.crop((x1, y1, x2, y2))

                avg = average(tile)
                avg_scaled = int((avg*64)/255)
                ascii_char = gscale[avg_scaled]
                if len(ascii_row) == 0: # Error catching for indexing string
                    pass
                # If this character comes before a string of none ` character, start color
                elif ascii_char != '`' and ascii_row[len(ascii_row) - 1] == '`':
                    ascii_char = "[magenta]" + ascii_char
                # If this character comes after a string of none ` characters, end color
                elif ascii_char == '`' and ascii_row[len(ascii_row) - 1] != '`':
                    ascii_char = "[/magenta]" + ascii_char

                ascii_row += ascii_char

            # Add row to overall image
            ascii_image.append(ascii_row)

        ascii_movie.append(ascii_image)

    return ascii_movie

def print_movie(ascii_movie, fps):
    """
    Author: Gabe Miles
    Date: 6/8/23
    Description: Function that prints the previously made ascii_movie to the terminal. It will clear the previous frame before
                 printing the next one.

    Input:       ascii_movie, or a 2D array with ASCII strings

    Output:      prints movie to terminal
    """
    os.system('clear') # Ensure clear terminal
    for image in ascii_movie:
        for line in image:
            print(line)
        wait_time = 1 / fps
        os.system('sleep {:.3f}'.format(wait_time))
        os.system('clear')

if __name__ == "__main__":
    ascii_movie = gen_movie("movie/frame", 10)
    print_movie(ascii_movie, 10)
