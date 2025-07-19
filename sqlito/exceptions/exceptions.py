class SQLitoError(Exception):
    """
    Base class for all SQLito exceptions.
    
    param message: Optional custom error message.
    type message: str
    """
    def __init__(self, message="An unknown SQLito error occurred."):
        self.message = message
        super().__init__(message)

class SQLitoTypeError(SQLitoError):
    def __init__(self, message="A type mismatch occurred.", expected_type=None, received_type=None):
        """
        Exception raised for type errors in SQLito.
        
        :param message: Custom error message.
        :type message: str
        :param expected_type: Expected type of the argument. Converted to its string representation, if possible. Appended to error message if provided.
        :type expected_type: str, type, optional
        :param received_type: Actual type of the argument received or the argument received itself. Appended to error message if provided.
        :type received_type: str, any, optional
        """
        full_message = [message]

        if expected_type:
            if isinstance(expected_type, type):
                try:
                    expected_type = expected_type.__name__
                except Exception:
                    expected_type = "unknown"

            full_message.append(f"Expected type: {expected_type}.")
        if received_type:
            if not isinstance(received_type, str):
                try:
                    received_type = type(received_type).__name__
                except Exception:
                    received_type = "unknown"

            full_message.append(f"Received type: {received_type}.")

        super().__init__(" ".join(full_message))

class SQLitoValueError(SQLitoError):
    def __init__(self, message="Invalid value provided."):
        """
        Exception raised for value errors in SQLito.
        
        :param message: Custom error message.
        :type message: str
        """
        super().__init__(message)

class SQLitoSyntaxError(SQLitoError):
    def __init__(self, message="Improper syntax for this SQLito operation."):
        """
        Exception raised for syntax errors in SQLito.
        
        :param message: Custom error message.
        :type message: str
        """
        super().__init__(message)

class SQLitoTimeout(SQLitoError):
    def __init__(self, message="SQLito operation timed out.", time_taken=None, max_time=None):
        """
        Exception raised for timeout errors in SQLito.
        
        :param message: Custom error message.
        :type message: str
        :param time_taken: Time taken for the operation. Appended to error message if provided.
        :type time_taken: float, optional
        :param max_time: Maximum allowed time for the operation. Appended to error message if provided.
        :type max_time: float, optional
        """
        full_message = [message]

        if time_taken is not None:
            full_message.append(f"Time taken: {time_taken} seconds.")
        if max_time is not None:
            full_message.append(f"Maximum allowed time: {max_time} seconds.")

        super().__init__(" ".join(full_message))

class SQLitoTableError(SQLitoError):
    def __init__(self, message="Table error occurred."):
        """
        Exception raised for errors related to tables in SQLito.
        
        :param message: Custom error message.
        :type message: str
        """
        super().__init__(message)

class SQLitoMissing(SQLitoError):
    def __init__(self, message="A required component is missing."):
        """
        Exception raised when a required component is missing. Usually reserved
        for execution time, when a required component to execute an operation
        is not found. Missing components during operation construction should
        instead raise a `SQLitoSyntaxError`.

        For instance, if `SELECT` is called on the fields of a table, but the
        table is not accessed via `FROM`, and the user tries to execute the
        query, this exception should be raised:
        ```
        Query(db).SELECT(table.field1, table.field2).execute() -> raises SQLitoMissing
        ```

        On the other hand, if the user fails to provide arguments to `SELECT`,
        this should raise a `SQLitoSyntaxError`, even before execution:
        ```
        Query(db).SELECT() -> raises SQLitoSyntaxError
        ```
        
        :param message: Custom error message.
        :type message: str
        """
        super().__init__(message)

class SQLitoNotImplemented(SQLitoError):
    def __init__(self, message="This feature is not implemented."):
        """
        Exception raised for features that are not yet implemented in SQLito.
        
        :param message: Custom error message.
        :type message: str
        """
        super().__init__(message)