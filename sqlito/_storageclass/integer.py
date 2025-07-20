from ._base import StorageClass
from sqlito.exceptions import SQLitoTypeError

class IntegerStorage(StorageClass):
    name = "INTEGER"
    valid_types = (int, bool)

    @classmethod
    def coerce(cls, value):
        """
        Attempts to coerce the value to an integer.
        Accepts bool, int, float (if integral), and numeric strings.

        :param value: Value to coerce.
        :return: Coerced int
        :rtype: int

        :raises SQLitoTypeError: If the value cannot be coerced to an integer.
        """
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float) and value.is_integer():
            return int(value)
        if isinstance(value, str):
            try:
                float_val = float(value)
                if float_val.is_integer():
                    return int(float_val)
            except ValueError:
                pass
        raise SQLitoTypeError(f"Cannot coerce {value!r} to INTEGER.")
    
    # used for finding the maximum or minimum value
    def __lt__(self, other):
        if not isinstance(other, IntegerStorage):
            raise SQLitoTypeError("Cannot compare IntegerStorage with non-IntegerStorage type.", IntegerStorage, other)
        
        return self.value < other.value
    

        
