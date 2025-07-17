from ._base import StorageClass
from sqlito.exceptions import SQLitoTypeError

class RealStorage(StorageClass):
    """Storage class for REAL values in SQLito."""
    name = "REAL"
    valid_types = (float, int)

    @classmethod
    def coerce(cls, value):
        """
        Attempts to coerce the value to a float.
        Accepts int, float, and numeric strings.

        :param value: Value to coerce.
        :return: Coerced float
        :rtype: float

        :raises SQLitoTypeError: If the value cannot be coerced to a float.
        """
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value.strip())
            except ValueError:
                pass
        raise SQLitoTypeError(f"Cannot coerce {value!r} to REAL.")