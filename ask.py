__author__ = 'jrootham'

import tkinter as tk
import tkinter.simpledialog as simple

class Ask:
    def __init__(self):
        pass

    def ask(self, current):
        if current.sibling is None:
            return current
        else:
            question = Question(current)
            if question.result is None:
                return current
            else:
                return question.result

class Question(tk.simpledialog):
    def __init__(self, current):
        tk.simpledialog.__init__()
        self.current = current

    def buttonbox(self):
        pass

    def body(self, master):

        box = tk.Frame(self)

        standard = None
        current = self.current
        while not current is None:
            button = tk.Button(
                box,
                text = current.ask_text(),
                background = current.colour(),
                foreground = "white",
                command = make_command(self, current)
            )
            button.pack(side=tk.LEFT, padx=5, pady=5)

            if standard is None:
                standard = button

            current = current.sibling

        box.pack()

        return standard

def make_command(dialogue, undo_redo):
    def command():
        dialogue.result = undo_redo

        dialogue.ok(None)
    return command
