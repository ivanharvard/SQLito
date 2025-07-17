from _singlearg import SingleArg

class MAX(SingleArg):
    """Class representing the MAX function in SQLito."""
    def __init__(self, arg):
        """
        Initializes the MAX function with the provided argument.
        
        :param arg: Column or expression to find the maximum of.
        :type arg: tuple

        :raises SQLitoTypeError: If the argument is not a Field or Expression.
        """
        super().__init__("MAX", arg)