# popup.py

# Popups are a type of "window" that operate in the Editor scope.

# TODO
# Add anchors for top right and bottom left, maybe also top center, bottom center, center left, and center, right
# Change 'pad_r' and 'pad_c' to just be 'padding[0]' and 'padding[1]' or something
# Make title optional on PopupDialog and PopupInput

# Add classes for...
#   * PopupConfirm - Body text, confirm button, and optional cancel button, buttons can have different actions
#   * PopupChoice - Body text, multiple choice list, different input types (select one or multiple), and confirm button

import curses
from color import *

# PopupDialog - Simple window with text and nothing else
class PopupDialog:
    def __init__(self, row, col, title, body, anchor="top left", padding=(0, 0)):
        self.row = row
        self.col = col
        self.title = title
        self.body = body

        self.anchor = anchor
        self.pad_r = padding[0]
        self.pad_c = padding[1]

        self.height = None
        self.width = None

        self.update()

    def update(self):
        # Update window height
        self.height = len(self.body) + (self.pad_r * 2) + 2

        # Update window width
        min_len = 0
        for line in self.body:
            if len(line) > min_len:
                min_len = len(line)
        self.width = min_len + (self.pad_c * 2) + 2

    def print(self, screen):
        screen.attron(curses.color_pair(Colors.Background))
        # Get Coordinates
        if self.anchor == "center":
            box_row = self.row - (self.height // 2)
            box_col = self.col - (self.width // 2)
        elif self.anchor == "bottom right":
            box_row = self.row - self.height
            box_col = self.col - self.width
        else: # Defaults to top left anchor
            box_row = self.row
            box_col = self.col

        # Box
        window = screen.derwin(self.height, self.width, box_row, box_col)
        window.box()

        # Title
        window.addstr(0, 1, f" {self.title} ")

        # Background
        for r in range(1, self.height-1):
            for c in range(1, self.width-1):
                screen.addstr(box_row+r, box_col+c, ' ')

        # Body
        for row, line in enumerate(self.body):
            window.addstr(row+self.pad_r+1, self.pad_c+1, line)

        screen.attroff(curses.color_pair(Colors.Background))


# PopupInput - Window with a single line text input and optional label text
class PopupInput:
    def __init__(self, row, col, title="Input", label=None, input_size=10, anchor="center", padding=(0, 0)):
        self.row = row
        self.col = col
        self.title = title
        self.label = label
        self.input_size = input_size
        self.anchor = anchor
        self.pad_r = padding[0]
        self.pad_c = padding[1]
        
        if self.label: self.height = (self.pad_r * 2) + 4
        else: self.height = (self.pad_r * 2) + 2

        if self.label: self.width = max(len(label), input_size) + (self.pad_c * 2) + 2
        else: self.width = input_size + (self.pad_c * 2) + 2
