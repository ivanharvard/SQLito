from sqlito.exceptions.exceptions import SQLitoSyntaxError, SQLitoNotImplemented
from sqlito.types import Expression, Field

class CAST(Field):
    """
    Represents a CAST operation in SQL.
    """
    def __init__(self, expr_field_or_literal):
        """
        Initializes the CAST operation with an expression or field. Awaits .AS() to specify the target type.

        :param expr_field_or_literal: The expression, field, or literal to cast.
        :type expr_field_or_literal: sqlito.types.Expression | sqlito.types.Field | sqlito.types.Literal

        :raises SQLitoSyntaxError: If the target type is not valid for casting.
        """
        super().__init__()
        self.expr_field_or_literal = expr_field_or_literal

    def AS(self, target_type):
        """
        Specifies the target type for the CAST operation.
        
        :param target_type: The type to cast the expression to.
        :type target_type: Any from sqlito.types that has a coercion method.

        :return: A string representation of the CAST operation.
        """
        if not hasattr(target_type, 'coerce'):
            raise SQLitoSyntaxError(f"Invalid target type for CAST: {target_type}")
        
        if isinstance(self.expr_field_or_literal, Expression):
            # TODO: Evaluate expression into field
            raise SQLitoNotImplemented("CAST can only be applied to literals for now.")
        elif isinstance(self.expr_field_or_literal, Field):
            # TODO: Column associated with field should be coerced
            raise SQLitoNotImplemented("CAST can only be applied to literals for now.")
        elif isinstance(self.expr_field_or_literal, (int, float, str, bool, type(None), bytes, bytearray)):
            return target_type.coerce(self.f)

    def __str__(self):
        """
        Returns the string representation of the CAST operation.
        
        :return: A string in the format "CAST(expression AS target_type)".
        """
        return f"CAST({self.expression} AS {self.target_type})"
    
