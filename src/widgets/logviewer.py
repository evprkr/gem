# Displays and updates a document in real time, intended for use with log files in a popup window

import curses, os
from logger import *
from widget import Widget

class LogViewer(Widget):
    def __init__(self, name, buffer, file):
        super().__init__(name, buffer)
        self.file = file

    def update(self):
        with open(self.file) as f:
            contents = f.readlines()

        self.buffer.lines = contents
        while self.buffer.line_count > self.buffer.rows + self.buffer.row_offset: self.buffer.row_offset += 1
