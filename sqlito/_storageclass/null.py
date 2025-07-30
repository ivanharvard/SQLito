from sqlito.exceptions import SQLitoTypeError
from ._base import StorageClass

class NullStorage(StorageClass):
    """Storage class for NULL values in SQLito."""
    name = "NULL"
    valid_types = (type(None),)

    def __init__(self, value=None):
        if value is not None:
            raise SQLitoTypeError(f"Invalid value for NULL storage: {value!r}")
        
        self.value = None

    @classmethod
    def coerce(cls, value):
        """
        Attempts to coerce the value to None.
        Accepts None, empty strings, and strings that represent null values.
        
        :param value: Value to coerce.
        :return: None
        :rtype: NoneType

        :raises SQLitoTypeError: If the value cannot be coerced to None.
        """
        if value is None:
            return None
        elif isinstance(value, str) and value.strip().lower() in {"null", "none", ""}:
            return None
        else:
            raise SQLitoTypeError(f"Cannot coerce {value!r} to NULL.")
