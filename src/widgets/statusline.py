# Simple persistent statusline that displays buffer information in the last row

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
