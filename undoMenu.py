__author__ = 'jrootham'

import tkMessageBox as box
import Tkinter as tk
import undo

__dependencies = None

def menu(menuBar, dependencies):
    global __dependencies

    __dependencies = dependencies

    undoMenu = tk.Menu(menuBar)
    menuBar.add_cascade(label='Undo', menu= undoMenu)
    undoMenu.add_command(label='Undo', command=__undo)
    undoMenu.add_command(label='Redo', command=__redo)
    undoMenu.add_command(label='Show', command=__show)
    undoMenu.add_command(label='Tag', command=__tagHandler)
    undoMenu.add_command(label='Go to tag', command=__gotoTagHandler)

def __undo():
    pass

def __redo():
    pass

def __show():
    if __dependencies['loaded']:
        top = tk.Toplevel()
        top.title("Undo/Redo Tree")
        canvas = tk.Canvas(top, bg='white')
        canvas.pack(fill=tk.BOTH, expand=1)

        undo.smte.draw_all(canvas)
    else:
        box.showerror("Show Error", "Mo file loaded")


def __tagHandler():
    pass

def __gotoTagHandler():
    pass

