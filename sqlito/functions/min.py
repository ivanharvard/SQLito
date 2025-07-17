from _singlearg import SingleArg

class MIN(SingleArg):
    """Class representing the MIN function in SQLito."""
    def __init__(self, arg):
        """
        Initializes the MIN function with the provided argument.
        
        :param arg: Column or expression to find the minimum of.
        :type arg: tuple

        :raises SQLitoTypeError: If the argument is not a Field or Expression.
        """
        super().__init__("MIN", arg)