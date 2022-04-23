# Single Key Constants
# Standard keys and shortcuts/actions performed with a single key
class Key:
    # Important Keys
    Leader = ' '
    Escape = ('KEY_ESCAPE', '\x1b')
    Delete = 'x'; InsDelete = 'KEY_DC'
    Backspace = ('KEY_BACKSPACE', '\b', '\x7f') # Cover all the bases
    Enter = (13, '\n')
    Tab = '\t'

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
    BufferLastRow = 'G'

    # Text Manipulation
    LineAppend = 'A'
    LineDelete = 'D' # TODO change to delete from cursor to end of line
    UndoAction = 'z'
    RedoAction = 'Z'
    RepeatAction = '.'

    # Mode Switching
    ModeInsert = 'i'
    ModeSelect = 's'
    ModePrompt = ':'
    ModeSearch = '/'

    # Window/Buffer Navigation
    BufferCycle = 'w'

KeyList = Key.__dict__.values()
SpecialKeys = (Key.Escape, Key.Delete, Key.Backspace, Key.Enter, Key.Tab)


# Multi-Key Sequences
# Performed either with two sequential keypresses or with a key pressed within 250ms after the Leader key
class Seq:
    # Special
    ForceQuit = ['Q', 'Q']

    # File Operations
    Save = [Key.Leader, 's']

    # Cursor Actions
    BufferFirstRow = ['g', 'g']
    LineDelete = ['d', 'd']

SeqList = dir(Seq)
for seq in SeqList.copy():
    if seq[0:2] == '__': SeqList.pop(SeqList.index(seq))


# Wait Key Sequences
# Single key shortcuts that wait for a second specific key to be pressed to perform an action
class Wait:
    Replace = 'r'
