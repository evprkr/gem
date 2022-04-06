# emerald.py

import os, sys
import argparse
import curses

from editor import *

def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    with open(args.file) as f:
        buffer = f.readlines()

    editor = Editor(buffer, curses.COLS - 1, curses.LINES - 1)

    while True:
        stdscr.erase()
        for row, line in enumerate(buffer[editor.buff_y:editor.buff_y + editor.buff_h]):
            stdscr.addstr(row, 0, line[editor.buff_x:editor.buff_x + editor.buff_w])

        stdscr.move(*editor.translate_curs())

        key = stdscr.getkey()
        if key == 'q': sys.exit(0) # Exit
        elif key in 'hjkl': editor.move_cursor(key) # Cursor movement

if __name__ == "__main__":
    curses.wrapper(main)
