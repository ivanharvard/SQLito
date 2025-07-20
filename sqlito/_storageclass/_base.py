from sqlito.exceptions import SQLitoTypeError

class StorageClass:
    name = "UNDEFINED"
    valid_types = ()

    def __init__(self, value):
        self.value = self.coerce(value)

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

    def __str__(self):
        return str(self.value)