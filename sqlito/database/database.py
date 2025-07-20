from sqlito.table.table import Table
from sqlito.exceptions import SQLitoTypeError, SQLitoValueError


class Database:
    def __init__(self, tables=None):
        """
        Initializes the Database with an optional list of tables.

        :param tables: A list of Table instances to initialize the database with.
        :type tables: list of Table
        """
        self.tables = tables if tables is not None else {}

        self._validate_database()

    def _validate_database(self):
        """
        Validates the database by checking the types of the tables and 
        uniqueness of table names.
        """
        if not isinstance(self.tables, dict):
            raise SQLitoTypeError("Tables must be a dictionary mapping table names to Table instances.", dict, self.tables)
        
        for name, table in self.tables.items():
            if not isinstance(name, str):
                raise SQLitoTypeError("Table names must be strings.", str, name)

            if not isinstance(table, Table):
                raise SQLitoTypeError(f"Table '{name}' must be an instance of Table.", Table, table)
            
            if not table.name or not table.name == name:
                raise SQLitoValueError(f"Table name '{name}' must be a non-empty string that matches the provided table's name '{table.name}'.")        
    
        if len(self.tables) != len(set(self.tables.keys())):
            raise SQLitoValueError("Table names must be unique in the database.")
        
    def add_table(self, table):
        """
        Adds a table to the database.
        
        :param table: The Table instance to add.
        :type table: Table
        
        :raises SQLitoTypeError: If the table is not an instance of Table.
        """
        if not isinstance(table, Table):
            raise SQLitoTypeError("The table must be an instance of Table.", Table, table)
        
        if table.name in self.tables:
            raise SQLitoValueError(f"Table '{table.name}' already exists in the database.")
        
        self.tables[table.name] = table

    def remove_table(self, name):
        """
        Removes a table from the database by its name.

        :param name: The name of the table to remove.
        :type name: str

        :return: The removed Table instance.
        """
        return self.tables.pop(name)
