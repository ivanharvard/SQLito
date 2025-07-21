from sqlito.query.selectquery import SELECTQuery

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
        self.db = db

    # ========================================
    # SELECT methods
    # ========================================

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