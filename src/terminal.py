# Ink Editor - terminal.py
# github.com/leftbones/ink

import os, pathlib
import curses

from logger import log

from config import Config
from cursor import Cursor
from window import Window

from actions import ActionHandler

from highlighter import Highlighter
from colorizer import Colorizer

from keys import *

class Terminal:
    def __init__(self, screen, nrows, ncols, path):
        self.screen = screen
        self.nrows = nrows
        self.ncols = ncols
        self.path = path

        self.exit = False

        self.config = Config()
        self.cursor = Cursor()

        self.windows = []
        self.tabs = []
        self.popup = None

        self.prompt_open = False
        self.prompt_window = None

        self.sidebar_open = False
        self.sidebar_window = None
        self.sidebar_paths = []
        self.sidebar_hint = 0

        self.tabswitcher_open = False
        self.tabswitcher_window = None

        # Load Configs
        self.deletelog = self.config.deletelog
        self.cleanlines = self.config.cleanlines
        self.hiddenfiles = self.config.hiddenfiles
        self.excludedirs = self.config.excludedirs

        # Init ActionHandler
        self.actionhandler = ActionHandler(self)

        # Init Colorizer
        self.colorizer = Colorizer(self)

    # Print all windows to the screen
    def print(self):
        self.screen.erase()
        self.screen.move(0, 0)

        for window in self.windows:
            window.print()
            if window.lifetime > 0:
                window.lifetime -= 0.5
                if window.lifetime == 0:
                    self.del_window(window)
                    self.popup = None

        self.screen.move(*self.cursor.window.translate_pos(self.cursor))

    # Exit the application
    def do_exit(self):
        self.exit = True

    # Open a file in a window
    def do_open(self, file, window=None, tab=False):
        if window == None: window = self.cursor.win_hint
        file = os.path.expanduser(file)
        with open(file, 'r') as f:
            window.contents = f.readlines()
            self.cursor.goto(0, 0)
        f.close()
        if len(window.contents) == 0: window.contents = ['\n']
        window.title = os.path.basename(file)
        window.path = file

        # Slight workaround, see issue #18 for more details
        if not window.path.endswith('txt'):
            window.highlighter.match_lexer()

    # Save the current file
    def do_save(self, file=None):
        if file == None:
            file = self.cursor.win_hint.path
        else:
            file = os.path.expanduser(os.path.dirname(self.cursor.win_hint.path) + '/' + file)
        with open(file, 'w') as f:
            f.writelines(self.cursor.win_hint.contents)
        f.close()
        self.cursor.win_hint.dirty = False

    # Add a window, all parameters are optional, steals cursor focus if set, steals cursor focus if cursor has no current focus
    def add_window(self, title=None, contents=None, row=0, col=0, nrows=None, ncols=None, box=True, margins=None, statusline=None, linenumbers=None, emptylines=None, readonly=False, lifetime=-1, steal_focus=False):
        wid = len(self.windows) + 1

        if not nrows: nrows = self.nrows
        if not ncols: ncols = self.ncols

        if not margins: margins = self.config.defaultmargins

        if statusline == None: statusline = self.config.statusline
        if linenumbers == None: linenumbers = self.config.linenumbers
        if emptylines == None: emptylines = self.config.emptylines

        window = Window(self, wid, title, contents, row, col, nrows, ncols, box, margins, statusline, linenumbers, emptylines, readonly, lifetime)

        if not self.cursor.window:
            self.cursor.window = window
            self.cursor.win_hint = window
            self.cursor.update_memory()
        elif steal_focus:
            self.cursor.win_hint = self.cursor.window
            self.cursor.goto_window(window)
            self.cursor.update_memory()

        self.windows.append(window)

    # Delete a window, fails if there is only one window in the terminal - if window is cursor's window, move cursor to cursor's window hint
    def del_window(self, window):
        if len(self.windows) == 1: return # TODO Show error message, can't delete last window
        if self.cursor.window == window: self.cursor.goto_window(self.cursor.win_hint)
        self.windows.remove(window)
        self.cursor.update_memory()

    # Open or close the toggle window, sets cursor to prompt mode, steals focus when opened
    def toggle_prompt(self):
        # Break early if sidebar is open
        if self.sidebar_open: return

        if not self.prompt_open:
            self.cursor.set_mode("PROMPT")
            self.add_window(
                title = "Prompt",
                contents = ['\n'],
                row = self.nrows // 2 - 1,
                col = self.ncols // 2 - 20,
                nrows = 3,
                ncols = 40,
                box = True,
                margins = [0, 0, 1, 1],
                statusline = False,
                linenumbers = False,
                emptylines = False,
                steal_focus = True
            )
            self.prompt_window = self.windows[-1]
            self.prompt_window.hscrolloffset = 0
            self.prompt_window.hlsyntax = False
            self.prompt_open = True
        else:
            self.cursor.set_mode("NORMAL")
            self.del_window(self.prompt_window)
            self.prompt_open = False

    # Open or close the sidebar window, steals focus when opened
    def toggle_sidebar(self, reset_cursor=False):
        if not self.sidebar_open:
#            self.cursor.window.ncols = self.cursor.window.ncols - 30
#            self.cursor.window.col = 30
            self.cursor.set_mode("LIST")
            self.add_window(
                title = "Directory",
                contents = self.get_file_tree(os.getcwd()),
                row = 0,
                col = 0,
                nrows = self.nrows,
                ncols = 30,
                box = True,
                margins = [0, 0, 1, 1],
                statusline = False,
                linenumbers = False,
                emptylines = False,
                steal_focus = True
            )
            self.sidebar_window = self.windows[-1]
            self.sidebar_window.hscrolloffset = 0
            self.sidebar_window.hlsyntax = False
            self.sidebar_open = True
            self.cursor.goto(self.sidebar_hint, 0)
        else:
#            self.cursor.win_hint.ncols = self.ncols
#            self.cursor.win_hint.col = 0
            self.cursor.set_mode("NORMAL")
            self.del_window(self.sidebar_window)
            if reset_cursor: self.cursor.goto(0, 0)
            self.sidebar_open = False

    # Open or close the tab switcher, steals focus when opened
    def toggle_tabswitcher(self, reset_cursor=False):
        if not self.tabswitcher_open:
            self.cursor.set_mode("LIST")
            self.add_window(
                title = "Tab Switcher",
                contents = ['This\n', 'doesn\'t\n', 'work yet\n', ':(\n'],
                row = self.nrows // 3,
                col = self.ncols // 3,
                nrows = self.nrows // 3,
                ncols = self.ncols // 3,
                box = True,
                margins = [0, 0, 1, 1],
                statusline = False,
                linenumbers = False,
                emptylines = False,
                steal_focus = True,
            )
            self.tabswitcher_window = self.windows[-1]
            self.tabswitcher_window.hscrolloffset = 0
            self.tabswitcher_window.hlsyntax = False
            self.tabswitcher_open = True
        else:
            self.cursor.set_mode("NORMAL")
            self.del_window(self.tabswitcher_window)
            if reset_cursor: self.cursor.goto(0, 0)
            self.tabswitcher_open = False

    # Create a temporary window with a specified message
    def send_alert(self, title, contents, timeout):
        window_width = len(max(contents, key=len)) + 3
        if window_width > self.ncols:
            title = "Whoops"
            contents = ["That's too much text to put in this tiny window.\n", "Nice job, you broke it.\n"]
            window_width = len(max(contents, key=len)) + 3
        window_height = len(contents) + 2

        self.add_window(
            title = title,
            contents = contents,
            row = 1,
            col = self.ncols - (window_width + 2),
            nrows = window_height,
            ncols = window_width,
            box = True,
            margins = [0, 0, 1, 1],
            statusline = False,
            linenumbers = False,
            emptylines = False,
            readonly = True,
            lifetime = timeout * 2,
        )


        if self.popup: self.del_window(self.popup)
        self.popup = self.windows[-1]
        self.popup.hlsyntax = False

    # Construct a file tree list to be shown in the sidebar
    def get_file_tree(self, path):
        tree = []
        self.sidebar_paths = []

        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            depth = ' ' * 2 * (level)

            if os.path.basename(root) not in self.excludedirs:
                tree.append(f"{depth}\ue5ff {os.path.basename(root)}")
                self.sidebar_paths.append(root)
                subindent = ' ' * 2 * (level + 1)

                for f in files:
                    if not self.hiddenfiles and f.startswith('.'): pass
                    else:
                        tree.append(f"{subindent}\uf0f6 {f}")
                        self.sidebar_paths.append(os.path.join(root, f))

        return tree

    # Process input from stream and call appropriate functions
    def process_input(self, keys):
        # Break early if no input was received
        if keys == [None, None]: return

        # Single Keys
        # ------------------------------
        if keys[1] == None:
            key = keys[0]

            # Normal Mode
            # ------------------------------
            if self.cursor.mode == "NORMAL":
                # Important Keys
                if key == Key.ModeInsert:
                    self.cursor.set_mode("INSERT")

                elif key == Key.ModePrompt:
                    self.toggle_prompt()

                elif key == Key.ModeSelect:
                    self.cursor.start_select_mode()

                elif key == Key.ModeLineSelect:
                    self.cursor.start_line_select_mode()

                elif key == Key.Delete or key == Key.InsDelete:
                    self.cursor.window.delete_char(self.cursor)

                # Cursor Movement
                elif key == Key.CursorLeft: self.cursor.move_left()
                elif key == Key.CursorRight: self.cursor.move_right()
                elif key == Key.CursorUp: self.cursor.move_up()
                elif key == Key.CursorDown: self.cursor.move_down()

                elif key == Key.JumpLineStart: self.cursor.goto(self.cursor.row, 0)
                elif key == Key.JumpLineEnding: self.cursor.goto(self.cursor.row, self.cursor.line_end - 1)

                elif key == Key.NextWordEnding:
                    if self.cursor.char == ' ': self.cursor.move_right()
                    while self.cursor.char not in ' \n': self.cursor.move_right()
                elif key == Key.PrevWordEnding:
                    if self.cursor.char == ' ': self.cursor.move_left()
                    while self.cursor.char not in ' ' and self.cursor.col > 0: self.cursor.move_left()

                elif key == Key.NextBlankLine:
                    if self.cursor.line == '\n': self.cursor.move_down()
                    while self.cursor.row < self.cursor.window.line_count - 1 and self.cursor.line != '\n':
                        self.cursor.move_down()
                elif key == Key.PrevBlankLine:
                    if self.cursor.line == '\n': self.cursor.move_up()
                    while self.cursor.row > 0 and self.cursor.line != '\n':
                        self.cursor.move_up()

                elif key == Key.WindowLastRow:
                    self.cursor.goto(self.cursor.window.line_count - self.cursor.window.lower_edge, self.cursor.col)

                # Text Manipulation
                elif key == Key.LineAppend: self.cursor.goto(self.cursor.row, self.cursor.line_end, "INSERT"); 
                elif key == Key.LineDelete:
                    self.cursor.window.delete_line(self.cursor)

                elif key == Key.UndoAction: self.cursor.window.undo(self.cursor)
                elif key == Key.RedoAction: self.cursor.window.redo(self.cursor)

                # Window Navigation
                elif key == Key.WindowCycle: self.cycle_windows()
                elif key == Key.ToggleSidebar: self.toggle_sidebar()
                elif key == Key.ToggleTabSwitcher: self.toggle_tabswitcher()

            # Insert Mode
            # ------------------------------
            elif self.cursor.mode == "INSERT":
                if key in Key.Escape:
                    if self.cleanlines: self.cursor.window.clean_lines(self.cursor)
                    self.cursor.set_mode("NORMAL")
                    self.cursor.move_left()

                elif key in Key.Backspace: self.cursor.window.bksp_char(self.cursor)
                elif key == Key.InsDelete: self.cursor.window.delete_char(self.cursor)

                elif key == Key.ArrowLeft: self.cursor.move_left()
                elif key == Key.ArrowRight: self.cursor.move_right()
                elif key == Key.ArrowUp: self.cursor.move_up()
                elif key == Key.ArrowDown: self.cursor.move_down()

                elif key == Key.Tab:
                    for i in range(self.cursor.window.tabstop): self.cursor.window.insert_char(self.cursor, ' ')
                elif key in Key.Enter: self.cursor.window.split_line(self.cursor)

                else: self.cursor.window.insert_char(self.cursor, key)

            # Select Mode
            # ------------------------------
            elif self.cursor.mode == "SELECT":
                if key in Key.Escape:
                    self.cursor.set_mode("NORMAL")

                # Cursor Movement
                elif key == Key.CursorLeft: self.cursor.move_left()
                elif key == Key.CursorRight: self.cursor.move_right()
                elif key == Key.CursorUp: self.cursor.move_up()
                elif key == Key.CursorDown: self.cursor.move_down()

                elif key == Key.JumpLineStart: self.cursor.goto(self.cursor.row, 0)
                elif key == Key.JumpLineEnding: self.cursor.goto(self.cursor.row, self.cursor.line_end - 1)

                elif key == Key.NextWordEnding:
                    if self.cursor.char == ' ': self.cursor.move_right()
                    while self.cursor.char not in ' \n': self.cursor.move_right()
                elif key == Key.PrevWordEnding:
                    if self.cursor.char == ' ': self.cursor.move_left()
                    while self.cursor.char not in ' ' and self.cursor.col > 0: self.cursor.move_left()

                elif key == Key.NextBlankLine:
                    if self.cursor.line == '\n': self.cursor.move_down()
                    while self.cursor.row < self.cursor.window.line_count - 1 and self.cursor.line != '\n':
                        self.cursor.move_down()
                elif key == Key.PrevBlankLine:
                    if self.cursor.line == '\n': self.cursor.move_up()
                    while self.cursor.row > 0 and self.cursor.line != '\n':
                        self.cursor.move_up()

            # Line Select Mode
            # ------------------------------
            elif self.cursor.mode == "LINE SELECT":
                if key in Key.Escape:
                    self.cursor.set_mode("NORMAL")

                elif key == Key.CursorUp: self.cursor.move_up()
                elif key == Key.CursorDown: self.cursor.move_down()

                elif key == Key.NextBlankLine:
                    if self.cursor.line == '\n': self.cursor.move_down()
                    while self.cursor.row < self.cursor.window.line_count - 1 and self.cursor.line != '\n':
                        self.cursor.move_down()
                elif key == Key.PrevBlankLine:
                    if self.cursor.line == '\n': self.cursor.move_up()
                    while self.cursor.row > 0 and self.cursor.line != '\n':
                        self.cursor.move_up()

            # Prompt Mode
            # ------------------------------
            elif self.cursor.mode == "PROMPT":
                if key in Key.Escape: self.toggle_prompt()
                elif key == Key.ArrowLeft: self.cursor.move_left()
                elif key == Key.ArrowRight: self.cursor.move_right()
                elif key == Key.InsDelete: self.cursor.window.delete_char(self.cursor)
                elif key in Key.Backspace:
                    if self.cursor.col == 0: self.toggle_prompt()
                    else: self.cursor.window.bksp_char(self.cursor)

                elif key in Key.Enter:
                    prompt_input = self.cursor.window.contents[-1].rstrip()
                    error = self.actionhandler.parse_input(prompt_input)
                    if not error: self.toggle_prompt()

                elif key in (Key.ArrowUp, Key.ArrowDown, Key.Tab): pass
                else: self.cursor.window.insert_char(self.cursor, key)

            # List Mode
            # ------------------------------
            elif self.cursor.mode == "LIST":
                # Close Window
                if key in Key.Escape:
                    if self.sidebar_open: self.toggle_sidebar()
                    if self.tabswitcher_open: self.toggle_tabswitcher()

                elif key == Key.ToggleSidebar:
                    if self.sidebar_open: self.toggle_sidebar()

                # Cursor Movement
                elif key == Key.CursorLeft: self.cursor.move_left()
                elif key == Key.CursorRight: self.cursor.move_right()
                elif key == Key.CursorUp:
                    self.cursor.move_up()
                    if self.sidebar_open: self.sidebar_hint = self.cursor.row
                elif key == Key.CursorDown:
                    self.cursor.move_down()
                    if self.sidebar_open: self.sidebar_hint = self.cursor.row

                elif key == Key.JumpLineStart: self.cursor.goto(self.cursor.row, 0)
                elif key == Key.JumpLineEnding: self.cursor.goto(self.cursor.row, self.cursor.line_end - 1)

                elif key == Key.WindowLastRow:
                    self.cursor.goto(self.cursor.window.line_count - self.cursor.window.lower_edge, self.cursor.col)

                # Select Item
                elif key in Key.Enter or key == ' ':
                    if self.sidebar_window:
                        if '\ue5ff' not in self.cursor.line:
                            self.do_open(self.sidebar_paths[self.cursor.row])
                            self.toggle_sidebar(reset_cursor=True)
                    elif self.tabswitcher_window:
                        self.toggle_tabswitcher(reset_cursor=True)

        # Leader Hotkeys
        # ------------------------------
        elif keys[0] == Key.Leader:
            pass

        # Other Hotkeys
        # ------------------------------
        else:
            if keys == Seq.ForceQuit: self.do_exit()
            elif keys == Seq.WindowFirstRow: self.cursor.goto(0, self.cursor.col)
            elif keys == Seq.LineDelete:
                self.cursor.window.delete_line(self.cursor)

            elif keys[0] == Wait.Replace:
                self.cursor.window.replace_char(self.cursor, keys[1])
