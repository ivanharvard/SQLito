from sqlito.types import Field, Expression
from sqlito.exceptions import SQLitoSyntaxError
from sqlito.functions import SQLITO_FUNCTIONS

class Query:
    def __init__(self, db):
        """
        Initialize the Query object with a database.

        :param db: The database instance to query against.
        :type db: Database
        """
        self.db = db

    def SELECT(self, *args):
        """
        Create a SELECT query with the provided arguments.
        
        :param args: Columns, literals, expressions, or functions to select.
        :type args: tuple

        :return: An instance of SELECTQuery.
        """
        return SELECTQuery(self.db, *args)

    def SELECT_DISTINCT(self, *args):
        """
        Create a SELECT DISTINCT query with the provided arguments.

        :param args: Columns, literals, expressions, or functions to select.
        :type args: tuple

        :return: An instance of SELECTQuery with distinct selection.
        """
        return SELECTQuery(self.db, *args, distinct=True)

    def SELECT_ALL(self, *args):
        """
        An identical, alternative method to SELECT.

        :param args: Columns, literals, expressions, or functions to select.
        :type args: tuple

        :return: An instance of SELECTQuery.
        """
        return SELECTQuery(self.db, *args, distinct=False)

    
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

        if args is None or len(args) == 0:
            raise SQLitoSyntaxError("No arguments provided for SELECT query.")
        
        function = tuple(SQLITO_FUNCTIONS)
        for arg in args:
            if isinstance(arg, Field):
                self.select_components["columns"].append(arg)
            elif isinstance(arg, Expression):
                self.select_components["expressions"].append(arg)
            elif isinstance(arg, function):
                self.select_components["functions"].append(arg)
            elif isinstance(arg, (int, float, str, bool, type(None), bytes, bytearray)):
                self.select_components["literals"].append(arg)
            else:
                raise SQLitoSyntaxError(f"Invalid argument type for SELECT query: {type(arg).__name__} ({arg!r})")

        

    # def FROM(self, table_name):
    #     self.table = self.db.get_table(table_name)
    #     return FROMQuery(self.db, self.args, self.table, self.distinct)

