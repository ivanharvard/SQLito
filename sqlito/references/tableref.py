from sqlito.exceptions import SQLitoTypeError
from sqlito.references.columnref import ColumnReference

class TableReference:
    """
    Table references are used internally by the .execute() method of certain  
    classes to refer to a table in the database without storing the table itself
    under a variable.

    For instance:
    ```
    employees = (Query(db)
                .CREATE_TABLE("employees")
                .COLUMN("name", TEXT)
                .execute())
    ```

    This will create a table reference for the "employees" table, which can then
    be used in queries like:

    ```
    result = (Query(db)
              .SELECT(employees.name)
              .FROM("employees")
              .execute())
    ```
    """
    def __init__(self, name, columns):
        """
        Initializes a TableReference with a name and a list of columns. Creates
        the attributes for each column in the table, allowing for easy access
        to the columns as attributes of the TableReference instance.
        
        :param name: The name of the table.
        :type name: str
        :param columns: A list of column names in the table.
        :type columns: list of str
        
        :raises SQLitoTypeError: If the name is not a string or columns is not a list of strings.
        """
        if not isinstance(name, str):
            raise SQLitoTypeError(f"Table name must be a string.")
        if not isinstance(columns, list):
            raise SQLitoTypeError(f"Columns must be a list of strings.")

        self._name = name
        self._columns = columns

        for col in columns:
            if not isinstance(col, str):
                raise SQLitoTypeError(f"Column name must be a string.", str, col)
            
            setattr(self, col, ColumnReference(name, col))

    # Useful to stop pylance from complaining about missing attributes
    def __getattr__(self, name: str) -> ColumnReference:
        if name in self._columns:
            return ColumnReference(self._name, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

