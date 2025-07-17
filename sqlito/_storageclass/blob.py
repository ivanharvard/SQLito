from ._base import StorageClass
from sqlito.exceptions import SQLitoTypeError

class BlobStorage(StorageClass):
    """Storage class for BLOB values in SQLito."""
    name = "BLOB"
    valid_types = (bytes, bytearray)

    @classmethod
    def coerce(cls, value):
        """
        Attempts to coerce the value to bytes.
        Accepts bytes, and bytearray.

        :param value: Value to coerce.
        :return: Coerced bytes
        :rtype: bytes

        :raises SQLitoTypeError: If the value cannot be coerced to bytes.
        """
        if isinstance(value, (bytes, bytearray)):
            return bytes(value)
        raise SQLitoTypeError(f"Cannot coerce {value!r} to BLOB.")