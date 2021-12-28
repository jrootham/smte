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
    undoMenu.add_command(label='Undo ^z', command=do_undo)
    undoMenu.add_command(label='Redo ^y', command=do_redo)
    undoMenu.add_command(label='Show ^s', command=show)
    undoMenu.add_command(label='Tag ^t', command=tag)
    undoMenu.add_command(label='Go to tag ^g', command=goto_tag)

def do_undo():
    undo.do_undo()

def do_redo():
    undo.do_redo()
    
class Tree:
    def __init__(self, container):
        container.title("Undo/Redo Tree")
        container.protocol("WM_DELETE_WINDOW", self.close_tree)
        magnify = tk.Frame(container)

        button = tk.Button(magnify, text = "Magnify")
        button.pack(side = tk.LEFT)

        magnify.pack(fill = tk.X)

        canvas = tk.Canvas(container, bg='white')
        canvas.pack(fill = tk.BOTH, expand = 1)

        context = tk.Frame(container)

        label = tk.Label(context, text = 'Context ')
        label.pack(side = tk.LEFT)

        self.display = tk.Canvas(context, bg = 'white', height = 3 * undo.HEIGHT)
        self.display.pack(side = tk.LEFT, fill = tk.X, expand = 1)

        context.pack(fill = tk.X)


        undo.smte.open_tree(canvas)
        canvas.bind("<Configure>", make_redraw(self))
        canvas.bind("<Enter>", enter)
        canvas.bind("<Leave>", leave)

def show():
    global __tree, __display

    if __dependencies['loaded']:
        __tree = Tree(tk.Toplevel())
    else:
        box.showerror("Show Error", "No file loaded")

def close_tree():
    undo.smte.close_tree()
    __tree.destroy()

def enter(event):
    event.widget.bind('<Motion>', move)

def leave(event):
    event.widget.unbind('<Motion>')

def move(event):
    global __display

    __display.delete(tk.ALL)
    __display.create_text((0, 0), anchor = tk.NW, text = str(event.x) + ' ' + str(event.y))


#function findUndoRedo(column, tree, target) {
#  if (tree.depth == target.depth && column == target.column) {
#    return {found: true, element: tree};
#  }
#  var newColumns = 1;
#
#   if (tree.down != null){
#     result = findUndoRedo(column, tree.down, target);
#     if (result.found){
#       return result;
#     }
#     else
#     {
#       newColumns = result.columns;
#     }
#   }
#
#   if (tree.across != null) {
#     result = findUndoRedo(column + newColumns, tree.across, target);
#     if (result.found) return result;
#     newColumns += result.columns;
#   }
#
#   return {found : false, columns: newColumns};
# }


def redraw(event):
    undo.smte.draw_all()

def tag():
    pass

def goto_tag():
    pass

