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


# Multi-Key Sequences
# Shortcut performed by pressing a key within 250ms of the leader key (Key.Leader)
class Seq:
    # File Operations
    Quit = [Key.Leader, 'q']
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
