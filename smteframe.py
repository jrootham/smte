#!/usr/bin/python

__author__ = 'jrootham'

import tkinter as tk

import file
import undoMenu
import display
import undo

class SMTEFrame(tk.Frame):
    def __init__(self, master=None):
        global  __dependencies

        tk.Frame.__init__(self, master)
        self.pack()

        display.make()
        makeMenu(master, self)

def makeMenu(parent, frame):
    global  __dependencies

    top = parent.winfo_toplevel()
    menuBar = tk.Menu(top)
    top['menu'] = menuBar
    file.menu(menuBar, __dependencies, frame)
    undoMenu.menu(menuBar, __dependencies)
    help(menuBar)


def help(menuBar):
    helpMenu = tk.Menu(menuBar)
    menuBar.add_cascade(label='Help', menu=helpMenu)
    helpMenu.add_command(label='About', command=__about)

def __about():
    box.showinfo("About", "Test bed for branching undo/redo\nGPL licenced")

def set_title(name):
    if len(name) > 0:
        separator = " - "
    else:
        separator = ""

    frame.master.title("Simple Minded Text Editor " + separator + name)

__dependencies = {
    'loaded':       False,
    'display':      display.display,
    'set_title':    set_title,
    'clear':        display.clear
}

root = tk.Tk()
frame = SMTEFrame(master = root)
set_title("")
frame.mainloop()

