from sqlito.exceptions import SQLitoTypeError

class StorageClass:
    name = "UNDEFINED"
    valid_types = ()

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
                expected_type=cls.valid_types,
                received_type=type(value).__name__
            )
    
    @classmethod
    def coerce(cls, value):
        raise NotImplementedError(f"{cls.__name__}.coerce() not implemented")
    
    def __str__(self):
        return self.name