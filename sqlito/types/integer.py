from sqlito.exceptions import SQLitoTypeError
from sqlito._storageclass.integer import IntegerStorage

class INTEGER:
    """Base class for INTEGER types in SQLito."""
    valid_types = (int, bool)
    storage = IntegerStorage

    @classmethod
    def validate(cls, value):
        cls.storage.validate(value)

    @classmethod
    def coerce(cls, value):
        return cls.storage.coerce(value)
        
    def __str__(self):
        """
        Returns the string representation of the INTEGER type.
        """
        return type(self).__name__
        
class TINYINT(INTEGER):
    """Class representing a TINYINT field in SQLito. Equivalent to INTEGER."""
    def __init__(self):
        super().__init__()

class SMALLINT(INTEGER):
    """Class representing a SMALLINT field in SQLito. Equivalent to INTEGER."""
    def __init__(self):
        super().__init__()

class MEDIUMINT(INTEGER):
    """Class representing a MEDIUMINT field in SQLito. Equivalent to INTEGER."""
    def __init__(self):
        super().__init__()

class BIGINT(INTEGER):
    """Class representing a BIGINT field in SQLito. Equivalent to INTEGER."""
    def __init__(self):
        super().__init__()

class INT2(INTEGER):
    """Class representing an INT2 field in SQLito. Equivalent to INTEGER."""
    def __init__(self):
        super().__init__()

class INT4(INTEGER):
    """Class representing an INT4 field in SQLito. Equivalent to INTEGER."""
    def __init__(self):
        super().__init__()

class INT8(INTEGER):
    """Class representing an INT8 field in SQLito. Equivalent to INTEGER."""
    def __init__(self):
        super().__init__()

