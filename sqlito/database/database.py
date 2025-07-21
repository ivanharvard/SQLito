from typing import Any
from sqlito.table.table import Table
from sqlito.exceptions import SQLitoTypeError, SQLitoValueError


class Database:
    def __init__(self, name, tables=None):
        """
        Initializes the Database with an optional list of tables.

        :param name: The name of the database.
        :type name: str
        :param tables: A list of Table instances to initialize the database with.
        :type tables: list of Table
        """
        self.name = name
        self.tables = tables if tables is not None else {}

        self._validate_database()

    def rename(self, new_name):
        """
        Renames the database to a new name.

        :param new_name: The new name for the database.
        :type new_name: str

        :raises SQLitoTypeError: If the new name is not a string.
        """
        if not isinstance(new_name, str) or not new_name:
            raise SQLitoTypeError("Database name must be a non-empty string.", str, new_name)

        self.name = new_name

    def _validate_database(self):
        """
        Validates the database by checking the types of the tables and 
        uniqueness of table names.
        """
        if not isinstance(self.name, str) or not self.name:
            raise SQLitoTypeError("Database name must be a non-empty string.", str, self.name)

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

    def pop_table(self, name):
        """
        Removes and returns a table from the database by its name.

        :param name: The name of the table to remove.
        :type name: str

        :return: The popped Table instance.
        """
        return self.tables.pop(name)
    
    def get_table(self, name):
        """
        Retrieves a table from the database by its name.

        :param name: The name of the table to retrieve.
        :type name: str

        :return: The Table instance if found, otherwise raises SQLitoValueError.
        """
        if name not in self.tables:
            raise SQLitoValueError(f"Table '{name}' does not exist in the database.")
        
        return self.tables[name]
    
    def replace_table(self, name, table):
        """
        Replaces an existing table in the database with a new one.

        :param name: The name of the table to replace.
        :type name: str
        :param table: The new Table instance to replace the existing one.
        :type table: Table

        :raises SQLitoTypeError: If the new table is not an instance of Table.
        :raises SQLitoValueError: If the table name does not match the provided table's name.
        """
        if not isinstance(table, Table):
            raise SQLitoTypeError("The new table must be an instance of Table.", Table, table)
        
        if name != table.name:
            raise SQLitoValueError(f"Table name '{name}' must match the provided table's name '{table.name}'.")

        self.tables[name] = table

    def delete_table(self, name):
        """
        Deletes a table from the database by its name. Does not return the table.

        :param name: The name of the table to delete.
        :type name: str

        :raises SQLitoValueError: If the table does not exist in the database.
        """
        if name not in self.tables:
            raise SQLitoValueError(f"Table '{name}' does not exist in the database.")
        
        del self.tables[name]
    
    def __getitem__(self, name):
        return self.tables[name]
    
    def __setitem__(self, name, table):
        self.tables[name] = table

    def __delitem__(self, name):
        del self.tables[name]

    def __contains__(self, name):
        return name in self.tables
    

