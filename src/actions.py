# Ink Editor - actions.py
# github.com/leftbones/ink

# --------------------------------------------------------------------------------
# Action
# --------------------------------------------------------------------------------

class Action:
    def __init__(self, commands, callback, description=None, usage=None):
        self.commands = commands
        self.callback = callback
        self.description = description
        self.usage = usage


# --------------------------------------------------------------------------------
# ActionHandler
# --------------------------------------------------------------------------------

class ActionHandler:
    def __init__(self, terminal):
        self.terminal = terminal
        self.history = []
        self.error = None

        self.actions = {
            # Close the active window, exits the app if the active window is the only window
            Action(
                commands = ['quit', 'q'],
                callback = self.terminal.do_exit,
                description = 'Exit the active window',
                usage = 'quit/q'
            ),

            # Save the current window contents
            Action(
                commands = ['save', 's', 'w'],
                callback = self.terminal.do_save,
                description = 'Save the current file',
                usage = 'save/s/w [FILEPATH]'
            ),

            # Save the current window contents and close the window
            Action(
                commands = ['savequit', 'sq', 'wq'],
                callback = (self.terminal.do_save, self.terminal.do_exit),
                description = 'Save the current file and quit',
                usage = 'savequit/ss/wq'
            ),

            # Open a file in the current window
            Action(
                commands = ['open', 'o', 'e'],
                callback = self.terminal.do_open,
                description = 'Open a file for editing',
                usage = 'open/o/e [FILEPATH]'
            ),
        }

    def parse_input(self, prompt_input):
        self.error = None

        # Split input by spaces and extract base command
        input_split = prompt_input.split(' ')
        base_cmd = input_split[0]
        args = []
        flags = []

        # Extract args and flags from remaining input
        for arg in input_split[1:]:
            if arg.startswith('-'): flags.append(arg.replace('-', ''))
            else: args.append(arg)

        # Attempt to process command with flags/args included
        for action in self.actions:
            if base_cmd in action.commands:
                self.history.append(prompt_input)
                if type(action.callback) == tuple:
                    for callback in action.callback: callback()
                else:
                    action.callback(*flags, *args)
                return

        # Return error if command is not found
        self.error = self.terminal.send_alert("Error", [f"Command '{prompt_input}' is invalid.\n"], 10)
#        self.error = f"Command '{prompt_input}' is invalid."
        return self.error
