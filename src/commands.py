# Prompt Commands
class Cmd:
    # File Manipulation
    Quit            = ('quit', 'q')                     # Quit File
    Save            = ('save', 's', 'w')                # Save/Write File
    SaveQuit        = ('savequit', 'sq', 'wq')          # Save/Write + Quit File
    Open            = ('open', 'o', 'e')                # Open/Edit File
    Pop             = ('pop', 'p')                      # Open a file in a popup window

    # Buffer Navigation
    Goto            = ('goto', 'go')                    # Jump to (row, col) in buffer

    # Buffer Manipulation
    AddLines        = ('addlines', 'al')                # Add blank lines to buffer

#CmdList = Cmd.__dict__.values()
