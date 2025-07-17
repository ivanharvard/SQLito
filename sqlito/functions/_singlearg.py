from sqlito.types import Expression, Field
from sqlito.exceptions import SQLitoTypeError

class SingleArg:
    """
    Base class for single-argument functions in SQLito.
    This class is used to define functions that take a single argument,
    such as MAX, MIN, SUM, etc.
    """
    def __init__(self, name, arg, valid_types=(Field, Expression)):
        """
        Initializes the function with the provided argument.

        :param name: Name of the function (e.g., "MAX", "min", "sUm").
        :type name: str
        :param arg: Argument to apply the function to.
        :type arg: any
        :param valid_types: Tuple of valid types for the argument. Default is (Field, Expression).
        :type valid_types: tuple

        :raises SQLitoTypeError: If the argument is not of a valid type.
        """

        self.name = name.upper()
        if not isinstance(arg, valid_types):
            raise SQLitoTypeError(f"{self.name} requires a single argument of one of these valid types: {valid_types}.", received_type=type(arg).__name__)
        
        self.arg = arg

    def to_sql(self):
        """
        Converts the function to its SQL representation.

        :return: SQL representation of the function.
        :rtype: str
        """
        return str(self)
    
    def __str__(self):
        """
        Returns the string representation of the function.

        :return: String representation of the function.
        :rtype: str
        """
        return f"{self.name}({self.arg})"