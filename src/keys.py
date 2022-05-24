# Ink Editor - keys.py
# github.com/leftbones/ink

# Single Key Constants
# Standard keys and hotkeys performed with a single key
class Key:
    # Important Keys
    Leader = ' ' # TODO Load from config file
    Escape = ('KEY_ESCAPE', '\x1b')
    Delete = 'x'; InsDelete = 'KEY_DC'
    Backspace = ('KEY_BACKSPACE', '\b', '\x7f')
    Enter = (13, '\n')
    Tab = '\t'

    # Numeric
    Numeric = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Cursor Movement
    CursorLeft = 'h'
    CursorDown = 'j'
    CursorUp = 'k'
    CursorRight = 'l'
    ArrowUp = 'KEY_UP'
    ArrowDown = 'KEY_DOWN'
    ArrowLeft = 'KEY_LEFT'
    ArrowRight = 'KEY_RIGHT'

    # Cursor Actions
    JumpLineStart = '('
    JumpLineEnding = ')'
    NextWordEnding = 'L'
    PrevWordEnding = 'H'
    NextBlankLine = 'J'
    PrevBlankLine = 'K'
    WindowLastRow = 'G'

    # Text Manipulation
    LineAppend = 'A'
    LineDelete = 'D' # TODO change to delete from cursor to end of line
    UndoAction = 'z'
    RedoAction = 'Z'
    RepeatAction = '.'

    # Mode Switching
    ModeInsert = 'i'
    ModeSelect = 's'
    ModeLineSelect = 'S'
    ModePrompt = ':'
    ModeSearch = '/'

    # Window Navigation
    WindowCycle = 'w'
    ToggleSidebar = 'T'
    ToggleTabSwitcher = '\t'

KeyList = Key.__dict__.values()
SpecialKeys = (Key.Escape, Key.Delete, Key.Backspace, Key.Enter, Key.Tab)


# Multi-Key Sequences
# Performed either with two sequential keypresses or with a key pressed within 250ms after the Leader key
class Seq:
    # Special
    ForceQuit = ['Q', 'Q']

    # Cursor Actions
    WindowFirstRow = ['g', 'g']
    LineDelete = ['d', 'd']

SeqList = Seq.__dict__.values()


# Wait Key Sequences
# Single key shortcuts that wait for a second specific key to be pressed to perform an action
class Wait:
    Replace = 'r'

WaitList = Wait.__dict__.values()
