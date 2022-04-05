# emerald.py

import os, sys
import argparse
import curses

def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    with open(args.file) as f:
        buffer = f.readlines()

    while True:
        stdscr.erase()
        for row, line in enumerate(buffer):
            stdscr.addstr(row, 0, line)

        key = stdscr.getkey()
        if key == 'q':
            sys.exit(0)

if __name__ == "__main__":
    curses.wrapper(main)
