#!/usr/bin/env python3

# Ink Editor - ink.py
# github.com/leftbones/ink

from __future__ import annotations

import os, sys
import traceback
import curses

from termcolor import cprint
from argparse import ArgumentParser, Namespace

from logger import log

from terminal import Terminal
from window import Window

from keys import *


# Argument Parsing
def _process_arguments(argv: list[str] | None = None) -> Namespace:
    parser = ArgumentParser(prog='ink')
    parser.add_argument('filepath', help='path to an editable file', nargs='?', default=None)
    return parser.parse_args(argv)

# Main Process
def main(screen, args):
    curses.start_color()
    curses.use_default_colors()
    curses.set_escdelay(250)
    screen.timeout(250)

    log.erase()

    if not args.filepath: args.filepath = 'New File'
    filename = os.path.basename(args.filepath)

    # Create Terminal instance
    terminal = Terminal(screen, curses.LINES, curses.COLS, args.filepath)

    # Create an empty window
    terminal.add_window(
        title = "New File",
        contents = ['\n'],
        row = 0,
        col = 0,
        nrows = terminal.nrows,
        ncols = terminal.ncols,
        box = True,
        statusline = True,
        linenumbers = True,
        emptylines = True,
    )

    # Load file from arguments
    try: terminal.do_open(args.filepath, terminal.windows[-1])
    except FileNotFoundError:
        terminal.send_alert("Error", [f"File {args.filepath} not found!\n", "Editing new file.\n"], 5)
        terminal.cursor.window.title = args.filepath
        terminal.cursor.window.dirty = True

    terminal.print()

    # Main input loop
    while not terminal.exit:
        terminal.screen.timeout(250)
        keys = []

        try: k = terminal.screen.getkey()
        except: k = None
        keys.append(k)

        # Handle multi-key sequences (normal mode and list mode only)
        if keys[0] != None and keys[0] not in Key.Escape:
            if terminal.cursor.mode in ["NORMAL", "LIST"]:
                if keys[0] == Key.Leader:
                    try: k = terminal.screen.getkey()
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
                        for wait in WaitList:
                            if type(wait) == str:
                                if keys[0] == wait:
                                    terminal.screen.timeout(-1)
                                    k = terminal.screen.getkey()
                                    keys.append(k)
                        for seq in SeqList:
                            if type(seq) == list:
                                if keys[0] == seq[0]:
                                    terminal.screen.timeout(-1)
                                    k = terminal.screen.getkey()
                                    keys.append(k)
                        if len(keys) != 2:
                            keys.append(None)
            else:
                keys.append(None)
        else:
            keys.append(None)

        # Send input to terminal to be processed
        try:
            terminal.process_input(keys)
            terminal.print()
        except Exception:
            tb = traceback.format_exc()

            terminal.screen.clear()
            terminal.screen.refresh()
            terminal.screen.timeout(-1)

            curses.reset_shell_mode()

            cprint("*** Ink has encountered an error! ***\n", attrs=['reverse'])
            print("Don't worry, your work is not lost! Here's some info on what happened...\n")
            print(tb)

            print("Press any key to continue...")

            curses.raw()
            curses.napms(1000)

            terminal.screen.getkey()

            curses.flushinp()
            curses.reset_prog_mode()

            terminal.screen.clear()
            terminal.screen.refresh()
            terminal.screen.timeout(250)

    curses.endwin()
    if terminal.deletelog: log.delete()

if __name__ == '__main__':
    args = _process_arguments(sys.argv[1:])
    curses.wrapper(main, args)
