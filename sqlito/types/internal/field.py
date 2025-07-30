from sqlito.exceptions import SQLitoNotImplemented, SQLitoTypeError, SQLitoValueError

class Field:
    def __init__(self, column_name, table_name=None):
        if not isinstance(column_name, str):
            raise SQLitoTypeError("Column name must be a string")

        if table_name is not None and not isinstance(table_name, str):
            raise SQLitoTypeError("Table name must be a string or None")

        self.name = column_name
        self.table = table_name
    
    def correlate(self, table):
        """
        Correlate the field with a specific table.

        :param table: The name of the table to correlate with.
        :type table: str

        :return: The field with the table correlated.
        :rtype: Field
        """
        if not isinstance(table, str):
            raise TypeError("Table name must be a string.")

        self.table = table
        return self
    
    def evaluate(self, db):
        """
        Returns a list of the data for this column in the provided table.
        """
        from sqlito.database import Database

        if not isinstance(db, Database):
            raise SQLitoTypeError("db must be an instance of Database")

        if not self.table:
            raise SQLitoValueError("Field must be correlated with a table before evaluation.")
        
        if self.table not in db:
            raise SQLitoValueError(f"Field '{self.name}' references unknown table '{self.table}'.")

        return db.get_table(self.table).get_column_data(self.name)

    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return isinstance(other, Field) and self.name == other.name and self.table == other.table

    def __hash__(self):
        return hash((self.table, self.name))
