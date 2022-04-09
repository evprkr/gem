# popup.py

# Popups are a type of "window" that operate in the Editor scope.

# TODO
# Add anchors for top right, bottom left, and bottom right

import curses
from color import *

class PopupDialog:
    def __init__(self, title, body, row, col, padding=(0, 0), anchor="top left"):
        self.title = title
        self.body = body
        self.row = row
        self.col = col

        self.pad_r = padding[0]
        self.pad_c = padding[1]
        self.anchor = anchor
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

        # Body
        for row, line in enumerate(self.body):
            window.addstr(row+self.pad_r+1, self.pad_c+1, line)
