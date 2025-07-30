from sqlito.exceptions import SQLitoTypeError

class StorageClass:
    name = "UNDEFINED"
    valid_types = ()

    def __init__(self, value):
        self.value = self.coerce(value)

    def evaluate(self, _db=None):
        """
        Returns the value of this storage class instance in a single item list.

        :param _db: Database (not used in this context, ignored).
        :type _db: any
        
        :return: The value stored in this instance.
        :rtype: one of valid_types
        """
        return [self.value]

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
    def __name__(cls):
        return cls.name

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)