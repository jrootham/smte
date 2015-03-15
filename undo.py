__author__ = 'jrootham'

import memento_undo.memento as memento
import display
import model
import tkMessageBox as box

ROOT, INSERT, DELETE, BACKSPACE, RIGHT, LEFT, UP, DOWN, SET_MARK = range(1, 10)

smte = None

def create_db(cursor):
    cursor.execute("BEGIN TRANSACTION;")

    memento.create_db(cursor)

    cursor.execute("ALTER TABLE state ADD export TEXT;")
    cursor.execute("ALTER TABLE state ADD mark_line INTEGER;")
    cursor.execute("ALTER TABLE state ADD mark_column INTEGER;")
    cursor.execute("ALTER TABLE state ADD tabsize INTEGER;")
    cursor.execute("ALTER TABLE state ADD select_start_line INTEGER;")
    cursor.execute("ALTER TABLE state ADD select_start_column INTEGER;")
    cursor.execute("ALTER TABLE state ADD select_end_line INTEGER;")
    cursor.execute("ALTER TABLE state ADD select_end_column INTEGER;")

    modify = "CREATE TABLE modify ("
    modify += "id INTEGER PRIMARY KEY,"
    modify += "data TEXT"
    modify += ");"

    cursor.execute(modify)

    mark = "CREATE TABLE mark ("
    mark += "id INTEGER PRIMARY KEY,"
    mark += "line INTEGER,"
    mark += "column INTEGER"
    mark += ");"

    cursor.execute(mark)

    selection = "CREATE TABLE selection ("
    selection += "id INTEGER PRIMARY KEY,"
    selection += "start_line INTEGER,"
    selection += "start_column INTEGER,"
    selection += "end_line INTEGER,"
    selection += "end_column INTEGER"
    selection += ");"

    cursor.execute(selection)

    number = "CREATE TABLE number ("
    number += "id INTEGER PRIMARY KEY,"
    number += "data INTEGER"
    number += ");"

    cursor.execute(number)

    fill_db(cursor)

    cursor.execute("END TRANSACTION;")

def fill_db(cursor):
    state = "INSERT INTO state (id, export,root,current,current_id,mark_line,mark_column,tabsize,"
    state += "select_start_line,select_start_column,select_end_line,select_end_column) "
    state += "VALUES (1, '', 1, 1, 1, 0, 0, 4, 0, 0, 0, 0);"

    cursor.execute(state)

    undo_redo = "INSERT INTO undo_redo (id, parent, sibling, child, type, data) "
    undo_redo += "VALUES (1, 0, 0, 0, 1, 0);"

    cursor.execute(undo_redo)

class SMTE(memento.Memento):
    def __init__(self, cursor):
        make_thing = \
            {
                ROOT:       make_root,
                INSERT:     make_insert,
                LEFT:       make_left,
                RIGHT:      make_right,
                UP:         make_up,
                DOWN:       make_down,
                DELETE:     make_delete,
                BACKSPACE:  make_backspace
            }

        memento.Memento.__init__(self, cursor, make_thing)
        self.model = model.Model(cursor)
        self.goto(self.model, self.current)
        display.display(self.model)
        display.set_focus()

    def unload(self):
        pass

def unload():
    global smte

    smte.unload()
    smte = None

def is_loaded():
    global smte

    result = not smte is None
    if not result:
        box.showerror("Edit Error", "File not loaded")
    return result

def do_undo():
    if is_loaded():
        pass

def do_redo():
    if is_loaded():
        pass

def key_pressed(char):
    if is_loaded() and len(char) == 1:
        insert(char)
    else:
        print len(char), char

def left_pressed():
    if is_loaded():
        left()

def right_pressed():
    if is_loaded():
        right()

def up_pressed():
    if is_loaded():
        up()

def down_pressed():
    if is_loaded():
        down()

def backspace_pressed():
    global smte

    if is_loaded():
        if smte.model.can_backspace():
            backspace()

def delete_pressed():
    global smte

    if is_loaded():
        if smte.model.can_delete():
            delete()

def tab_pressed():
    if is_loaded():
        tab();

def construct(thing):
    global smte

    smte.cursor.execute("BEGIN TRANSACTION;")
    smte.connect(thing)
    thing.redo(smte.model)
    display.display(smte.model)
    smte.draw_all()
    smte.save(smte.cursor)
    smte.cursor.execute("END TRANSACTION;")



# Root functions

def make_root(cursor, id, parent, data):
    return Root(id, parent)

class Root(memento.UndoRedo):
    def __init__(self, id, parent):
        memento.UndoRedo.__init__(self, id, parent)

    def name(self):
        return 'Rt'

    def colour(self):
        return 'black'

    def redo(self, model):
        model.reset()

# modify functions

def modify(cursor, data_id):
    result = cursor.execute("SELECT data FROM modify WHERE id=?;", (data_id,))
    return result.fetchone()[0]

class Modify(memento.UndoRedo):
    def __init__(self, id, parent, char):
        memento.UndoRedo.__init__(self, id, parent)
        self.char = char

    def save(self, cursor, type):
        memento.UndoRedo.save(self,cursor)
        modify_sql = "INSERT INTO modify (id,data) VALUES(?,?)"
        modify_id = smte.next()
        cursor.execute(modify_sql, (modify_id, self.char))
        update_sql = 'UPDATE undo_redo SET type=?,data=? WHERE id=?;'
        cursor.execute(update_sql, (type, modify_id, self.id))

# Insert functions

def make_insert(cursor, id, parent, data_id):
    return Insert(id, parent, modify(cursor, data_id))

def insert(char):
    global smte
    construct(Insert(smte.next(), smte.current, char))


class Insert(Modify):
    def __init__(self, id, parent, char):
        Modify.__init__(self, id, parent, char)

    def name(self):
        return 'In'

    def colour(self):
        return 'green'

    def redo(self, model):
        model.char(self.char)

    def undo(self, model):
        model.backspace(len(self.char))

    def save(self, cursor):
        Modify.save(self, cursor, INSERT)
# Tab

def tab():
    global smte
    construct(Insert(smte.next(), smte.current, smte.model.make_tab()))

# Delete

def make_delete(cursor, id, parent, data_id):
    return Delete(id, parent, modify(cursor, data_id))

def delete():
    global smte

    char = smte.model.next_char()
    if not char is None:
        construct(Delete(smte.next(), smte.current, char))


class Delete(Modify):
    def __init__(self, id, parent, char):
        Modify.__init__(self, id, parent, char)

    def name(self):
        return 'Dl'

    def colour(self):
        return 'red'

    def redo(self, model):
        model.delete(len(self.char))

    def undo(self, model):
        pass

    def save(self, cursor):
        Modify.save(self, cursor, DELETE)

# Backspace

def make_backspace(cursor, id, parent, data_id):
    return Backspace(id, parent, modify(cursor, data_id))

def backspace():
    global smte

    char = smte.model.last_char()
    if not char is None:
        construct(Backspace(smte.next(), smte.current, char))


class Backspace(Modify):
    def __init__(self, id, parent, char):
        Modify.__init__(self, id, parent, char)

    def name(self):
        return 'Bs'

    def colour(self):
        return 'red'

    def redo(self, model):
        model.backspace(len(self.char))

    def save(self, cursor):
        Modify.save(self, cursor, BACKSPACE)

# Move

def move_mark(cursor, mark_id):
    return cursor.execute("SELECT line,column FROM mark WHERE id=?;", (mark_id,)).fetchone()

class Move(memento.UndoRedo):
    def __init__(self, id, parent, mark_line, mark_column):
        memento.UndoRedo.__init__(self, id, parent)
        self.line = mark_line
        self.column = mark_column

    def colour(self):
        return 'blue'

    def save(self, cursor, type):
        memento.UndoRedo.save(self,cursor)
        mark_sql = "INSERT INTO mark (id,line,column) VALUES(?,?,?)"
        mark_id = smte.next()
        cursor.execute(mark_sql, (mark_id, self.line, self.column))
        update_sql = 'UPDATE undo_redo SET type=?,data=? WHERE id=?;'
        cursor.execute(update_sql, (type, mark_id, self.id))

# Left functions

def make_left(cursor, id, parent, mark_id):
    mark = move_mark(cursor, mark_id)
    return Left(id, parent, mark[0], mark[1])

def left():
    global smte
    construct(Left(smte.next(), smte.current, smte.model.mark_line, smte.model.mark_column))


class Left(Move):
    def __init__(self, id, parent, mark_line, mark_column):
        Move.__init__(self, id, parent, mark_line, mark_column)

    def name(self):
        return 'L'

    def redo(self, model):
        model.left()

    def save(self, cursor):
        Move.save(self, cursor, LEFT)

# Right functions

def make_right(cursor, id, parent, mark_id):
    mark = move_mark(cursor, mark_id)
    return Right(id, parent, mark[0], mark[1])

def right():
    global smte
    construct(Right(smte.next(), smte.current, smte.model.mark_line, smte.model.mark_column))


class Right(Move):
    def __init__(self, id, parent, mark_line, mark_column):
        Move.__init__(self, id, parent, mark_line, mark_column)

    def name(self):
        return 'R'

    def redo(self, model):
        model.right()

    def save(self, cursor):
        Move.save(self, cursor, RIGHT)

# Up functions

def make_up(cursor, id, parent, mark_id):
    mark = move_mark(cursor, mark_id)
    return Up(id, parent, mark[0], mark[1])

def up():
    global smte
    construct(Up(smte.next(), smte.current, smte.model.mark_line, smte.model.mark_column))


class Up(Move):
    def __init__(self, id, parent, mark_line, mark_column):
        Move.__init__(self, id, parent, mark_line, mark_column)

    def name(self):
        return 'U'

    def redo(self, model):
        model.up()

    def save(self, cursor):
        Move.save(self, cursor, UP)

# Down functions

def make_down(cursor, id, parent, mark_id):
    mark = move_mark(cursor, mark_id)
    return Down(id, parent, mark[0], mark[1])

def down():
    global smte
    construct(Down(smte.next(), smte.current, smte.model.mark_line, smte.model.mark_column))


class Down(Move):
    def __init__(self, id, parent, mark_line, mark_column):
        Move.__init__(self, id, parent, mark_line, mark_column)

    def name(self):
        return 'U'

    def redo(self, model):
        model.down()

    def save(self, cursor):
        Move.save(self, cursor, DOWN)
