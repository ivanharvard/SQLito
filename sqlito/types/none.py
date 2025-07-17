class NONE:
    """Base class for NONE type in SQLito."""
    @classmethod
    def validate(cls, value):
        """
        Accepts any value.
        
        :param value: The value to validate.
        :type value: any
        """
        # Accept anything
        pass

    def __str__(self):
        """Returns the string representation of the NONE type."""
        return type(self).__name__
    