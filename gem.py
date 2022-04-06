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
        for row, line in enumerate(buffer[:editor.height]):
            stdscr.addstr(row, 0, line[:editor.width])

        stdscr.move(editor.cursor_y, editor.cursor_x)

        key = stdscr.getkey()
        if key == 'q': sys.exit(0) # Exit
        elif key in 'hjkl': editor.move_cursor(key) # Cursor movement

if __name__ == "__main__":
    curses.wrapper(main)
