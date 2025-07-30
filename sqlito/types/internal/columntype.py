from sqlito.types import SQLITO_AFFINITIES, INTEGER
from sqlito.exceptions import SQLitoTypeError, SQLitoSyntaxError

class ColumnType:
    """
    Represents a column type in SQLito.
    This class is used to define the type of a column in a table.
    """
    def __init__(self, name, affinity, strict=False, default=None, nullable=False, autoincrement=False):
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
        :param autoincrement: If True, the column is an autoincrementing primary key.
        :type autoincrement: bool
        """
        if not isinstance(name, str):
            raise SQLitoTypeError("Column name must be a string.")
        if not issubclass(affinity, SQLITO_AFFINITIES):
            raise SQLitoTypeError("Column affinity must be one of SQLito's defined affinities.", received_type=affinity)
        if not isinstance(strict, bool):
            raise SQLitoTypeError("Strictness must be a boolean value.")
        if not isinstance(nullable, bool):
            raise SQLitoTypeError("Nullability must be a boolean value.")
        if not isinstance(autoincrement, bool):
            raise SQLitoTypeError("Autoincrement must be a boolean value.")
        if not issubclass(affinity, INTEGER) and autoincrement:
            raise SQLitoSyntaxError("Autoincrement can only be applied to INTEGER columns.")

        self.name = name
        self.affinity = affinity
        self.strict = strict
        self.default = default
        self.nullable = nullable
        self.autoincrement = autoincrement

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
    
    def rename(self, new_name):
        """
        Renames the column type to a new name.

        :param new_name: The new name for the column type.
        :type new_name: str
        """
        if not isinstance(new_name, str):
            raise SQLitoTypeError("Column name must be a string.", str, new_name)
        self.name = new_name
        
    @classmethod
    def compare(cls, cols1, cols2):
        """
        Compares two lists of ColumnType instances for equality.

        :param cols1: The first list of ColumnType instances.
        :type cols1: list of ColumnType
        :param cols2: The second list of ColumnType instances.
        :type cols2: list of ColumnType

        :return: True if the lists are equal, False otherwise.
        """
        if not isinstance(cols1, list) or not isinstance(cols2, list):
            raise SQLitoTypeError("Both arguments must be lists of ColumnType instances.", list, (cols1, cols2))

        if len(cols1) != len(cols2) or sorted(cols1) != sorted(cols2):
            return False
        return True
        
    def __hash__(self):
        """Returns the hash of the column type based on its name."""
        return hash((self.name, self.affinity, self.strict, self.default, self.nullable))

    def __eq__(self, other):
        return isinstance(other, ColumnType) and (
            self.name == other.name and
            self.affinity == other.affinity and
            self.strict == other.strict and
            self.default == other.default and
            self.nullable == other.nullable
        )

    # used for sorting
    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"ColumnType(name={self.name}, affinity={self.affinity}, strict={self.strict}, default={self.default}, nullable={self.nullable})"