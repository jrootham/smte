__author__ = 'jrootham'

class Model:

    def __init__(self, cursor):
        self.reset()
        self.load(cursor)

    def reset(self):
        self.contents = ['']
        self.mark_line = 0
        self.mark_column = 0
        self.start_select_line = 0
        self.start_select_column = 0
        self.end_select_line = 0
        self.end_select_column = 0
        self.tabsize = 4

    def save(self, cursor):
        state_sql = "UPDATE state SET export=?,mark_line=?,mark_column=?,tabsize=?,"
        state_sql += "start_select_line=?,start_select_column=?,end_select_line=?,end_select_column=?;"
        cursor.execute(state_sql, (self.export,self.mark_line, self.mark_column, self.tabsize,
        self.start_select_line, self.start_select_column, self.end_select_line, self.end_select_column))

    def load(self, cursor):
        data = cursor.execute("SELECT export,tabsize FROM state WHERE id=1;").fetchone()
        self.export_name = data[0]
        self.tabsize = data[1]

    def char(self, text):
        if text == '\r':
            self.new_line()
        else:
            self.insert(text)

    def insert(self, text):
        line_index = self.mark_line
        current = self.contents[line_index]
        self.contents[line_index] = current[:self.mark_column] + text + current[self.mark_column:]
        self.mark_column += len(text)

#        for i in range(1, len(textList)):
#            self.contents.insert(start_line + i, textList[i])

#        end_line = start_line + len(textList) - 1
#        self.contents[end_line] += current[self.mark_column:]
#        self.mark_line = end_line

    def new_line(self):
        line_index = self.mark_line
        current = self.contents[line_index]
        self.contents[line_index] = current[:self.mark_column]
        self.contents.insert(line_index + 1, current[self.mark_column:])
        self.mark_column = 0
        self.mark_line += 1

    def export(self):
        file = open(self.export_name, 'w')
        file.write('\n'.join(self.contents))
        file.close()

    def up(self):
        if self.mark_line > 0:
            self.mark_line -= 1
        self.set_column()

    def down(self):
        if self.mark_line < len(self.contents) - 1:
            self.mark_line += 1
        self.set_column()

    def set_column(self):
        self.mark_column = min(self.mark_column, len(self.contents[self.mark_line]))

    def left(self):
        if self.mark_column != 0:
            self.mark_column -= 1
        else:
            if self.mark_line > 0:
                self.mark_line -= 1
                self.mark_column = len(self.contents[self.mark_line])

    def right(self):
        if self.mark_column < len(self.contents[self.mark_line]):
            self.mark_column += 1
        else:
            if self.mark_line < len(self.contents) - 1:
                self.mark_line += 1
                self.mark_column = 0

    def can_delete(self):
        return self.mark_line < len(self.contents) - 1 or self.mark_column < len(self.contents[self.mark_line])

    def next_char(self):
        if self.mark_column == len(self.contents[self.mark_line]):
            char = '\n'
        else:
            char = self.contents[self.mark_line][self.mark_column:self.mark_column + 1]
        return char

    def delete(self, count):
        if self.mark_column + count <= len(self.contents[self.mark_line]):
            line = self.contents[self.mark_line]
            self.contents[self.mark_line] = line[:self.mark_column] + line[self.mark_column + count:]
        else:
            self.contents[self.mark_line] += self.contents[self.mark_line + 1]
            self.contents.pop(self.mark_line + 1)

    def can_backspace(self):
        return self.mark_line > 0 or self.mark_column > 0

    def last_char(self):
        if self.mark_column == 0:
            char = '\n'
        else:
            char = self.contents[self.mark_line][self.mark_column - 1:self.mark_column]
        return char

    def backspace(self, count):
        self.left()
        self.delete(count)

    def make_tab(self):
        return (self.tabsize - (self.mark_column % self.tabsize)) * " "
