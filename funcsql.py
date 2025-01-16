class Table:
    def __init__(self, name: str, data: list[dict]):
        self.name = name
        self.data = data

    def get_name(self):
        return self.name
    
    def get_columns(self):
        return list(self.data[0].keys()) if self.data else [] 

    def get_data(self):
        return self.data
    
    def __str__(self):
        return self.name

class Database:
    def __init__(self, tables=None):
        self.tables = {table.get_name(): table for table in (tables or [])}

    def insert_table(self, table):
        name, data = table
        self.tables[name] = data

    def delete_table(self, name):
        return self.tables.pop(name, None)
    
    def drop_table(self, names):
        for name in names:
            self.delete_table(name)
    
    def get_table(self, name):
        for table_name in self.tables:
            if table_name == name:
                return self.tables[table_name]
        return None
    
class Query:
    def __init__(self, db):
        self.db = db 
        self.table = None # Table to be queried

        self.select_fields = []
        self.conditional_fields = []
        self.aggregate_fields = []
        self.order_by = None
        self.limit = None

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
        if table_name not in self.tables():
            raise ValueError(f"{table_name} is not a valid table.")
        
        self.table = self.db.get_table(table_name)
        return self
    
    def WHERE(self, field_or_condition):
        import re
        
        # Use regex to parse condition (e.g., "age > 30")
        pattern = r"(\w+)\s*([=|!=|<|>|<=|>=|<>]+)\s*(.+)"
        match = re.match(pattern, field_or_condition)
        
        if match:
            field, operator, value = match.groups()

            if field not in self.columns():
                raise ValueError(f"{field} is not a valid field.")

            self.conditional_fields.append((field, operator, value))
        else:
            # If no match, then assume it's some kind of field and validate it.
            field = field_or_condition

            if field not in self.columns():
                raise ValueError(f"{field} is not a valid field.")

            self.conditional_fields.append((field, None, None))
        
        return self
            
    def AND(self, field_or_condition):
        pass

    def OR(self, field_or_condition):
        pass

    def LIKE(self, value):
        pass

    def IN(self, values):
        pass

    def BETWEEN(self, value1, value2):
        pass

    def IS_NULL(self):
        pass

    def IF_NOT_NULL(self):
        pass
    
    def ORDER_BY(self, field):
        self.order_by = field
        return self
    
    def LIMIT(self, limit):
        self.limit = limit
        return self
    
    def tables(self):
        return list(self.db.tables.keys())
    
    def columns(self):
        return self.table.get_columns() if self.table else []
    
    def execute(self):
        if not self.table:
            raise ValueError("No table given.")
        if not self.select_fields and not self.aggregate_fields:
            raise ValueError("No fields to select.")

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

        return selected_data

    def __apply_conditions(self, data):
        if not self.conditional_fields:
            return data
        
        def evaluate_condition(row, field, operator, value):
            if operator:
                try:
                    import operator as op

                    # Map operator strings to funcs
                    operators = {
                        '=': op.eq,
                        '!=': op.ne,
                        '<>': op.ne,
                        '<': op.lt,
                        '<=': op.le,
                        '>': op.gt,
                        '>=': op.ge,
                    }

                    # Try to get equivalent operator function, otherwise use operator string.
                    operator_func = operators.get(operator, operator)

                    # Convert value to the same type as row[field]
                    field_value = row[field]
                    if isinstance(field_value, (int, float)):
                        value = float(value) if '.' in str(value) else int(value)
                    elif isinstance(field_value, str) and \
                         ((value.startswith('"') and value.endswith('"')) or \
                          (value.startswith("'") and value.endswith("'"))):
                        value = value[1:-1]

                    return operator_func(field_value, value)
                except SyntaxError:
                    # Operator must be keyword (e.g., LIKE, IN, etc.)
                    print('Failed to evaluate condition.')
                    return False #TODO
                
            else:
                raise ValueError(
                    f"""
                    WHERE condition is incomplete.
                    Field: {field} 
                    Operator: {operator} 
                    Value: {value}
                    """
                )

        filtered_data = []
        for row in data:
            match = True
            for clause in self.conditional_fields:
                field, operator, value = clause
                if not evaluate_condition(row, field, operator, value):
                    match = False
                    break
            if match:
                filtered_data.append(row)

        return filtered_data 
        
    
    def __apply_order(self, data):
        if self.order_by:
            return sorted(data, key=lambda x: x[self.order_by])
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
        else:
            raise ValueError(f"{field_name} is not a valid field.")
            
        if not values:
            raise ValueError(f"No values found for field: {field_name}")
        
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
        if self.conditional_fields:
            for field, operator, value in self.conditional_fields:
                query += f" WHERE {field} "
                if operator:
                    query += f"{operator} {value}"
        if self.order_by:
            query += " ORDER BY " + self.order_by
        if self.limit:
            query += " LIMIT " + str(self.limit)
        return query
    
def __aggregator(aggregateop, field):
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