# Command Handler
# Handles processing and executing of all commands

from logger import *
from commands import *
from errors import *

class CmdHandler:
    def __init__(self, terminal):
        self.terminal = terminal
        self.error = None

    def process(self, cmd):
        self.error = None
        cursor = self.terminal.cursor
        buffer = cursor.prev_buffer
        cmd = ''.join(cmd).replace('\n', '').split(' ') # Remove list brackets, remove \n, split at spaces

        args = cmd.copy()[1:]
        cmd = cmd[0]


        # File Manipulation
        if cmd in Cmd.Quit: self.terminal.quit = True
        elif cmd in Cmd.Save: self.terminal.save_buffer(buffer)
        elif cmd in Cmd.SaveQuit:
            self.terminal.save_buffer(buffer)
            self.terminal.quit = True

        # Quick jump to any line
        elif cmd.isnumeric() and len(args) == 0:
            try:
                self.terminal.close_prompt()
                cursor.goto(int(cmd) - 1, 0)
            except Exception as e:
                self.error = PythonError(f"*Python Error* {e}")

        # Goto (row, col) in buffer
        elif cmd in Cmd.Goto:
            if len(args) == 2: 
                try:
                    row = int(args[0]) - 1
                    col = int(args[1]) - 1
                    self.terminal.close_prompt()
                    cursor.goto(row, col)
                except Exception as e:
                    self.error = PythonError(f"*Python Error* {e}")
            else:
                self.error = InvalidArgsError(f"wrong number of arguments, expected 2, got {len(args)}")

#        elif cmd in Cmd.Pop:
#            if len(args) == 1: pass
#            else:
#                self.error = InvalidArgsError(f"wrong number of arguments, expected 1, got {len(args)}")

        # Add blank lines to buffer
        elif cmd in Cmd.AddLines:
            if len(args) == 1:
                try:
                    num = int(args[0])
                    self.terminal.close_prompt()
                    for i in range(num):
                        buffer.split_line(cursor)
                except Exception as e:
                    self.error = PythonError(f"*Python Error* {e}")
            else:
                self.error = InvalidArgsError(f"wrong number of arguments, expected 2, got {len(args)}")

        else: self.error = CmdNotFoundError(f"command '{cmd}' not found")

        return self.error
