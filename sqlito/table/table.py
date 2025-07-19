from sqlito.exceptions import SQLitoSyntaxError, SQLitoTypeError
from sqlito.types import SQLITO_AFFINITIES
from sqlito.types.internal import ColumnType

class Table:
    def __init__(self, name, columns, data=[], strict=False):
        """
        Initializes and validates the Table with a name, its column names and 
        types, and data. The name is a unique identifier for the table, and 
        the data is a list of dictionaries representing rows in the table, 
        where each dictionary's keys are column names and values are 
        the corresponding row values.

        :param name: The name of the table.
        :type name: str
        :param columns: A list of column names and their types. Column type \
                        defaults to BLOB if not specified.
        :type columns: list of dicts
        :param data: The data for the table, a list of dictionaries.
        :type data: list of dicts
        :param strict: If True, column values must conform to the declared type.
        :type strict: bool
        """
        self.name = name
        self.columns = columns
        self.data = data
        self.strict = strict

        self._validate_table()

    def rename(self, new_name):
        """
        Renames the table to a new name.

        :param new_name: The new name for the table.
        :type new_name: str
        """
        if not isinstance(new_name, str):
            raise SQLitoTypeError("Table name must be a string.", str, new_name)
        self.name = new_name

    def add_columns(self, new_columns):
        """
        Adds new columns to the table. The new columns must be a list of
        ColumnTypes.  
        """
        if not isinstance(new_columns, list):
            raise SQLitoTypeError("New columns must in be a list.", list, new_columns)
        
        for col in new_columns:
            if not isinstance(col, ColumnType):
                raise SQLitoTypeError("Each column must be an instance of ColumnType.", ColumnType, col)
            self.columns[col.name] = col.type

    def _validate_table(self):
        """
        Validates the columns of the table to ensure they are consistent across 
        all rows.

        - The table must have a name (string).
        - At least one column must exist, declared in the first row of data.
        - No duplicate column names are allowed.
        - All rows must have the same columns as declared in the first row.
        """
        # Check for table name
        if not self.name or not isinstance(self.name, str):
            raise SQLitoSyntaxError("Table must have a name.")

        # Check for existence of columns
        if not self.columns:
            raise SQLitoSyntaxError("Table must have at least one column.")

        # Check for duplicates in columns
        if len(self.columns) != len(set(self.columns)):
            raise SQLitoSyntaxError("Duplicate columns found in the table.")
        
        for col, col_type in self.columns.items():
            # Check all column names are strings and types are valid SQLito affinities
            if not isinstance(col, str):
                raise SQLitoTypeError(f"Column name must be a string.", "str", type(col).__name__)
            if not isinstance(col_type, SQLITO_AFFINITIES):
                raise SQLitoTypeError(f"Column type must be a valid SQLito type.", "SQLITO_AFFINITY", type(col_type).__name__)

        # Check if data is in a list
        if not isinstance(self.data, list):
            raise SQLitoSyntaxError("Table data must be a list.")

        # Check if all rows have the same columns
        for i, row in enumerate(self.data):
            if not isinstance(row, dict):
                raise SQLitoSyntaxError("Each row in the table must be a dictionary.")

            row_cols = list(row.keys())
            if sorted(row_cols) != sorted(self.columns):
                raise SQLitoSyntaxError(f"Row {i} has inconsistent columns: {row_cols} != {self.columns}")
            

