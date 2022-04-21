# Error Handling + Messages
# Needs to be fleshed out more

class Error:
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return f"ERROR: {self.message}"

# Any error from Python that I don't feel like handling
class PythonError(Error):
    def __init__(self, message):
        super().__init__(message)

    def __repr__(self):
        return f"{self.message}"


class CmdNotFoundError(Error):
    def __init__(self, message):
        super().__init__(message)


class InvalidArgsError(Error):
    def __init__(self, message):
        super().__init__(message)
