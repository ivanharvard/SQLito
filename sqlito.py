import time
import re

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
            self.timer = timer_vals[timer_str]
        except KeyError:
            raise ValueError("Invalid timer value. Valid values: on, off")
        
        return self
    
class Query:
    def __init__(self, db):
        self.db = db 
        self.table = None # Table to be queried

        self.select_fields = []
        self.conditional_fields = []
        self.aggregate_fields = []
        self.order_by = None
        self.order_direction = "ASC"
        self.limit = None
        self.last_condition_ref = None

    def SELECT(self, *fields):
        has_aggregates    = any(callable(field) for field in fields)
        has_no_aggregates = any(not callable(field) for field in fields)

        if has_aggregates and has_no_aggregates:
            raise ValueError("Cannot mix aggregate functions and fields in SELECT.")

        # Since we validated that they can't mix,
        # now we just check whether these are aggregate funcs or fields
        if has_aggregates:
            self.select_fields = []
            self.aggregate_fields = [field(self) for field in fields]
        else:
            self.select_fields = fields
            self.aggregate_fields = []

        return self
    
    def FROM(self, table_name):
        if not self.select_fields and not self.aggregate_fields:
            raise ValueError("No fields to select. Did you forget to call SELECT?")

        all_tables = self.tables()
        if not all_tables:
            raise ValueError(f"Cannot access the {table_name} table because there are no tables in this database.")
        if table_name not in all_tables:
            raise ValueError(f"{table_name} is not a valid table in this database.")
        
        self.table = self.db.get_table(table_name)
        return self
    
    def WHERE(self, field_or_condition):
        if not self.table:
            raise ValueError("No table to query. Did you forget to call FROM?")
        if self.conditional_fields:
            raise ValueError("Cannot chain multiple WHERE conditions. Use AND or OR instead.")
        self.__add_condition(field_or_condition)
        return self
            
    def AND(self, field_or_condition):
        if not self.conditional_fields:
            raise ValueError("AND cannot be used without a preceding WHERE.")
        self.__add_condition(field_or_condition, "AND")
        return self

    def OR(self, field_or_condition):
        if not self.conditional_fields:
            raise ValueError("OR cannot be used without a preceding WHERE.")
        self.__add_condition(field_or_condition, "OR")
        return self

    def LIKE(self, value):
        return self.__keyword_operator("LIKE", value)
        
    def IN(self, values):
        return self.__keyword_operator("IN", values)

    def BETWEEN(self, value1, value2):
        return self.__keyword_operator("BETWEEN", (value1, value2))

    def IS_NULL(self):
        return self.__keyword_operator("IS NULL", None)

    def IS_NOT_NULL(self):
        return self.__keyword_operator("IS NOT NULL", None)
    
    def ORDER_BY(self, field, direction="ASC"):
        self.order_by = field
        if direction in ["ASC", "DESC"]:
            self.order_direction = direction
        else:
            raise ValueError(f"Invalid ORDER BY direction: {direction}")
        return self
    
    def LIMIT(self, limit):
        self.limit = limit
        return self
    
    def tables(self):
        return list(self.db.tables.keys())
    
    def columns(self):
        return self.table.get_columns() if self.table else []
    
    def execute(self):
        if not self.db:
            raise ValueError("No database given.")
        if not self.table:
            raise ValueError("No table given.")
        if not self.select_fields and not self.aggregate_fields:
            raise ValueError("No fields to select.")
        
        if self.db.mode_setting != "off":
            pass
        if self.db.timer_setting:
            start_time = time.time()

        # Get all data from table
        table_data = self.table.get_data()

        # Filter data based on WHERE conditions
        filtered_data = self.__apply_conditions(table_data)

        # Order data based on ORDER BY
        ordered_data = self.__apply_order(filtered_data)

        # Limit data based on LIMIT
        limited_data = self.__apply_limit(ordered_data)

        # Select only the fields specified
        selected_data = self.__apply_select(limited_data)

        # Stop timer (to not include printing time)
        if self.db.timer_setting:
            end_time = time.time()

        # Check for mode settings and print appropriately ('off' to disable)
        if self.db.mode_setting == 'python':
            print(selected_data)
        elif self.db.mode_setting == 'tabs':
            if isinstance(selected_data, dict):
                print("\t".join(str(val) for val in selected_data.values()))
            else:
                for item in selected_data:
                    print("\t".join(str(val) for val in item.values()))

        # Print timer after printing results
        if self.db.timer_setting:
            print(f"real: {end_time - start_time} seconds")

        return selected_data
    
    def __add_condition(self, field_or_condition, logic_operator=None):
        # Use regex to parse condition (e.g., "age > 30")
        pattern = r"(\w+)\s*([=|!=|<|>|<=|>=|<>]+)\s*(.+)"
        match = re.match(pattern, field_or_condition)
        
        if match:
            field, operator, value = match.groups()

            if field not in self.columns():
                raise ValueError(f"{field} is not a valid field.")

            new_condition = (field, operator, value)
        else:
            # If no match, then assume it's some kind of field and validate it.
            field = field_or_condition

            if field not in self.columns():
                raise ValueError(f"{field} is not a valid field.")

            new_condition = (field, None, None)

        if not self.conditional_fields:
            self.conditional_fields = new_condition

            # Store reference of last condition for .LIKE, .IN, .BETWEEN, etc.
            self.last_condition_ref = new_condition
        else:
            if isinstance(self.conditional_fields, dict) and self.conditional_fields.get("logic") == logic_operator:
                self.conditional_fields["conditions"].append(new_condition)
            else:
                self.conditional_fields = {
                    "logic": logic_operator,
                    "conditions": [self.conditional_fields, new_condition]
                }

            # Store reference of last condition for .LIKE, .IN, .BETWEEN, etc.
            self.last_condition_ref = new_condition
        
        return self
    
    def __keyword_operator(self, keyword, value):
        if not self.conditional_fields:
            raise ValueError(f"{keyword} cannot be used without a preceding WHERE.")
        
        if self.last_condition_ref is None:
            raise ValueError(f"No condition to apply {keyword} to.")

        field, operator, _ = self.last_condition_ref

        if operator is not None:
            raise ValueError(f"Operator already applied to condition on {field}. Cannot apply {keyword}.")

        updated_condition = (field, keyword, value)

        def update_condition(condition, updated_condition):
            # Update only the condition matching self.last_condition_ref
            if condition == self.last_condition_ref:
                return updated_condition
            elif isinstance(condition, tuple):
                return condition
            elif isinstance(condition, dict):
                return {
                    "logic": condition.get("logic"),
                    "conditions": [update_condition(cond, updated_condition) for cond in condition.get("conditions")]
                }
            else:
                raise ValueError(f"Invalid condition: {condition}")
            
        self.conditional_fields = update_condition(self.conditional_fields, updated_condition)
        self.last_condition_ref = updated_condition

        return self
    
    def __like_match(self, field_value, pattern):
        """
        Matches field_value against a SQL-like pattern using regex.
        SQL LIKE uses `%` for any number of characters and `_` for exactly one character.
        """

        # Convert SQL LIKE pattern to Python regex pattern
        # - `%` becomes `.*` (zero or more characters)
        # - `_` becomes `.` (exactly one character)
        regex_pattern = "^" + pattern.replace("%", ".*").replace("_", ".") + "$"

        # Match the field value using the regex pattern
        return re.match(regex_pattern, field_value) is not None

    def __apply_conditions(self, data):
        if not self.conditional_fields:
            return data
        
        def evaluate_condition(row, condition):
            if isinstance(condition, tuple):
                field, operator, value, = condition
                value = value.strip("'").strip('"') if isinstance(value, str) else value
                field_value = row.get(field)

                # Map operator strings to funcs
                operators = {
                    '='          : lambda x, y: x == y,
                    '!='         : lambda x, y: x != y,
                    '<>'         : lambda x, y: x != y,
                    '<'          : lambda x, y: x < y,
                    '<='         : lambda x, y: x <= y,
                    '>'          : lambda x, y: x > y,
                    '>='         : lambda x, y: x >= y,
                    'LIKE'       : lambda x, y: self.__like_match(x, y),
                    'IN'         : lambda x, y: x in y,
                    'BETWEEN'    : lambda x, y: y[0] <= x <= y[1],
                    'IS NULL'    : lambda x, y: x is None,
                    'IS NOT NULL': lambda x, y: x is not None,
                }

                # Try to get equivalent operator function, otherwise leave as is
                operator_func = operators.get(operator)

                # Convert value to the same type as row[field]
                if isinstance(value, tuple):
                    if isinstance(field_value, (int, float)):
                        value = tuple(float(val) if isinstance(val, str) and '.' in val else int(val) for val in value)
                else:
                    if field_value is not None:  # Only attempt conversion if value is not None
                        if isinstance(field_value, (int, float)):
                            if value is not None:
                                value = float(value) if isinstance(value, str) and '.' in value else int(value)

                try:
                    if field_value is not None and operator not in ["IS NULL", "IS NOT NULL"]:
                        return operator_func(field_value, value) if operator_func else False
                    elif operator in ["IS NULL", "IS NOT NULL"]:
                        return operator_func(field_value, value)
                    else:
                        return False
                except SyntaxError:
                    raise ValueError(f"Invalid operator: {operator}")
            elif isinstance(condition, dict):
                logic = condition.get("logic")
                conditions = condition.get("conditions")

                if logic == "AND" or logic is None:
                    return all(evaluate_condition(row, cond) for cond in conditions)
                elif logic == "OR":
                    return any(evaluate_condition(row, cond) for cond in conditions)
                else:
                    raise ValueError(f"Invalid logic operator: {logic}")
            else:
                raise ValueError(f"Invalid condition: {condition}")

        return [row for row in data if evaluate_condition(row, self.conditional_fields)]
    
    def __apply_order(self, data):
        if self.order_by:
            if self.order_direction == "ASC":
                return sorted(data, key=lambda x: x[self.order_by])
            else:
                return sorted(data, key=lambda x: x[self.order_by], reverse=True)
        else:
            return data
    
    def __apply_limit(self, data):
        # Returns the top n (self.limit) rows 
        return data[:self.limit] if self.limit else data
    
    def __apply_select(self, data):
        # Returns only the fields specified in self.select_fields, or all fields if * is specified.
        if '*' in self.select_fields:
            if len(self.select_fields) == 1:
                # Since the length is 1, the only selected field is '*'
                return data
            else:
                raise ValueError("Cannot simultaneously select all fields and specific fields.")
        elif self.select_fields:
            return [
                {field: row[field] for field in self.select_fields} for row in data
            ]
        elif self.aggregate_fields:
            result = {}
            for field in self.aggregate_fields:
                aggregate_results = self.__apply_aggregate(field, data)
                result[field] = aggregate_results
            return result
        else:
            raise ValueError("No fields were selected. Did you forget to call SELECT?")
        
    def __apply_aggregate(self, aggregate_call, data):
        # Find name of function by finding first parenthesis
        aggregate_name = aggregate_call[:aggregate_call.find('(')]
        # Find name of field in between paraenthesis
        field_name = aggregate_call[aggregate_call.find('(')+1:aggregate_call.find(')')]
        
        # Extract values for specified field from field_name
        values = []
        if field_name in self.columns():
            values = [row[field_name] for row in data]
        elif field_name == "*":
            values = data 
        else:
            raise ValueError(f"{field_name} is not a valid field.")
            
        if not values:
            raise ValueError(f"No values found for field: {field_name}")
        
        # Filter out NULL (None) values
        values = [val for val in values if val is not None]

        if not values:
            # If no values are left after filtering out NULL values, some aggregate functions return 0, others return None
            if aggregate_name in ["COUNT", "SUM"]:
                return 0
            else:
                return None
        
        # Apply aggregate function to values
        try:
            if aggregate_name == "COUNT":
                return len(values)
            elif aggregate_name == "SUM":
                return sum(values)
            elif aggregate_name == "AVG":
                return sum(values) / len(values)
            elif aggregate_name == "MAX":
                return max(values)
            elif aggregate_name == "MIN":
                return min(values)
            else:
                raise ValueError(f"Invalid aggregate function: {aggregate_name}")
        except Exception as e:
            raise ValueError(f"Failed to apply aggregate function: {aggregate_name}. Error: {e}")

    def __str__(self):
        query = "SELECT "
        query += ", ".join(self.select_fields or self.aggregate_fields)
        query += " FROM " + self.table.get_name()
        # if self.conditional_fields:
        #     for (field, operator, value) in self.conditional_fields:
        #         query += f" WHERE {field} "
        #         if operator:
        #             query += f"{operator} {value}"
        if self.order_by:
            query += " ORDER BY " + self.order_by
        if self.limit:
            query += " LIMIT " + str(self.limit)
        return query
    
# ==================================
# Aggregate functions
# ==================================

def __aggregator(aggregateop, field):
    # Aggregates return string and append to aggregate field, only executed when
    # execute() is called
    def __apply(query):
        query.aggregate_fields.append(f"{aggregateop}({field})")
        return f"{aggregateop}({field})"
    return __apply

def COUNT(field):
    return __aggregator("COUNT", field)

def SUM(field):
    return __aggregator("SUM", field)

def AVG(field):
    return __aggregator("AVG", field)

def MAX(field):
    return __aggregator("MAX", field)

def MIN(field):
    return __aggregator("MIN", field)

# ==================================
# Additional functions
# ==================================

def csv_to_table(name, file):
    import csv

    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        return Table(name, data)
    
def table_to_csv(table, file='output.csv'):
    import csv
    
    with open(file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=table.get_columns())
        writer.writeheader()
        for row in table.get_data():
            writer.writerow(row)

# def sqlite_to_db(file):
#     # Converts an SQLite database file into a `Database` object.
#     import sqlite3
    
#     # Connect to SQLite database
#     conn = sqlite3.connect(file)
#     conn.row_factory = sqlite3.Row  # Access rows as dictionaries
#     cursor = conn.cursor()

#     # Fetch all table names
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
#     tables = cursor.fetchall()
#     table_names = [table["name"] for table in tables]

#     # Load each table into a Table object
#     db_tables = []
#     for table_name in table_names:
#         cursor.execute(f"SELECT * FROM {table_name};")
#         rows = [dict(row) for row in cursor.fetchall()]  # Convert rows to a list of dictionaries
#         db_tables.append(Table(name=table_name, data=rows))

#     # Close the connection
#     conn.close()

#     # Create a Database object with the imported tables
#     return Database(db_tables)

# ==================================