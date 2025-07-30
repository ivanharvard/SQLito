from sqlito.types.internal import RowType, ColumnType
from sqlito.exceptions import SQLitoSyntaxError, SQLitoTypeError

class VirtualTable:
    """
    Represents a virtual table in the database.
    
    This is a lightweight representation of a table that is the product of 
    certain query operations, such as a SELECT query.
    """
    def __init__(self, alias, columns, rows):
        """
        Initializes the VirtualTable with an alias, columns, and rows.
        
        :param alias: The alias for the virtual table.
        :type alias: str
        :param columns: The columns of the virtual table.
        :type columns: list[ColumnType]
        :param rows: The data rows of the virtual table.
        :type rows: list[dict[Any, RowType]]
        """
        self.alias = alias
        self.columns = columns
        self.rows = rows

        self._validate_vtable()

    def _validate_vtable(self):
        if not isinstance(self.alias, str):
            raise SQLitoTypeError("alias must be a string")
        if not isinstance(self.columns, list) or not all(isinstance(col, ColumnType) for col in self.columns):
            raise SQLitoTypeError("columns must be a list of ColumnType instances")
        if not isinstance(self.rows, list):
            raise SQLitoTypeError("rows must be a list of dictionaries with primary keys as keys and RowTypes as values")
        for row in self.rows:
            if not isinstance(row, dict):
                raise SQLitoTypeError("row must be a dictionary with primary keys as keys and RowTypes as values")
            for value in row.values():
                if not isinstance(value, RowType):
                    raise SQLitoTypeError(f"Row value must be an instance of RowType, not {type(value)}")
                

