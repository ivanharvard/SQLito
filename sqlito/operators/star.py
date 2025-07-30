from sqlito.exceptions import SQLitoTypeError
from sqlito.table import Table

class Star:
    def __init__(self):
        self._resolved = False
        self._columns = None

    def resolve(self, table):
        if not isinstance(table, Table):
            raise SQLitoTypeError("Star operator can only be resolved with a Table instance.")
        
        self._columns = table.columns
        self._resolved = True

    def is_resolved(self):
        return self._resolved

    def __str__(self):
        return "*"
    
STAR = Star()