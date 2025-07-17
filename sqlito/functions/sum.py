from _singlearg import SingleArg

class SUM(SingleArg):
    """Class representing the SUM function in SQLito."""
    def __init__(self, arg):
        """
        Initializes the SUM function with the provided argument.
        
        :param arg: Column or expression to count.
        :type arg: tuple

        :raises SQLitoTypeError: If the argument is not a Field or Expression.
        """
        super().__init__("SUM", arg)