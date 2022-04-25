# Displays a scrollbar (non-interactive) on the last col of the buffer to show scroll distance

import curses
from logger import *
from widget import Widget

class Scrollbar(Widget):
    def __init__(self, name, buffer, row, col):
        super().__init__(name, buffer, row, col)
        self.lines = []
        self.position = 0;


    def update(self):
        return self.char, curses.A_REVERSE
