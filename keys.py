# keys.py

class Keybinds:
    def __init__(self):
        self.Leader = ' '
        self.Escape = 'KEY_ESCAPE'
        self.Enter = 13
        self.Delete = ('KEY_DC', 'x')
        self.Backspace = ('KEY_BACKSPACE', '\b', '\x7f')
        self.Tab = '\t'

        self.Insert = 'i'
        self.Exit = 'q'
        self.Save = 's'

        self.CursorLeft = 'h'
        self.CursorRight = 'l' 
        self.CursorUp = 'k'
        self.CursorDown = 'j'

        # Line Shortcuts
        self.LineStart = '('
        self.LineEnd = ')'
        self.LineDelete = 'D'
        self.Append = 'A'


Keys = Keybinds()
