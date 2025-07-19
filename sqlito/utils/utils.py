from sqlito._storageclass import NullStorage, IntegerStorage, RealStorage, TextStorage, BlobStorage
from sqlito.types import SQLITO_AFFINITIES, NUMERIC

def store_as_storageclass(value):
    """
    Stores a value under its appropriate storage class based on its type.
    Accepts None, Python primitives, SQLito affinities, and Python objects.
    If the value is of an unknown type (e.g. Python objects), it will be 
    serialized as a BLOB.

    :param value: The value to be stored.
    :type value: any

    :return: An instance of the appropriate storage class.
    :rtype: NullStorage, IntegerStorage, RealStorage, TextStorage, BlobStorage,
    """
    # To ensure we actually store the value appropriately, we first coerce it so
    # that its Python primitive is valid for the storage class. Then, we store
    # the coerced value in the appropriate storage class and return it.

    if value is None:
        return NullStorage(NullStorage.coerce(value))
    elif isinstance(value, int):
        return IntegerStorage(IntegerStorage.coerce(value))
    elif isinstance(value, float):
        return RealStorage(RealStorage.coerce(value))
    elif isinstance(value, str):
        return TextStorage(TextStorage.coerce(value))
    elif isinstance(value, (bytes, bytearray)):
        return BlobStorage(BlobStorage.coerce(value))
    elif isinstance(value, SQLITO_AFFINITIES):
        affinity = value.__class__

        if not hasattr(affinity, 'storage'):
            # NUMERIC types are the only type that don't have a storage class, 
            # so we infer it based on the value.
            affinity = NUMERIC.infer_type(value)
            
        storage_class = affinity.storage
        return storage_class(storage_class.coerce(value))
    else:
        # If the value is of unknown type, we'll serialize it as a BLOB.
        return BlobStorage(BlobStorage.coerce(value))