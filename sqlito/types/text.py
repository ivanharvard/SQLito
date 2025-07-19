from sqlito.exceptions import SQLitoTypeError
from sqlito._storageclass import TextStorage

class TEXT:
    """
    Base canonical class for text fields in SQLito. 
    """
    valid_types = (str,)
    storage = TextStorage
    

    def __init__(self, size=None):
        """
        Size field is optional, but entirely ignored.
    
        :param size: Optional size of the text field.
        :type size: int, optional
        """
        self.size = size
        
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
        name_of_type = type(self).__name__
        return f"{name_of_type}({self.size})" if self.size else name_of_type
    
class CHAR(TEXT):
    """Class representing a CHAR field in SQLito. Ignores size. Equivalent to TEXT."""
    def __init__(self, size=None):
        super().__init__(size)

class VARCHAR(TEXT):
    """Class representing a VARCHAR field in SQLito. Ignores size. Equivalent to TEXT."""
    def __init__(self, size=None):
        super().__init__(size)

class TINYTEXT(TEXT):
    """Class representing a TINYTEXT field in SQLito. Ignores size. Equivalent to TEXT."""
    def __init__(self, size=None):
        super().__init__(size)

class MEDIUMTEXT(TEXT):
    """Class representing a MEDIUMTEXT field in SQLito. Ignores size. Equivalent to TEXT."""
    def __init__(self, size=None):
        super().__init__(size)

class LONGTEXT(TEXT):
    """Class representing a LONGTEXT field in SQLito. Ignores size. Equivalent to TEXT."""
    def __init__(self, size=None):
        super().__init__(size)

class NCHAR(TEXT):
    """Class representing a NCHAR field in SQLito. Ignores size. Equivalent to TEXT."""
    def __init__(self, size=None):
        super().__init__(size)

class NVARCHAR(TEXT):
    """Class representing a NVARCHAR field in SQLito. Ignores size. Equivalent to TEXT."""
    def __init__(self, size=None):
        super().__init__(size)

class CLOB(TEXT):
    """Class representing a CLOB field in SQLito. Ignores size. Equivalent to TEXT."""
    def __init__(self, size=None):
        super().__init__(size)

