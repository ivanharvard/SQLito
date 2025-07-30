from sqlito.database import Database

from sqlito.exceptions import SQLitoSyntaxError, SQLitoTypeError
from sqlito.operators import STAR
from sqlito.types.internal import SelectItem
from sqlito.references import TableReference

class SelectCore:
    def __init__(self, db, *args, distinct=False):
        """
        Initializes the SelectCore with the database and arguments. Parses the
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
        if not args:
            raise SQLitoSyntaxError("No arguments provided for SELECT query.")
        self.distinct = distinct
        self.selected_items = [SelectItem(value=arg) for arg in args]

        self._validate_selectquery()

    def _validate_selectquery(self):
        if not self.args:
            raise SQLitoSyntaxError("No arguments provided for SELECT query.")
        if not isinstance(self.db, Database) or self.db is None:
            raise SQLitoTypeError("db must be an instance of Database")
        if not isinstance(self.distinct, bool):
            raise SQLitoTypeError("distinct must be a boolean value")
        
    def FROM(self, *tables_or_subqueries):
        """
        Specify the tables or subqueries to select from. If more than one 
        argument is provided, the tables/subqueries are joined using a CROSS 
        JOIN. 

        :param tables_or_subqueries: Tables or subqueries to select from.
        :type tables_or_subqueries: tuple[TableReference, SelectCore]
        """
        if not tables_or_subqueries:
            raise SQLitoSyntaxError("No tables or subqueries provided for FROM clause.")

        if not all(isinstance(item, (TableReference, SelectCore)) for item in tables_or_subqueries):
            raise SQLitoTypeError("Arguments for FROM must be tables or subqueries.")
        
        self.from_clause = list(tables_or_subqueries)
        return self
    
    def WHERE(self, condition):
        """
        Specify the condition for filtering the results.
        """
        

        
        
