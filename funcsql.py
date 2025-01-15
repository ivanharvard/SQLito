import time

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
        self.order_by = None
        self.limit = None

    def SELECT(self, *fields):
        self.select_fields = fields
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
        if not self.select_fields:
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
                # Operator should change to Python equivalent
                py_equivalents = {
                    '=': '==',
                    '!=': '!=',
                    '<>': '!=',
                    '<=': '<=',
                    '>=': '>=',
                    '<': '<',
                    '>': '>'
                }

                # Try to convert. If fails, leave as is.
                operator = py_equivalents.get(operator, operator)

                try:
                    return eval(f"{row[field]} {operator} {value}")
                except SyntaxError:
                    # Operator must be keyword (e.g., LIKE, IN, etc.)
                    return False #TODO
                
            else:
                raise ValueError(f"""
                                 WHERE condition is incomplete: 
                                 Field: {field} 
                                 Operator: {operator} 
                                 Value: {value}
                                 """)

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
        # Returns only the fields specified in self.select_fields
        return [
            {field: row[field] for field in self.select_fields} for row in data
        ]

    def __str__(self):
        query = "SELECT "
        query += ", ".join(self.select_fields)
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
    
def main():

    people = Table("people", [
        {"id": 1, "name": "John", "age": 30, "role": "Engineer"},
        {"id": 2, "name": "Jane", "age": 25, "role": "Manager"},
        {"id": 3, "name": "Alice", "age": 35, "role": "Engineer"},
        {"id": 4, "name": "Bob", "age": 40, "role": "Manager"},
        {"id": 5, "name": "Charlie", "age": 45, "role": "Engineer"},
        {"id": 6, "name": "David", "age": 50, "role": "Manager"},
        {"id": 7, "name": "Eve", "age": 55, "role": "Engineer"},
        {"id": 8, "name": "Frank", "age": 60, "role": "Manager"},
        {"id": 9, "name": "Grace", "age": 65, "role": "Engineer"},
        {"id": 10, "name": "Heidi", "age": 70, "role": "Manager"},
    ])

    db = Database([people])

    query = Query(db).SELECT("id", "age") \
                     .FROM("people") \
                     .WHERE("name") \
                     .LIKE("J%") \
                     .ORDER_BY("age") \
                     .LIMIT(3)
    
    start_time = time.time()
    results = query.execute()
    end_time = time.time()


    print(query)
    print(results)
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()