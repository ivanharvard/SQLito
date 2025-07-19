import enum
from sqlito.types.expression import Expression
from sqlito.exceptions import SQLitoNotImplemented

class Field(enum.Enum):
    def AS(self, alias):
        """
        Assign an alias to the field.
        """
        raise SQLitoNotImplemented("General AS method has not been implemented yet.")
    
    def correlate(self, table):
        """
        Correlate the field with a specific table. This is useful for queries"""
        self.table = table
        return self

    def __str__(self):
        return self.name
    
    def __add__(self, other):
        return Expression(self, "+", other)
    
    def __radd__(self, other):
        return Expression(other, "+", self)
    
    def __sub__(self, other):
        return Expression(self, "-", other)
    
    def __rsub__(self, other):
        return Expression(other, "-", self)
    
    def __mul__(self, other):
        return Expression(self, "*", other)
    
    def __rmul__(self, other):
        return Expression(other, "*", self)
    
    def __truediv__(self, other):
        return Expression(self, "/", other)
    
    def __rtruediv__(self, other):
        return Expression(other, "/", self)
    
    def __mod__(self, other):
        return Expression(self, "%", other)
    
    def __rmod__(self, other):
        return Expression(other, "%", self)
    
    def __eq__(self, other):
        return isinstance(other, Field) and self.name == other.name and self.table == other.table

    def __hash__(self):
        return hash((self.table, self.name))
