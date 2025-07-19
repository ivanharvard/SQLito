from sqlito.exceptions import SQLitoTypeError
from sqlito._storageclass import RealStorage

class REAL:
    """Base class for REAL types in SQLito."""
    valid_types = (float, int, bool)
    storage = RealStorage

    @classmethod
    def validate(cls, value):
        """
        Validates the type of the value against the valid types for this class.

        :param value: Value to validate.
        :type value: any

        :raises SQLitoTypeError: If the value is not of a valid type.
        """
        if not isinstance(value, cls.valid_types):
            raise SQLitoTypeError(
                f"Invalid type for {cls.__name__} field.",
                expected_type=cls.valid_types,
                received_type=type(value).__name__
            )

    def __str__(self):
        """
        Returns the string representation of the REAL type.
        """
        return type(self).__name__
    
class DOUBLE(REAL):
    """Class representing a DOUBLE field in SQLito. Equivalent to REAL."""
    def __init__(self):
        super().__init__() 

class DOUBLE_PRECISION(REAL):
    """Class representing a DOUBLE PRECISION field in SQLito. Equivalent to REAL."""
    def __init__(self):
        super().__init__()

class FLOAT(REAL):
    """Class representing a FLOAT field in SQLito. Equivalent to REAL."""
    def __init__(self):
        super().__init__()

