# emerald.py

import os, sys
import argparse
import curses

# Local Imports
from buffer import *
from cursor import *
from editor import *

# Application Start
def main(screen):
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    with open(args.file) as f:
        contents = f.readlines()

    # Init Components
    buffer = Buffer(contents, curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor(buffer, buffer.margin_top, buffer.margin_left)
    editor = Editor(screen, buffer, cursor)

    while not editor.exit:
        editor.refresh()

        key = screen.getch()
        editor.handle_keypress(key)

if __name__ == "__main__":
    curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.set_escdelay(25)
    curses.wrapper(main)
