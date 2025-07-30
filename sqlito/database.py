from sqlito.builders import TableBuilder, RowBuilder
from sqlito.table import Table
from sqlito.exceptions import SQLitoTableError

class Database:
    def __init__(self, tables=[]):
        # Check that all tables have unique names
        if not isinstance(tables, list) or not all(isinstance(item, Table) for item in tables):
            raise TypeError("Database tables must be a list of Table objects")

        table_names = [table.get_name() for table in tables]
        if len(table_names) != len(set(table_names)):
            raise ValueError("All tables must have unique names.")
        
        # Create table dictionary
        self.tables = {table.get_name(): table for table in (tables or [])}

        self.mode_setting = "off"
        self.timer_setting = True

    def CREATE_TABLE(self, name):
        return TableBuilder(self, name)
    
    def INSERT_INTO(self, name, col_names):
        return RowBuilder(self, name, col_names)

    def insert_table(self, table):
        name, data = table
        self.tables[name] = data

    def delete_table(self, name):
        return self.tables.pop(name, None)
    
    def drop_table(self, names):
        for name in names:
            self.delete_table(name)

    def get_tables(self):
        return self.tables.keys()
    
    def get_table(self, name):
        for table_name in self.tables:
            if table_name == name:
                return self.tables[table_name]
        return None
    
    def schema(self):
        return {name: table.types for name, table in self.tables.items()}
    
    def mode(self, mode_str):
        valid_modes = ['off', 'python', 'table', 'tabs', 'csv']

        if mode_str not in valid_modes:
            raise ValueError("Invalid mode. Valid modes: {valid_modes}")
        self.mode_setting = mode_str
        return self

    def timer(self, timer_str):
        timer_vals = {
            "on": True,
            "off": False
        }

        try:
            self.timer_setting = timer_vals[timer_str]
        except KeyError:
            raise ValueError("Invalid timer value. Valid values: on, off")
        
        return self