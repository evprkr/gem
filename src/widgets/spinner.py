# Spinner animation that changes frame each time the update method is called

import curses
from logger import *
from widget import Widget

class Spinner(Widget):
    def __init__(self, name, buffer, row, col):
        super().__init__(name, buffer, row, col)

        # All of these high quality animations can be yours for three easy payments of $79.95!
        self.animation = "-\\|/"            # Spinner (Free Trial)
        #self.animation = "←↖↑↗→↘↓↙"        # Arrows
        #self.animation = "___-`'´-___"     # Flippy Line
        #self.animation = "▁▃▄▅▆▇█▇▆▅▄▃"    # Monolith
        #self.animation = "▉▊▋▌▍▎▏▎▍▌▋▊▉"   # Door
        #self.animation = "▖▘▝▗"            # Spinny Square
        #self.animation = "▌▀▐▄"            # Spinny Rectangle
        #self.animation = "◢◣◤◥"            # Spinny Triangle
        #self.animation = "◰◳◲◱"            # Small Spinny Square
        #self.animation = "┤┘┴└├┌┬┐"        # Really Bad Clock
        #self.animation = "◴◷◶◵"            # Slightly better clock
        #self.animation = "◐◓◑◒"            # Why is The Moon Spinning?!
        #self.animation = ".oO@*"           # Explosion? I think?
        #self.animation = "dqpb"            # dqpb
        #self.animation = "⣾⣽⣻⢿⡿⣟⣯⣷"        # from curses import braille
        #self.animation = "▓▒░▒"            # TV Static

        self.frame = 0
        self.char = self.animation[0]

    def update(self):
        if self.frame + 1 < len(self.animation): self.frame += 1
        else: self.frame = 0
        self.char = self.animation[self.frame]

        return self.char, curses.A_REVERSE
