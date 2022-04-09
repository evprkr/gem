# keys.py

class Keybinds:
    def __init__(self):
        self.Escape = 'KEY_ESCAPE'
        self.Enter = 13
        self.Delete = ('KEY_DC')
        self.Backspace = ('KEY_BACKSPACE', '\b', '\x7f')
        self.CursorLeft = 'h'
        self.CursorRight = 'l' 
        self.CursorUp = 'k'
        self.CursorDown = 'j'
        self.Insert = 'i'
        self.Exit = 'q'

Keys = Keybinds()
