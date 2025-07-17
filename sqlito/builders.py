from sqlito.table import Table

class RowBuilder:
    def __init__(self, db, name, col_names):
        self.db = db
        self.name = name
        self.col_names = col_names
        self.table = self.db.get_table(name)  
        
        if not isinstance(col_names, list):
            raise TypeError("Column names must be a list.")
        
        for col in col_names:
            if not self.table:
                raise ValueError(f"Table '{name}' does not exist.")
            if col not in self.table.get_columns():
                raise ValueError(f"Column '{col}' does not exist in table '{name}'.")
            
    def VALUES(self, values):
        if not isinstance(values, list):
            raise TypeError("Values must be a list.")
        
        if len(values) != len(self.col_names):
            raise ValueError(f"Number of values ({len(values)}) does not match number of columns ({len(self.col_names)}).")

        # Create a new row with the specified values
        new_row = {col: val for col, val in zip(self.col_names, values)}

        # Check if the number of values is less than the number of columns
        all_columns = self.table.get_columns()
        if len(values) < len(all_columns):
            # If so, then we can (try to) fill in the remaining columns with 
            # their default values.
            
            # Add None values for the remaining columns
            for col in all_columns:
                if col not in self.col_names:
                    values.append(None)

            for col in all_columns:
                contraints = self.table.types[col]
                # Set value of column to its default value if it exists and not
                # already set
                if contraints["default"] and new_row[col] is None:
                    new_row[col] = contraints["default"]
                elif not contraints["allows_null"]:
                    raise ValueError(f"Column '{col}' does not allow NULL values.")
        
        for col, val in new_row.items():
            constraints = self.table.types[col]
            if val is None:
                if constraints["default"]:
                    new_row[col] = constraints["default"]
                elif not constraints["allows_null"]:
                    raise ValueError(f"Column '{col}' does not allow NULL values.")

            col_type = constraints["type"]
            if not isinstance(val, self.__get_type(col_type)):
                raise TypeError(f"Value '{val}' for column '{col}' is not of type '{col_type}'.")
            
            if constraints["unique"]:
                for row in self.table.get_data():
                    if row[col] == val:
                        raise ValueError(f"Value '{val}' for column '{col}' must be unique.")
                    
        self.table.get_data().append(new_row)

    def __get_type(self, type_str):
        # Map SQL types to Python types
        sql_to_python = {
            "TEXT": str,
            "INTEGER": int,
            "REAL": float,
            "BLOB": bytes
        }
        return sql_to_python.get(type_str.strip().upper(), str)
    
class TableBuilder:
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self.columns = []
        self.types = {}
        self.current_column = None
        self.will_raise_exists = True
        self.without_rowid = False

    def IF_NOT_EXISTS(self):
        self.will_raise_exists = False
        return self
    
    def COLUMN(self, name, type_str='TEXT'):
        self.columns.append(name)
        self.types[name] = {
            "type": self.__get_type(type_str),
            "allows_null": True,
            "primary_key": False,
            "default": None,
            "unique": False
        }
        self.current_column = name
        return self
    
    def COLUMNS(self, names_and_types):
        # Add multiple columns at once, with the tradeoff of not being able to 
        # set constraints on each column individually.
        if not isinstance(names_and_types, list):
            raise TypeError("COLUMNS must be a list of tuples (name, type).")
        
        for name, type_str in names_and_types:
            self.COLUMN(name, type_str)
        return self
    
    def PRIMARY_KEY(self):
        for col in self.columns:
            if self.types[col]["primary_key"]:
                raise ValueError(f"Column '{col}' is already set as primary key.")

        self.types[self.current_column]["primary_key"] = True
        self.types[self.current_column]["allows_null"] = False
        self.types[self.current_column]["unique"] = True
        return self
    
    def NOT_NULL(self):
        self.types[self.current_column]["allows_null"] = False
        return self
    
    def DEFAULT(self, value):
        self.types[self.current_column]["default"] = value
        return self
    
    def UNIQUE(self):
        self.types[self.current_column]["unique"] = True
        return self
    
    def __get_type(self, type_str):
        # Map SQL types to Python types
        sql_to_python = {
            "TEXT": str.__name__,
            "INTEGER": int.__name__,
            "REAL": float.__name__,
            "BLOB": bytes.__name__
        }
        return sql_to_python.get(type_str.strip().upper(), str.__name__)
    
    def execute(self):
        # does the table exist already?
        if self.db.get_table(self.name):
            # if "IF NOT EXISTS" was not called, raise an error
            if self.will_raise_exists:
                raise ValueError(f"Table '{self.name}' already exists.")
            else:
                return self.db.get_table(self.name)
            
        init_row = {col: None for col in self.columns}

        # Create the new table with the specified columns and types
        new_table = Table(self.name, [init_row])
        new_table.types = self.types

        # Add the new table to the database
        self.db.insert_table((self.name, new_table))

        return self.db