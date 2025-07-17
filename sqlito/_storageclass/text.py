from ._base import StorageClass
from sqlito.exceptions import SQLitoTypeError

class TextStorage(StorageClass):
    """Storage class for TEXT values in SQLito."""
    name = "TEXT"
    valid_types = (str, bytes)

    @classmethod
    def coerce(cls, value):
        """
        Attempts to coerce the value to a string.
        Accepts str and bytes.

        :param value: Value to coerce.
        :return: Coerced string
        :rtype: str

        :raises SQLitoTypeError: If the value cannot be coerced to a string.
        """
        if isinstance(value, str):
            return value
        if isinstance(value, bytes):
            return value.decode('utf-8', errors='replace')
        raise SQLitoTypeError(f"Cannot coerce {value!r} to TEXT.")