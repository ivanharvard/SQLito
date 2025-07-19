from sqlito.types import SQLITO_AFFINITIES
from sqlito.exceptions import SQLitoTypeError, SQLitoSyntaxError

class ColumnType:
    """
    Represents a column type in SQLito.
    This class is used to define the type of a column in a table.
    """
    def __init__(self, name, affinity, strict=False, default=None, nullable=False):
        """
        Initializes the ColumnType with a name, affinity, strictness, default value, and nullability.

        :param name: The name of the column type.
        :type name: str
        :param affinity: The affinity of the column type, must be one of SQLITO_AFFINITIES.
        :type affinity: SQLITO_AFFINITIES
        :param strict: If True, the column must conform to the declared type.
        :type strict: bool
        :param default: The default value for the column, if any.
        :type default: any
        :param nullable: If True, the column can accept NULL values.
        :type nullable: bool
        """
        if not isinstance(name, str):
            raise SQLitoTypeError("Column name must be a string.")
        if not isinstance(affinity, SQLITO_AFFINITIES):
            raise SQLitoTypeError("Column affinity must be one of SQLito's defined affinities.", received_type=affinity)
        if not isinstance(strict, bool):
            raise SQLitoTypeError("Strictness must be a boolean value.")

        self.name = name
        self.affinity = affinity
        self.type = affinity # alias for readability
        self.strict = strict
        self.default = default
        self.nullable = nullable

    def conforms_to_affinity(self, value, nullability=False) -> bool:
        """
        Checks if the value is an instance of the column's affinity type.

        :param value: The value to check.
        :type value: any
        :param nullability: If True, allows None as a valid value.
        :type nullability: bool

        :return: True if the value is an instance of the column's affinity type, False otherwise.
        """
        if value is None:
            return not nullability
        
        return isinstance(value, self.affinity.valid_types)

    def __eq__(self, other):
        """Two ColumnType instances are equal if their names are the same."""
        return isinstance(other, ColumnType) and self.name == other.name

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"ColumnType(name={self.name}, affinity={self.affinity}, strict={self.strict})"