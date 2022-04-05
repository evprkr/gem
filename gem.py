# emerald.py

import curses

def main(stdscr):
    while True:
        k = stdscr.getkey()

if __name__ == "__main__":
    curses.wrapper(main)
