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
        Accepts any type that can be serialized to bytes, or is already bytes.

        :param value: Value to coerce.
        :type value: bytes, bytearray, or any serializable type
        :return: Coerced bytes
        :rtype: bytes

        :raises SQLitoTypeError: If the value cannot be coerced to bytes.
        """
        if isinstance(value, (bytes, bytearray)):
            return bytes(value)
        
        try:
            from pickle import dumps
            return dumps(value)
        except Exception as e:
            raise SQLitoTypeError(f"Cannot coerce {value!r} to BLOB. Error: {e}")