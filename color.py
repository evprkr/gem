# color.py
# this class contains all custom colors and must be initialized for color to work

# TODO
# Create a YAML config file that can be used to make colorschemes
# init_colors() would look for it and apply whatever it finds to the active colorscheme

import curses

# Initialize a new color (redundant)
def set_color(index, fg, bg):
    curses.init_pair(index, fg, bg)

# Convert curses colors (0self.DefaultBG000) to RGB (0-256)
def rgb(index, r, g, b):
    curses.init_color(index, int(r/0.255), int(g/0.255), int(b/0.255))


# Initialize Color System
class HighlightGroups:
    def __init__(self):
        curses.initscr()
        curses.start_color()
        curses.use_default_colors()

        # Color IDs
        self.Background                 = 1
        self.BufferText                 = 2
        self.LineNumbers                = 3
        self.CursorLineNumber           = 4
        self.CursorRowMarker            = 5
        self.StatuslineMain             = 6
        self.StatusFilename             = 7
        self.StatusBufferPos            = 8
        self.StatusCursorPos            = 9
        self.StatusNormalMode           = 10
        self.StatusInsertMode           = 11
        self.StatusSelectMode           = 12
        self.StatusPromptMode           = 13

        # Init Color Pairs
        rgb(9, 26, 26, 34);         self.Black       = 9
        rgb(10, 241, 241, 241);     self.White       = 10
        rgb(11, 71, 76, 83);        self.DarkGray    = 11
        rgb(12, 239, 71, 111);      self.Red         = 12
        rgb(13, 255, 117, 56);      self.Orange      = 13
        rgb(14, 255, 206, 92);      self.Yellow      = 14
        rgb(15, 7, 197, 102);       self.Green       = 15
        rgb(16, 4, 174, 173);       self.Teal        = 16
        rgb(17, 1, 151, 244);       self.Blue        = 17
        rgb(18, 159, 89, 197);      self.Purple      = 18
        rgb(19, 121, 129, 140);     self.LightGray   = 19
        rgb(20, 96, 103, 112);      self.Gray        = 20

        # Default Colors
        self.DefaultFG = self.White
        self.DefaultBG = self.Black

        # Editor Colors
        set_color(self.Background, self.DefaultFG, self.DefaultBG)

        # Buffer Colors
        set_color(self.BufferText, self.White, self.DefaultBG)
        set_color(self.LineNumbers, self.DarkGray, self.DefaultBG)

        set_color(self.CursorLineNumber, self.White, self.DefaultBG)
        set_color(self.CursorRowMarker, self.DefaultFG, self.White)

        # Statusline Colors
        set_color(self.StatuslineMain, self.DefaultFG, self.DarkGray)
        set_color(self.StatusNormalMode, self.Black, self.Green)
        set_color(self.StatusInsertMode, self.Black, self.Orange)
        set_color(self.StatusSelectMode, self.Black, self.Yellow)
        set_color(self.StatusPromptMode, self.Black, self.Purple)
        set_color(self.StatusFilename, self.White, self.Gray)
        set_color(self.StatusBufferPos, self.White, self.Gray)
        set_color(self.StatusCursorPos, self.Black, self.Gray)

Colors = HighlightGroups()
