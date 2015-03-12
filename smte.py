#!/usr/bin/python

__author__ = 'jrootham'

import Tkinter as tk
import tkMessageBox as box
import tkFont

import file
import undoMenu
import display
import undo

class SMTE(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        display.make()
        makeMenu(master)

def makeMenu(parent):
    global  __dependencies

    top = parent.winfo_toplevel()
    menuBar = tk.Menu(top)
    top['menu'] = menuBar
    file.menu(menuBar, __dependencies)
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

    smte.master.title("Simple Minded Text Editor " + separator + name)

__dependencies = {
    'loaded': False,
    'display': display.display,
    'set_title': set_title}

root = tk.Tk()
smte = SMTE(master = root)

fonts=list(tkFont.families())
fonts.sort()
print '\n'.join(fonts)

set_title("")
smte.mainloop()

