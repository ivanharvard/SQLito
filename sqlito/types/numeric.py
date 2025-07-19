from . import TEXT, INTEGER, REAL, NONE
from sqlito.exceptions import SQLitoTypeError

class NUMERIC:
    """
    Base canonical class for numeric fields in SQLito.
    """
    valid_types = (int, float, str, bool, type(None))
    storage = 

    @classmethod
    def validate(cls, value):
        storage = cls.infer_type(value)
        storage.validate(value)


    @classmethod
    def infer_type(cls, value):
        """
        Returns a more specific typing for a NUMERIC value, if possible.
        - First, it will try to interpret the value as an INTEGER.
        - If that fails, it will try to interpret it as a REAL.
        - If that fails, it will fallback to TEXT.

        :param value: Value to infer type.
        :type value: any

        :return: A SQLito type class: INTEGER, REAL, TEXT, or NONE.
        :rtype: Type
        """
        # Confirms the value is NUMERIC
        cls.validate(value)

        if isinstance(value, (int, bool)):
            return INTEGER
        elif isinstance(value, float):
            return REAL
        elif isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in ("null", "none", ""):
                return NONE
            elif lowered in ("true", "false"):
                return INTEGER

            try:
                # Attempt to parse as integer or float
                if '.' not in lowered and 'e' not in lowered:
                    int(lowered)
                    return INTEGER
                else:
                    float(lowered)
                    return REAL
            except ValueError:
                return TEXT
        else:
            return TEXT
    
    def __str__(self):
        """
        Returns the string representation of the NUMERIC field.
        
        :return: String representation of the NUMERIC field.
        :rtype: str
        """
        return type(self).__name__  
            
class DECIMAL(NUMERIC):
    """
    Class representing a DECIMAL field in SQLito.
    Inherits from NUMERIC.
    """
    def __init__(self):
        super().__init__()

class BOOLEAN(NUMERIC):
    """
    Class representing a BOOLEAN field in SQLito.
    Inherits from NUMERIC.
    """
    def __init__(self):
        super().__init__()

 
                

                
        
