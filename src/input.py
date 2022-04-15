# Single Key Constants
# Standard keys and shortcuts/actions performed with a single key
class Key:
    # Important Keys
    Leader = ' '
    Escape = ('KEY_ESCAPE', '\x1b')
    Delete = 'x'; InsDelete = 'KEY_DC'
    Backspace = ('KEY_BACKSPACE', '\b', '\x7f') # Cover all the bases
    Enter = 13
    Tab = '\t'

    # Cursor Movement
    CursorLeft = 'h'
    CursorDown = 'j'
    CursorUp = 'k'
    CursorRight = 'l'

    # Cursor Actions
    JumpLineStart = '('
    JumpLineEnding = ')'
    NextWordEnding = 'L'
    PrevWordEnding = 'H'
    NextBlankLine = 'J'
    PrevBlankLine = 'K'
    BufferFirstRow = 'g'
    BufferLastRow = 'G'

    # Text Manipulation
    LineAppend = 'A'
    LineDelete = 'D'
    UndoAction = 'z'
    RedoAction = 'Z'
    RepeatAction = '.'

    # Mode Switching
    ModeInsert = 'i'
    ModeSelect = 's'
    ModePrompt = ':'
    ModeSearch = '/'


# Leader Key Sequences
# Shortcut performed by pressing a key within 250ms of the leader key (Key.Leader)
class Seq:
    # File Operations
    Quit = [Key.Leader, 'q']
    Save = [Key.Leader, 's']


# Wait Key Sequences
# Single key shortcuts that wait for a second specific key to be pressed to perform an action
class Wait:
    Replace = 'r'
