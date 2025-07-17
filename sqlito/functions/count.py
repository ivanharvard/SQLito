from _singlearg import SingleArg

class COUNT(SingleArg):
    """Class representing the COUNT function in SQLito."""
    def __init__(self, arg):
        """
        Initializes the COUNT function with the provided argument.
        
        :param arg: Column or expression to count.
        :type arg: tuple

        :raises SQLitoTypeError: If the argument is not a Field or Expression.
        """
        super().__init__("COUNT", arg)