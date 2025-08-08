from sqlito._storageclass import NullStorage, IntegerStorage, RealStorage, TextStorage, BlobStorage, SerializedBlobStorage
from sqlito.types import SQLITO_AFFINITIES, NUMERIC
from sqlito.exceptions import SQLitoTypeError, SQLitoValueError, SQLitoNotImplemented

import re

def store_as_storageclass(value):
    """
    Stores a value under its appropriate storage class based on its type.
    Accepts None, Python primitives, SQLito affinities, and Python objects.
    If the value is of an unknown type (e.g. Python objects), it will be 
    serialized as a SerializedBLOB.

    :param value: The value to be stored.
    :type value: any

    :return: An instance of the appropriate storage class.
    :rtype: NullStorage, IntegerStorage, RealStorage, TextStorage, BlobStorage
    """
    # To ensure we actually store the value appropriately, we first coerce it so
    # that its Python primitive is valid for the storage class. Then, we store
    # the coerced value in the appropriate storage class and return it.
    # e.g. store_as_storageclass("42") will coerce "42" to a Python int, then
    # store it in IntegerStorage (i.e. IntegerStorage(42)).

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
    elif is_sqlito_affinity(value):
        affinity = value.__class__

        if not hasattr(affinity, 'storage'):
            # NUMERIC types are the only type that don't have a storage class, 
            # so we infer it based on the value.
            affinity = NUMERIC.infer_type(value)

        storage_class = affinity.storage  # ignore pylance error, we've already inferred the type
        return storage_class(storage_class.coerce(value))
    else:
        # If the value is of unknown type, we'll serialize it as a SerializedBLOB.
        return SerializedBlobStorage(SerializedBlobStorage.coerce(value))

def is_sqlito_affinity(obj):
    """
    Checks if a obj is a SQLito affinity type.

    :param obj: The value to check.
    :type obj: any

    :return: True if the value is a SQLito affinity type, False otherwise.
    :rtype: bool
    """
    return isinstance(obj, type) and issubclass(obj, SQLITO_AFFINITIES)

def like_helper(elements, pattern, escape_char=None):
    """
    Helper function to perform the LIKE operation with optional escape character.
    ```
    For each element in the list of elements:
        - If the element is a string, it checks if it matches the pattern.
        - If the element is not a string:
            - If the element is NULL, return NULL.
            - Try to coerce the element to a TEXT, then grab the string, and check if it matches the pattern.
        - Otherwise, return False.
    ```
    
    :param elements: The elements to match against the pattern.
    :type elements: list[Any] | tuple[Any]

    :param pattern: The pattern to match.
    :type pattern: str

    :param escape_char: The escape character for special characters in the pattern.
    :type escape_char: str | None
    """
    def like_pattern_to_regex(pattern, escape_char=None):
        """
        Converts a LIKE pattern to a regex pattern.

        - % => .*
        - _ => .
        - escape_char (if provided) escapes %, _, or itself
        - Other regex metacharacters are escaped automatically

        :param pattern: The LIKE pattern string.
        :param escape_char: Optional single-character escape character.
        :return: A regex string pattern bounded with ^ and $.
        """
        regex = []
        i = 0
        length = len(pattern)
        
        while i < length:
            char = pattern[i]

            if escape_char is not None and char == escape_char:
                i += 1
                if i < length:
                    regex.append(re.escape(pattern[i]))
                else:
                    raise SQLitoValueError("Pattern ends with a lone escape character")
            elif char == '%':
                regex.append('.*')
            elif char == '_':
                regex.append('.')
            elif char in ".^$+?{}[]|()":
                regex.append(f'\\{char}')
            else:
                regex.append(char)

            i += 1

        return '^' + ''.join(regex) + '$'


    if not isinstance(elements, list):
        raise SQLitoTypeError(f"Expected a list.", list, elements)

    if not isinstance(pattern, str) or (isinstance(pattern, str) and len(pattern) != 1):
        raise SQLitoTypeError(f"Expected a single-char string pattern.", str, pattern)
    
    if not isinstance(escape_char, (str, type(None))):
        raise SQLitoTypeError(f"Expected a string or None for escape_char.", "str | None", escape_char)
    
    if escape_char is not None:
        raise SQLitoNotImplemented(f"Escape character is not implemented yet.")
    
    results = []
    regex = like_pattern_to_regex(pattern, escape_char)
    for element in elements:
        if isinstance(element, str):
            results.append(re.match(regex, element) is not None)
        elif isinstance(element, NullStorage):
            results.append(NullStorage())
        else:
            try:
                coerced = TextStorage.coerce(element)
                results.append(re.match(regex, coerced) is not None)
            except SQLitoTypeError:
                results.append(False)
        
    return results

        