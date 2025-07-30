from sqlito.types.internal.vcolumn import VirtualColumn

from sqlito.exceptions import SQLitoTypeError, SQLitoValueError
from sqlito.utils import store_as_storageclass

from itertools import zip_longest

class Expression:
    valid_operators = ["+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">="]

    def __init__(self, left, operator, right):
        """
        Initializes the Expression instance.

        :param left: The left operand of the expression.
        :type left: Expression, Field, StorageClass, VirtualColumn, or a Python object.
        :param operator: The operator to apply between left and right.
        :type operator: str
        :param right: The right operand of the expression.
        :type right: Expression, Field, StorageClass, VirtualColumn, or a Python object.
        """
        self.left = left
        self.operator = operator
        self.right = right
        self.alias = None

        self._validate_expression()

        self.left = self._wrap(self.left)
        self.right = self._wrap(self.right)

    def _validate_expression(self):
        if self.operator not in Expression.valid_operators:
            raise SQLitoValueError(f"Invalid operator: {self.operator}. Supported operators are: {Expression.valid_operators}.")

    def _wrap(self, value):
        if hasattr(value, 'evaluate'):
            return value # Field, Expression, or StorageClass instance
        
        return store_as_storageclass(value) # Python object

    def AS(self, alias):
        """
        Assign an alias to the expression.
        """
        self.alias = alias
        return self
    
    def _op_to_func(self):
        """
        Converts the operator to a function.
        
        :return: A function that applies the operator.
        :rtype: function
        """
        mapping = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "%": lambda x, y: x % y,
        }
        try:
            return mapping[self.operator]
        except KeyError:
            raise SQLitoValueError(f"Invalid operator: {self.operator}. Supported operators are: +, -, *, /, %.")
    
    def evaluate(self, db):
        """
        Evaluate the expression against the database.
        """
        # Unwrap storage classes if present
        def unwrap(v):
            return v.value if hasattr(v, "value") else v
        
        def normalize(v, db):
            if hasattr(v, 'evaluate'):
                v = v.evaluate(db)
            if hasattr(v, 'data'):
                v = v.data
            return [unwrap(item) for item in v] if isinstance(v, list) else [unwrap(v)]
        
        def extend_if_scalar(scalar, length):
            if len(scalar) == 1 and length > 1:
                scalar *= length
            return scalar

        left_values  = normalize(self.left, db)
        right_values = normalize(self.right, db)

        left_values  = extend_if_scalar(left_values, len(right_values))
        right_values = extend_if_scalar(right_values, len(left_values))

        if len(left_values) != len(right_values):
            raise SQLitoValueError("Cannot evaluate expression: left and right sides have different lengths.")
        
        func = self._op_to_func()
        result_data = [func(l, r) for l, r in zip(left_values, right_values)]

        alias = self.alias if self.alias else f"({self.left} {self.operator} {self.right})"
        return VirtualColumn(data=result_data, alias=alias) 
    
    def __add__(self, other):
        return Expression(self, "+", other)
    
    def __sub__(self, other):
        return Expression(self, "-", other)
    
    def __mul__(self, other):
        return Expression(self, "*", other)
    
    def __truediv__(self, other):
        return Expression(self, "/", other)
    
    def __mod__(self, other):
        return Expression(self, "%", other)

    def __str__(self):
        expr = f"({self.left} {self.operator} {self.right})" 
        if self.alias:
            return f"{expr} AS {self.alias}"
        return expr
    
    def __repr__(self):
        return f"Expression({self.left}, {self.operator}, {self.right})"