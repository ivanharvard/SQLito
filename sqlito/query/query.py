from sqlito.query.cores import SelectCore
from sqlito.database import Database

class Query:
    """
    A class that is the entry point for building SQL queries against a database.

    From this class, you will SELECT, INSERT, UPDATE, DELETE, etc. It provides methods
    """
    def __init__(self, db):
        """
        Initialize the Query object with a database.

        :param db: The database instance to query against.
        :type db: Database
        """
        if not isinstance(db, Database):
            raise TypeError("db must be an instance of Database")

        self.db = db

    # ========================================
    # SELECT methods
    # ========================================

    def SELECT(self, *args):
        """
        Create a SELECT query with the provided arguments.
        
        :param args: Columns, literals, expressions, or functions to select.
        :type args: tuple

        :return: An instance of SelectCore.
        """
        return SelectCore(self.db, *args)

    def SELECT_DISTINCT(self, *args):
        """
        Create a SELECT DISTINCT query with the provided arguments.

        :param args: Columns, literals, expressions, or functions to select.
        :type args: tuple

        :return: An instance of SelectCore with distinct selection.
        """
        return SelectCore(self.db, *args, distinct=True)

    def SELECT_ALL(self, *args):
        """
        An identical, alternative method to SELECT.

        :param args: Columns, literals, expressions, or functions to select.
        :type args: tuple

        :return: An instance of SelectCore.
        """
        return SelectCore(self.db, *args, distinct=False)

    # ========================================
    # CREATE methods
    # ========================================
    
    pass
    
    # ========================================
    # INSERT methods
    # ========================================

    pass

    # ========================================
    # UPDATE methods
    # ========================================

    pass

    # ========================================
    # DELETE methods
    # ========================================

    pass