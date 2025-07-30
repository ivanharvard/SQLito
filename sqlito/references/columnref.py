from sqlito.exceptions import SQLitoTypeError
from sqlito.types.internal import Field, Expression

class ColumnReference:
    def __init__(self, table, name):
        """
        Initializes a ColumnReference with a table name and column name.

        :param table: The name of the table this column belongs to.
        :type table: str
        :param name: The name of the column.
        :type name: str

        :raises SQLitoTypeError: If the table or name is not a string.
        """
        if not isinstance(table, str):
            raise SQLitoTypeError(f"Table name must be a string.")
        if not isinstance(name, str):
            raise SQLitoTypeError(f"Column name must be a string.")

        self.table = table
        self.name = name

    def to_field(self):
        """
        Converts this ColumnReference to a Field object.

        :return: A Field object representing this column.
        :rtype: Field
        """
        return Field(self.name, self.table)
    
    def evaluate(self, db):
        return self.to_field().evaluate(db)

    def __add__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()

        return Expression(self.to_field(), "+", other)
    
    def __radd__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()

        return Expression(other, "+", self.to_field())
    
    def __sub__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()

        return Expression(self.to_field(), "-", other)

    def __rsub__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()

        return Expression(other, "-", self.to_field())

    def __mul__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()
        return Expression(self.to_field(), "*", other)

    def __rmul__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()
        return Expression(other, "*", self.to_field())

    def __truediv__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()
        return Expression(self.to_field(), "/", other)

    def __rtruediv__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()
        return Expression(other, "/", self.to_field())

    def __mod__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()
        return Expression(self.to_field(), "%", other)

    def __rmod__(self, other):
        if isinstance(other, ColumnReference):
            other = other.to_field()
        return Expression(other, "%", self.to_field())

    def __str__(self):
        return f"{self.table}.{self.name}"