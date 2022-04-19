from logger import *

# Used to track what actions happened in the history in a single object
class Action:
    def __init__(self, cursor_pos, items):
        self.cursor_pos = cursor_pos
        self.items = items

    def __repr__(self):
        return f"{self.cursor_pos} {self.items}"

# Manages history actions, undoing, and redoing
class History:
    def __init__(self, changes=[]):
        self.index = 0
        self.changes = changes

    # Add an action to the history
    def add(self, cursor, items):
        action = Action((cursor.row, cursor.col), items)
        self.changes.insert(0, action)

    # Move to the previous item in the history
    def undo(self):
        self.index += 1
        return self.changes[self.index]

    # Move to the next item in the history, after undoing
    def redo(self):
        self.index -= 1
        return self.changes[self.index]

    # "Fork" the history, keeping all previous history but erasing everything ahead of the current point
    def fork(self):
        for i in range(self.index+1):
            try: self.changes.pop(i)
            except Exception as e:
                log.write(f"History: Fork failed, exception: {e}")
        self.index = 0
