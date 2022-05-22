# Ink Editor - window.py
# github.com/leftbones/ink

import os

class Config:
    def __init__(self):
        self.inkrc_path = os.path.expanduser('~') + '/.inkrc'

        self.deletelog = False                  # (False) Delete the log file after closing Ink

        self.hlsyntax = True                    # (True) Enable colored syntax highlighting
        self.colorscheme = 'material'           # (material) Set the colorscheme (requires hlsyntax = True)
        self.transparentbg = True               # (True) Match Ink's background color to the background color of your terminal

        self.linenumbers = True                 # (True) Buffer lines are numbered
        self.hlcursorline = True                # (True) Highlight the line number at the cursor position (requires linenumbers = True)
        self.emptylines = True                  # (True) Print a '~' on empty buffer lines (requires linenumbers = True)
        self.statusline = True                  # (True) Show relevant status information at the bottom of the window

        self.statusprompt = False               # (False) Nest the prompt into the statusline (requires statusline = True)

        self.autohidetabbar = True              # (True) Hide the tab bar when there is only one tab

        self.tabstop = 4                        # (4) Number of spaces in a tab
        self.autotabs = True                    # (True) Match indent distance on new lines
        self.bksptabs = True                    # (True) Backspace tabs all at once rather than by spaces
        self.deltabs = True                     # (True) Delete tabs all at once rather than by spaces

        self.vscrolloffset = 5                  # (5) Offset (in rows) before vertical scrolling begins
        self.hscrolloffset = 10                 # (10) Offset (in cols) before horizontal scrolling begins

        self.defaultmargins = [0, 0, 0, 0]      # Default margins for new windows

        self.cleanlines = True                  # (True) Automatically strip unnecessary whitespace from lines
        self.preservetabs = False               # (False) Preserve tabs on lines that are only whitespace (requires cleanlines = True)

        self.hiddenfiles = False                # (False) Show hidden files in the sidebar's file tree
        self.excludedirs = ['__pycache__', '.git'] # Directories to exclude from the sidebar's file tree

        # Check for existing inkrc and load configs from it
        if os.path.exists(self.inkrc_path): self.load()

    def load(self):
        pass # TODO read from inkrc file, override defaults with settings in file
