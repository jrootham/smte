__author__ = 'jrootham'

import os.path

import tkMessageBox as box
import sqlite3 as sq
import Tkinter as tk
import tkSimpleDialog as tksd
import tkFileDialog as tkfd

import undo

def menu(menuBar,  dependencies):
    global __dependencies

    __dependencies = dependencies

    fileMenu = tk.Menu(menuBar)
    menuBar.add_cascade(label='File', menu= fileMenu)

    fileMenu.add_command(label='New', command=__newFile)
    fileMenu.add_command(label='Open', command=__openFile)
    fileMenu.add_command(label='Close', command=__closeFile)
    fileMenu.add_command(label='Export', command=__export)
    fileMenu.add_command(label='Export As', command=exportAs)

def __newFile():
    global __dependencies

    if not __dependencies['loaded']:
        response = tksd.askstring("File name", "Enter file name\nType is .smte")
        if not response is None:
            filename = response +".smte"

            if (not os.path.isfile(filename)):
                connect = set_connect(filename)
                undo.create_db(connect.cursor())
                connect.close()

                load(filename)
            else:
                box.showerror("Create Error", "File already exists")
        else:
            box.showerror("Create Error", "Create cancelled")
    else:
        box.showerror("Create Error", "File already loaded")

def __openFile():
    global __dependencies

    if not __dependencies['loaded']:
        filename = tkfd.askopenfilename(defaultextension='.smte', filetypes=[('smte files', '.smte')])
        if filename != "":
            load(filename)
        else:
            box.showerror("Open Error", "No file specified")
    else:
        box.showerror("Open Error", "File already loaded")

def load(filename):
    global __dependencies, __connect, __events

    __connect = set_connect(filename)
    __dependencies["set_title"](filename)
    __dependencies['loaded'] = True
    undo.smte = undo.SMTE(__connect.cursor())

def __closeFile():
    if __dependencies['loaded']:
        __connect.close()
        __dependencies["loaded"] = False
        undo.unload()

def __export():
    if __dependencies['loaded']:
        if undo.smte.model.export_name != '':
            undo.smte.model.export()
        else:
            exportAs()

def exportAs():
    if __dependencies['loaded']:
        filename = tkfd.asksaveasfilename()
        if filename != '':
            undo.smte.model.export_name = filename
            undo.smte.model.export()

def set_connect(filename):
    connect = sq.connect(filename)
    connect.isolation_level = None

    return connect

