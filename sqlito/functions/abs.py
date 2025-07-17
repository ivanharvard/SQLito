from _singlearg import SingleArg
from sqlito.exceptions import SQLitoTypeError

class ABS(SingleArg):
    """Class representing the ABS function in SQLito."""
    def __init__(self, arg):
        """
        Initializes the ABS function with the provided argument.
        
        :param arg: Number to find the absolute value of. Returns 0.0 if the argument is a string or blob.
        :type arg: tuple

        :raises SQLitoTypeError: If the argument is not a number (int or float), a string (str), or a blob (bytes).
        """
        super().__init__("ABS", arg, valid_types=(int, float, str, bytes))

    def __call__(self):
        """
        Returns the absolute value of the argument.

        :return: The absolute value of the number, or 0.0 if the argument is a string or blob.
        :rtype: int
        """
        if isinstance(self.arg, (int, float)):
            return abs(self.arg)
        elif isinstance(self.arg, (str, bytes)):
            return 0.0
        else:
            raise SQLitoTypeError("Invalid type for ABS function.", expected_type="int, float, str, or bytes", received_type=type(self.arg).__name__)
