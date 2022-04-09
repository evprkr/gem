# color.py
# this class contains all custom colors and must be initialized for color to work

# TODO
# Create a YAML config file that can be used to make colorschemes
# init_colors() would look for it and apply whatever it finds to the active colorscheme

import curses

def set_color(index, fg, bg):
    curses.init_pair(index, fg, bg)

def rgb(index, r, g, b):
    curses.init_color(index, int(r/0.255), int(g/0.255), int(b/0.255))

def init_colors():
    curses.start_color()
    curses.use_default_colors()

    rgb(9, 241, 241, 241)
    rgb(10, 71, 76, 83)

    set_color(1, -1, -1)
    set_color(2, 10, -1)

class HighlightGroups:
    BufferText = 1
    LineNumbers = 2

HighlightGroups = HighlightGroups()
