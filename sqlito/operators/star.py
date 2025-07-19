from sqlito.types import Field
from sqlito.exceptions import SQLitoSyntaxError

class Star(Field):
    def __init__(self):
        super().__init__()

    def AS(self, alias):
        """
        STAR does not support aliasing.

        :raises SQLitoSyntaxError: Always raises an error when trying to alias STAR.
        """
        raise SQLitoSyntaxError("STAR does not support aliasing.")

    def __str__(self):
        return "*"
    
STAR = Star()