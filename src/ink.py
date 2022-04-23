#!/usr/bin/env python3

import os, sys, time
import argparse
import curses

from logger import *
from terminal import *
from buffer import *
from cursor import *
from input import * # TODO Rename this file to something else, maybe shortcuts or hotkeys

from popup import *

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
    cursor = Cursor(screen); log.write("Cursor initialized") # Create the cursor
    terminal = Terminal(rows, cols, screen, cursor); log.write("Terminal initialized") # Create the terminal
    terminal.add_buffer(Buffer(file, contents, terminal)); log.write("Initial buffer initialized") # Create the initial buffer

    # Initial update
    terminal.update(); log.write("Initial Terminal update completed") # Run an update loop before starting input loop

    # Input loop
    log.write("Entering input loop")
    while not terminal.quit:
        screen.timeout(250)
        keys = []

        try: k = screen.getkey()
        except: k = None
        keys.append(k)

        # Handle leader sequence (normal mode only)
        if keys[0] != None:
            if terminal.cursor.mode == "NORMAL":
                if keys[0] == Key.Leader:
                    screen.timeout(250)
                    try: k = screen.getkey()
                    except: k = None
                    keys.append(k)
                else:
                    for key in KeyList:
                        if type(key) == tuple:
                            if keys[0] in key:
                                keys.append(None)
                                break
                        else:
                            if keys[0] == key:
                                keys.append(None)
                                break

                    if len(keys) != 2:
                        screen.timeout(-1)
                        k = screen.getkey()
                        keys.append(k)
            else:
                keys.append(None)
        else:
            keys.append(None)

        # Send input to terminal, skip if there is no valid input
        if keys != [None, None]:
            terminal.process_input(keys)
            terminal.update()

    curses.endwin()
    log.write("Input loop terminated")

if __name__ == "__main__":
    log.write("Application started")
    curses.wrapper(main)
    log.write("Application exited successfully")
