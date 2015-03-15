__author__ = 'jrootham'

import tkMessageBox as box
import Tkinter as tk
import undo

__dependencies = None
__tree = None

def menu(menuBar, dependencies):
    global __dependencies

    __dependencies = dependencies

    undoMenu = tk.Menu(menuBar)
    menuBar.add_cascade(label='Undo', menu= undoMenu)
    undoMenu.add_command(label='Undo', command=do_undo)
    undoMenu.add_command(label='Redo', command=do_redo)
    undoMenu.add_command(label='Show', command=show)
    undoMenu.add_command(label='Tag', command=tag)
    undoMenu.add_command(label='Go to tag', command=goto_tag)

def do_undo():
    undo.do_undo()

def do_redo():
    undo.do_redo()

def show():
    global __tree

    if __dependencies['loaded']:
        __tree = tk.Toplevel()
        __tree.title("Undo/Redo Tree")
        __tree.protocol("WM_DELETE_WINDOW", close_tree)
        canvas = tk.Canvas(__tree, bg='white')
        canvas.pack(fill=tk.BOTH, expand=1)

        undo.smte.open_tree(canvas)
        canvas.bind("<Configure>", redraw)
    else:
        box.showerror("Show Error", "No file loaded")

def close_tree():
    undo.smte.close_tree()
    __tree.destroy()

def redraw(event):
    undo.smte.draw_all()

def tag():
    pass

def goto_tag():
    pass

