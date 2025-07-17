import enum
from sqlito.types.expression import Expression

class Field(enum.Enum):
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
