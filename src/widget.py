from logger import *

class Widget:
    def __init__(self, name, buffer, row=0, col=0):
        self.name = name
        self.buffer = buffer
        self.row = row
        self.col = col
    
    def update(self):
        log.write(f"Widget '{self.name}' has no update method!")
