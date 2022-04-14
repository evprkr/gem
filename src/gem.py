import os, sys, time
import argparse
import curses

from logger import *
from terminal import *
from buffer import *
from cursor import *
from input import * # TODO Rename this file?

def main(screen):
    curses.set_escdelay(25)

    # Load file or create new empty file
    if len(sys.argv) == 2:
        file = sys.argv[1]

        try:
            with open(file) as f:
                contents = f.readlines()
                log.write(f"Data read from file '{file}'")
        except:
            file = sys.argv[1]
            contents = ['\n']
            log.write(f"File '{file}' not found, new file created")
    else:
        file = "New File"
        contents = ['\n']
        log.write("No file name passed as argument, new file created")

    # Terminal size at startup
    rows = curses.LINES - 1
    cols = curses.COLS - 1

    # Init components
    cursor = Cursor(); log.write("Cursor initialized")
    terminal = Terminal(rows, cols, screen, cursor); log.write("Terminal initialized")
    terminal.add_buffer(file, contents); log.write("Initial buffer initialized")
    terminal.update_buffers(); log.write("Initial Terminal update completed")

    # Input loop
    log.write("Entering input loop")
    while not terminal.quit:
        screen.timeout(1000)
        keys = []

        try: k = screen.getkey()
        except: k = None
        keys.append(k)

        # Handle leader sequence (normal mode only)
        if terminal.cursor.mode == "NORMAL" and keys[0] == Key.Leader:
            screen.timeout(250)
            try: k = screen.getkey()
            except: k = None
            keys.append(k)
        else:
            keys.append(None)

        # Send input to terminal, skip if there is no valid input
        if keys != [None, None]:
            terminal.process_input(keys)
            terminal.update()

    log.write("Input loop terminated")

if __name__ == "__main__":
    log.write("Application started")
    curses.wrapper(main)
    log.write("Application exited successfully")
