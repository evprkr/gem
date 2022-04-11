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

#    parser = argparse.ArgumentParser()
#    parser.add_argument("file")
#    args = parser.parse_args()

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        try: 
            with open(sys.argv[1]) as f:
                contents = f.readlines()
        except:
            filename = sys.argv[1]
            contents = ["\n"]
    else: # If no arguments, create an empty, unnamed file // TODO Add some sort of landing screen here instead
        filename = "No File"
        contents = ["\n"]

    # Init Components
    max_lines = curses.LINES - 1
    max_cols = curses.COLS - 1

    buffer = Buffer(filename, contents, max_lines, max_cols)
    cursor = Cursor(buffer, 0, 0)
    editor = Editor(screen, buffer, cursor)

    debug_window = PopupDialog(max_lines-1, max_cols, "Debug", ["There's no text here yet"], "bottom right", (1, 2))
    editor.windows.append(debug_window)

    while not editor.exit:
        editor.refresh()

        key = screen.getkey()
        editor.handle_keypress(key)

if __name__ == "__main__":
    curses.wrapper(main)
