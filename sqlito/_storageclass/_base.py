from sqlito.exceptions import SQLitoTypeError

class StorageClass:
    name = "UNDEFINED"
    valid_types = ()

    def __init__(self, value):
        value = self.coerce(value)

    @classmethod
    def validate(cls, value):
        """
        Validates the type of the value against the valid types for this class.

        :param value: Value to validate.
        :type value: any

        :raises SQLitoTypeError: If the value is not of a valid type.
        """
        if not isinstance(value, cls.valid_types):
            raise SQLitoTypeError(
                f"Invalid type for {cls.__name__} field.",
                cls.valid_types,
                value
            )
    
    @classmethod
    def coerce(cls, value):
        raise NotImplementedError(f"{cls.__name__}.coerce() not implemented")
    
    @classmethod
    def wrap(cls, value):
        """
        Utility method to coerce and return a raw Python value, not an instance
        of the storage class.

        Example usage::
            from sqlito._storageclass import INTEGER

            value = INTEGER.wrap(42)
            print(type(value))  # <class 'int'>

            value = INTEGER.wrap("42") # SQLitoTypeError

        :param value: Value to coerce.
        :return: Coerced value as a raw Python type.
        """
        cls.validate(value)
        return cls.coerce(value)
    
    @classmethod
    def __name__(cls):
        return cls.name

    def __str__(self):
        return str(self.value)