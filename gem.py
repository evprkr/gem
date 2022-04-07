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

    # Init Buffer, Cursor, Editor
    buffer = Buffer(contents, curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor(buffer, buffer.margin_top, buffer.margin_left)
    editor = Editor(screen, buffer, cursor)

    while True:
        editor.refresh()

        key = screen.getkey()
        if key == 'q': sys.exit(0) # Exit Application
        else: editor.handle_keypress(key)

if __name__ == "__main__":
    curses.wrapper(main)
