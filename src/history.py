from logger import *

class Action:
    def __init__(self, cursor_pos, items):
        self.cursor_pos = cursor_pos
        self.items = items

class History:
    def __init__(self):
        self.index = 1
        self.changes = [Action((0, 0), ['\n'])]

    def add(self, cursor_pos, items):
        pack = Action(cursor_pos, items)
        self.changes.append(pack)

    def undo(self):
        self.index += 1
        return self.changes[-self.index]

    def redo(self):
        self.index -= 1
        return self.changes[-self.index]

    def fork(self):
        for i in range(self.index-1):
            try: self.changes.pop(-1)
            except Exception as e:
                log.write(f"History: Fork failed, exception: {e}")

        self.index = 1
