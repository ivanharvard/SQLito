from sqlito.types import Field, Expression
from sqlito.exceptions import SQLitoSyntaxError
from sqlito.functions import SQLITO_FUNCTIONS
from sqlito.operators import STAR
    
class SELECTQuery:
    def __init__(self, db, *args, distinct=False):
        """
        Initializes the SELECTQuery with the database and arguments. Parses the 
        arguments into components.
        
        :param db: The database instance to query against.
        :type db: Database
        :param args: Columns, literals, expressions, or functions to select.
        :type args: tuple
        :param distinct: Whether to select distinct values. Default is False.
        :type distinct: bool
        """
        self.db = db
        self.args = args
        self.distinct = distinct
        self.select_components = {
            "columns": [],
            "literals": [],
            "expressions": [],
            "functions": [],
        }

        if not args:
            raise SQLitoSyntaxError("No arguments provided for SELECT query.")
        
        for arg in args:
            if isinstance(arg, Field):
                self.select_components["columns"].append(arg)
            elif isinstance(arg, Expression):
                self.select_components["expressions"].append(arg)
            elif isinstance(arg, SQLITO_FUNCTIONS):
                self.select_components["functions"].append(arg)
            elif isinstance(arg, (int, float, str, bool, type(None), bytes, bytearray)):
                self.select_components["literals"].append(arg)
            else:
                raise SQLitoSyntaxError(f"Invalid argument type for SELECT query: {type(arg).__name__} ({arg!r})")

        # STAR and "*" handling
        for all_columns_symbol in (STAR, "*"):
            if all_columns_symbol in self.select_components['columns']:
                self.select_components['columns'].remove(all_columns_symbol)
                # TODO extend the columns with all columns from the table
                # But since the table is not provided, we cannot "access" the columns
                # unless we pull it from the field itself. for instance, SELECT(emp.name),
                # we need to access the emp table to get all columns. not sure how to do that yet.
                

        # Raise an error if two duplicate columns are provided
        if len(self.select_components['columns']) != len(set(self.select_components['columns'])):
            raise SQLitoSyntaxError("Duplicate columns are not allowed in SELECT query.")
        


    # def FROM(self, table_name):
    #     self.table = self.db.get_table(table_name)
    #     return FROMQuery(self.db, self.args, self.table, self.distinct)

from sqlito.types import NUMERIC, TEXT, VARCHAR, INT2, INT4

users = Table("users", columns=[
    ColumnType("id", INT2, primary_key=True),
    ColumnType("name", TEXT(50), not_null=True),
    ColumnType("email", VARCHAR(100))
])

db = Database([users])

emp =  Query(db) \
      .CREATE_TABLE("employees") \
      .IF_NOT_EXISTS() \
      .COLUMN("id", INT4).PRIMARY_KEY() \
      .COLUMN("name", TEXT(20)).NOT_NULL() \
      .COLUMN("salary", NUMERIC).DEFAULT(0) \
      .execute()

result = Query(db) \
         .SELECT(emp.name, emp.salary) \
         .FROM("employees") \
         .WHERE(emp.salary > 1000) \
         .execute()