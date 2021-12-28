__author__ = 'jrootham'

import tkinter as tk
import undo

__canvas = None

def make():
    global __canvas

    __canvas = tk.Canvas(bg='white')
    __canvas.pack(fill=tk.BOTH, expand=1)
    __canvas.bind("<Key>", key_pressed)
    __canvas.bind("<BackSpace>", backspace)
    __canvas.bind("<Delete>", delete)
    __canvas.bind("<Left>", left)
    __canvas.bind("<Right>", right)
    __canvas.bind("<Up>", up)
    __canvas.bind("<Down>", down)
    __canvas.bind("<Tab>", tab)
    __canvas.bind("<Control-z>", do_undo)
    __canvas.bind("<Control-y>", do_redo)
    set_focus()

def set_focus():
    global __canvas

    __canvas.focus_set()

def key_pressed(event):
    undo.key_pressed(event.char)

def backspace(event):
     undo.backspace_pressed()

def delete(event):
    undo.delete_pressed()

def left(event):
    undo.left_pressed()

def right(event):
    undo.right_pressed()

def up(event):
    undo.up_pressed()

def down(event):
    undo.down_pressed()

def tab(event):
    undo.tab_pressed()

def do_undo(event):
    undo.do_undo()

def do_redo(event):
    undo.do_redo()

def clear():
    global __canvas
    __canvas.delete(tk.ALL)

def display(model):
    global __canvas

    __canvas.delete(tk.ALL)

    y = 0
    for line in model.contents:
        text = line.expandtabs(model.tabsize)
        __canvas.create_text((0,y), text = text, fill = "black", anchor = tk.NW, font =("Ubuntu Mono", 14))
        y += undo.HEIGHT

    x = model.mark_column * undo.WIDTH
    y = model.mark_line * undo.HEIGHT

    __canvas.create_line(x, y, x, y + undo.HEIGHT)

    set_focus()