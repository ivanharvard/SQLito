from sqlito.exceptions import SQLitoTypeError
from sqlito.types.internal.columntype import ColumnType

class RowType:
    def __init__(self, columns, data):
        """
        Initializes the RowType with the given columns and data.

        :param columns: The columns for the row, must be a list of ColumnType instances.
        :type columns: list
        :param data: The data for the row, must be a dictionary mapping column names to values.
        :type data: dict
        """
        if not isinstance(data, dict):
            raise SQLitoTypeError("Row data must be a dictionary.")
        if not isinstance(columns, list):
            raise SQLitoTypeError("Columns must be a list of ColumnType instances.")
        if not all(isinstance(col, ColumnType) for col in columns):
            raise SQLitoTypeError("All columns must be instances of ColumnType.")

        self.data = data
        self.columns = columns
        self._validate_row()

    def _validate_row(self):
        for col in self.columns:

            if col.name not in self.data:
                raise SQLitoTypeError(f"Column '{col.name}' is missing in row data.")
            
            value = self.data[col.name]
            if value is None:
                value = col.default
                self.data[col.name] = value

            if value is None:
                if not col.nullable:
                    raise SQLitoTypeError(f"Column '{col.name}' cannot be NULL.")
            else:
                if not col.conforms_to_affinity(value):
                    if col.strict:
                        raise SQLitoTypeError(
                            f"Value '{value}' for column '{col.name}' does not conform to its type {col.affinity.name}."
                        )
                    else: 
                        # If not strict, we can coerce the value
                        try:
                            self.data[col.name] = col.affinity.coerce(value)
                        except SQLitoTypeError:
                            

    def keys(self):
        """
        Returns the keys of the row data.
        :return: A list of column names in the row.
        """
        return list(self.data.keys())
    
    def values(self):
        """
        Returns the values of the row data.
        :return: A list of values in the row.
        """
        return list(self.data.values())
    
    def items(self):
        """
        Returns the items of the row data.
        :return: A list of tuples (column_name, value) in the row.
        """
        return list(self.data.items())

    def __getitem__(self, item):
        """
        Retrieves the value for the given column name.
        :param item: The column name.
        :type item: str
        :return: The value for the column, or None if the column does not exist.
        """
        return self.data.get(item)

    def __setitem__(self, key, value):
        """
        Sets the value for the given column name.
        :param key: The column name.
        :type key: str
        :param value: The value to set.
        :type value: any
        """
        self.data[key] = value

    def __delitem__(self, key):
        """
        Deletes the value for the given column name.
        :param key: The column name.
        :type key: str
        """
        if key in self.data:
            del self.data[key]

    def __contains__(self, item):
        return item in self.data

    def __eq__(self, other):
        return isinstance(other, RowType) and self.data == other.data
    
    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return f"RowType({self.data})"