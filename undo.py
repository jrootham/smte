__author__ = 'jrootham'

import memento_undo.memento as memento
import display
import model

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
        make_thing = {ROOT: make_root, INSERT: make_insert}
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

def key_pressed(char):
    global smte

    if (not smte is None) and len(char) == 1:
        insert(char)
        display.display(smte.model)
    else:
        print len(char), char

def backspace():
    pass

def delete():
    pass

def construct(thing):
    global smte

    smte.cursor.execute("BEGIN TRANSACTION;")
    smte.connect(thing)
    thing.redo(smte.model)
    display.display(smte.model)
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

# Insert functions

def make_insert(cursor, id, parent, data_id):
    result = cursor.execute("SELECT data FROM modify WHERE id=?;", (data_id,))
    row = result.fetchone()

    return Insert(id, parent, row[0])

def insert(char):
    global smte

    construct(Insert(smte.next(), smte.current, char))


class Insert(memento.UndoRedo):
    def __init__(self, id, parent, char):
        memento.UndoRedo.__init__(self, id, parent)
        self.char = char

    def name(self):
        return 'In'

    def colour(self):
        return 'green'

    def redo(self, model):
        model.char(self.char)

    def save(self, cursor):
        memento.UndoRedo.save(self,cursor)
        modify_sql = "INSERT INTO modify (id,data) VALUES(?,?)"
        modify_id = smte.next()
        cursor.execute(modify_sql, (modify_id, self.char))
        update_sql = 'UPDATE undo_redo SET type=?,data=? WHERE id=?;'
        cursor.execute(update_sql, (INSERT, modify_id, self.id))

# Move

class Move(memento.UndoRedo):
    def __init__(self, id, parent, model):
        memento.UndoRedo.__init__(self, id, parent)
        self.line = model.mark_line
        self.column = model.mark_column

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

def make_left(cursor, id, parent, model):
    return Left(id, parent, model)

def left():
    global smte

    construct(Left(smte.next(), smte.current, smte.model))


class Left(Move):
    def __init__(self, id, parent, model):
        Move.__init__(self, id, parent, model)

    def name(self):
        return 'L'

    def redo(self, model):
        model.left()

    def save(self, cursor):
        Move.save(cursor, LEFT)

# Right functions

def make_right(cursor, id, parent):
    return Right(id, parent)

def right():
    global smte

    construct(Right(smte.next(), smte.current))


class Right(Move):
    def __init__(self, id, parent):
        Move.__init__(self, id, parent)

    def name(self):
        return 'R'

    def redo(self, model):
        model.right()

    def save(self, cursor):
        Move.save(cursor, RIGHT)

# Up functions

def make_up(cursor, id, parent):
    return Right(id, parent)

def up():
    global smte

    construct(Up(smte.next(), smte.current))


class Up(Move):
    def __init__(self, id, parent):
        Move.__init__(self, id, parent)

    def name(self):
        return 'U'

    def redo(self, model):
        model.right()

    def save(self, cursor):
        Move.save(cursor, UP)
