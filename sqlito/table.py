class Table:
    def __init__(self, name: str, data: list[dict]):
        self.name = name
        if self.__validate_table(data):
            self.data = data
        else:
            raise ValueError("Invalid table data.")
        
        self.types = self.__determine_types()

    def get_name(self):
        return self.name
    
    def get_columns(self):
        return list(self.data[0].keys()) if self.data else [] 

    def get_data(self):
        return self.data

    def __validate_table(self, table):
        # Ensure table is a list
        if not isinstance(table, list):
            raise ValueError("Table data must be a list.")
        
        # Check for empty table
        if not table:
            raise ValueError("Table data cannot be empty. There should be at least one row with column names, even if each column is empty.")
        
        # Ensure all rows are dictionaries
        if not all(isinstance(row, dict) for row in table):
            raise ValueError("Table data must be a list of dictionaries.")
        
        # Ensure all rows have the same keys
        expected_keys = set(table[0].keys())
        for i, row in enumerate(table):
            if set(row.keys()) != expected_keys:
                raise ValueError(f"Row {i + 1} has inconsistent keys. Expected: {expected_keys}, Got: {set(row.keys())}")
            
        # Ensure table has a valid name
        if not self.get_name():
            raise ValueError("Table must have a name.")
            
        return True
    
    def __determine_types(self):
        # Determine the type of the column based on the first non-None value
        # If there exists None values, add "None"
        results = {}
        for col_name in self.get_columns(): 
            col_type = {"type": None, "allows_null": False}
            for row in self.data:
                entry = row[col_name]
                if entry is None:
                    col_type["allows_null"] = True
                else:
                    if col_type["type"] is None:
                        col_type["type"] = type(entry).__name__
                    else:
                        if col_type["type"] != type(entry).__name__:
                            raise TypeError(f"Encountered a {col_type['type']} in column '{col_name}', but it is already set to {col_type['type']}.")
            results[col_name] = col_type
        return results
    
    def __str__(self):
        return self.name
    
