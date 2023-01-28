from collections import namedtuple

Row = namedtuple("Row",["subject","predicate","object"])

class Table:
    def __init__(self):
        self.rows = []
    def addRow(self,row):
        self.rows.append(row)
