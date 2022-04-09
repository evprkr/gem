# emerald.py

import os, sys
import argparse
import curses

# Local Imports
from buffer import *
from cursor import *
from editor import *
from popup import *
from color import *

# Application Start
def main(screen):
    curses.set_escdelay(25)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    with open(args.file) as f:
        contents = f.read().splitlines()
#        contents = f.readlines()

    # Init Components
    max_lines = curses.LINES - 1
    max_cols = curses.COLS - 1

    init_colors()

    buffer = Buffer(contents, max_lines, max_cols)
    cursor = Cursor(buffer, buffer.margin_top, buffer.margin_left)
    editor = Editor(screen, buffer, cursor)

    debug_window = PopupDialog("Debug", ["There's no text here yet"], max_lines-1, max_cols, (1, 2), "bottom right")
    editor.windows.append(debug_window)

    while not editor.exit:
        editor.refresh()

        key = screen.getkey()
        editor.handle_keypress(key)

if __name__ == "__main__":
    curses.wrapper(main)
