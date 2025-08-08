
from sqlito.types.internal.expression import Expression
from sqlito.exceptions import SQLitoTypeError, SQLitoValueError
from sqlito._storageclass import NullStorage
from sqlito.query.cores import SelectCore
from sqlito.types.internal.vcolumn import VirtualColumn
from sqlito.database import Database
from sqlito.utils import store_as_storageclass, _like_helper

class Condition(Expression):
    valid_keywords  = ("AND", "OR", "IS", "LIKE", "IN", "BETWEEN",
                       "IS NOT", "NOT LIKE", "NOT IN", "NOT BETWEEN",)
    mapping = {
        "=": lambda x, y: x == y,
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y,
        "<": lambda x, y: x < y,
        ">": lambda x, y: x > y,
        "<=": lambda x, y: x <= y,
        ">=": lambda x, y: x >= y,
    }

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        self.alias = None

        self._validate()
        self.left = self._wrap(self.left)
        self.right = self._wrap(self.right)

    def _validate(self):
        if self.operator not in self.mapping and self.operator not in self.valid_keywords:
            raise SQLitoValueError(f"Invalid operator: {self.operator}. Supported operators are: {self.mapping.keys()}.")
        
    def evaluate(self, db):
        """
        Evaluate the condition against the database.
        
        :param db: The database instance to evaluate against.
        :return: The result of the evaluation.
        :rtype: bool
        """
        if not isinstance(db, Database):
            raise SQLitoTypeError(f"Expected a Database instance, got {type(db).__name__}.")
        
        def get_value(value):
            if isinstance(value, SelectCore):
                return value.execute()
            elif isinstance(value, VirtualColumn):
                return value.data
            elif hasattr(value, 'evaluate'): # StorageClass, Expression, Field, Condition
                return value.evaluate(db)
            else:
                return store_as_storageclass(value).value
            
        left_value  = get_value(self.left)
        right_value = get_value(self.right)
        
        if self.operator in self.mapping:
            func = self._op_to_func()
            return func(left_value, right_value)
        elif self.operator in self.valid_keywords:
            if self.operator == "AND":
                return left_value and right_value
            elif self.operator == "OR":
                return left_value or right_value
            elif self.operator == "IS":
                return (
                    left_value == right_value
                    or (isinstance(left_value, NullStorage) and isinstance(right_value, NullStorage))
                    or (left_value is None and right_value is None)
                )
            elif self.operator == "IS NOT":
                return not (
                    left_value == right_value
                    or (isinstance(left_value, NullStorage) and isinstance(right_value, NullStorage))
                    or (left_value is None and right_value is None)
                )
            elif self.operator == "LIKE":
                return Condition._like(left_value, right_value, escape_char=None)
             
        

    def AS(self, alias):
        """
        Assign an alias to the expression.
        """
        self.alias = alias
        return self

    def AND(self, other):
        if not isinstance(other, Condition):
            raise SQLitoTypeError(f"AND operation requires a Condition, not {type(other).__name__}.")
        
        return Condition(self, "AND", other)
    
    def OR(self, other):
        if not isinstance(other, Condition):
            raise SQLitoTypeError(f"OR operation requires a Condition, not {type(other).__name__}.")
        
        return Condition(self, "OR", other)
    
    def IS(self, other):
        return Condition(self, "IS", other)
    
    def IS_NOT(self, other):
        return Condition(self, "IS NOT", other)
    
    def LIKE(self, other):
        if not isinstance(other, str):
            raise SQLitoTypeError(f"LIKE operation requires a string, not {type(other).__name__}.")
        
        return Condition(self, "LIKE", other)
    
    def NOT_LIKE(self, other):
        if not isinstance(other, str):
            raise SQLitoTypeError(f"NOT LIKE operation requires a string, not {type(other).__name__}.")
        
        return Condition(self, "NOT LIKE", other)
    
    def IN(self, other):
        if not isinstance(other, (list, tuple, SelectCore, VirtualColumn)):
            raise SQLitoTypeError(f"IN operation requires a list, tuple, or a SELECT query, not {type(other).__name__}.")
        
        return Condition(self, "IN", other)
    
    def NOT_IN(self, other):
        if not isinstance(other, (list, tuple, SelectCore, VirtualColumn)):
            raise SQLitoTypeError(f"NOT IN operation requires a list, tuple, or a SELECT query, not {type(other).__name__}.")
        
        return Condition(self, "NOT IN", other)
    
    def BETWEEN(self, other):
        if not isinstance(other, Condition):
            raise SQLitoTypeError(f"BETWEEN operation requires a Condition, not {type(other).__name__}.")
        
        if not other.operator == "AND":
            raise SQLitoValueError("BETWEEN operation requires a Condition with 'AND' operator.")
        
        return Condition(self, "BETWEEN", other)

    def __and__(self, other):
        return self.AND(other)
    
    def __rand__(self, other):
        return other.AND(self)
    
    def __or__(self, other):
        return self.OR(other)
    
    def __ror__(self, other):
        return other.OR(self)

    def __add__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for +: 'Condition' and '{type(other).__name__}'")

    def __radd__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for +: '{type(other).__name__}' and 'Condition'")
    
    def __sub__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for -: 'Condition' and '{type(other).__name__}'")
    
    def __rsub__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for -: '{type(other).__name__}' and 'Condition'")
    
    def __mul__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for *: 'Condition' and '{type(other).__name__}'")
    
    def __rmul__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for *: '{type(other).__name__}' and 'Condition'")
    
    def __truediv__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for /: 'Condition' and '{type(other).__name__}'")
    
    def __rtruediv__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for /: '{type(other).__name__}' and 'Condition'")
    
    def __mod__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for %: 'Condition' and '{type(other).__name__}'")
    
    def __rmod__(self, other):
        raise SQLitoTypeError(f"unsupported operand type(s) for %: '{type(other).__name__}' and 'Condition'")
    
class ConditionKeyword:
    def __init__(self, keyword):
        self.keyword = keyword