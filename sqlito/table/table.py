from sqlito.exceptions import SQLitoSyntaxError, SQLitoTypeError, SQLitoValueError
from sqlito.types import SQLITO_AFFINITIES, INTEGER
from sqlito.types.internal import ColumnType, RowType
from sqlito.utils import store_as_storageclass
from sqlito._storageclass import NullStorage, IntegerStorage, STORAGECLASSES

class Table:
    def __init__(self, name, columns, rows, strict=False, primary_key="rowid", include_rowid=True):
        """
        Initializes and validates the Table with a name, its column names and
        types, and rows. The name is a unique identifier for the table, and
        the rows is a dictionary of RowType instances, where each dictionary's
        keys are the primary keys of the rows, and the values are RowType 
        instances containing the row data.

        :param name: The name of the table.
        :type name: str
        :param columns: The columns for the table.
        :type columns: list of ColumnType instances
        :param rows: The rows for the table.
        :type rows: dict of RowType instances, where, for each row, the key is 
                    the primary key value for that RowType instance.
        :param strict: If True, column values must conform to the declared type.
        :type strict: bool
        :param primary_key: The name of the primary key column. Defaults to "rowid".
        :type primary_key: str
        :param include_rowid: If True, includes a rowid column in the table.
        :type include_rowid: bool
        """
        self.name = name
        self.columns = columns
        self.rows = rows if rows is not None else {}
        self.strict = strict
        self.primary_key = primary_key
        self.include_rowid = include_rowid

        self._used_primary_keys = set()
        self._used_primary_keys.update(self.rows.keys())

        if self.rows:
            max_key = max(
                k.value for k in self.rows.keys()
                if isinstance(k, IntegerStorage)
            )
            self._auto_increment = max_key + 1
        else:
            self._auto_increment = 1

        self._validate_table()

    def rename(self, new_name):
        """
        Renames the table to a new name.

        :param new_name: The new name for the table.
        :type new_name: str
        """
        if not isinstance(new_name, str):
            raise SQLitoTypeError("Table name must be a string.", str, new_name)
        self.name = new_name

    def add_columns(self, new_columns):
        """
        Adds new columns to the table. Coerces non-strict columns to strict if 
        the table is strict.

        :param new_columns: A ColumnType or a list of ColumnType instances to add.
        :type new_columns: ColumnType or list of ColumnType
        """
        if not isinstance(new_columns, (list, ColumnType)):
            raise SQLitoTypeError("New columns must be a ColumnType or a list of ColumnType instances.", (list, ColumnType), new_columns)

        # make sure to convert new_columns to an iterable if it's a single ColumnType
        if isinstance(new_columns, ColumnType):
            new_columns = (new_columns,)

        for col in new_columns:
            if not isinstance(col, ColumnType):
                raise SQLitoTypeError("Each column must be an instance of ColumnType.", ColumnType, col)
            if not col.strict and self.strict:
                col.strict = True
            self.columns.append(col)

    def delete_columns(self, delete_columns):
        """
        Deletes specified columns from the table.

        :param delete_columns: A string or a list of strings representing column 
                               names.
        :type delete_columns: str, or list of str

        :raises SQLitoTypeError: If delete_columns is not a string or a list of
                                 strings, or if any provided column name is not
                                 in the table.

        """
        if isinstance(delete_columns, str):
            delete_columns = [delete_columns]
        elif not isinstance(delete_columns, list):
            raise SQLitoTypeError("Columns must be a string or a list of strings.", (str, list), delete_columns)

        for dcol in delete_columns:
            if not isinstance(dcol, str):
                raise SQLitoTypeError("Each column name must be a string.", str, dcol)

        existing_col_names = {col.name for col in self.columns}
        missing = [name for name in delete_columns if name not in existing_col_names]
        if missing:
            raise SQLitoSyntaxError(f"Column(s) not found in table '{self.name}': {', '.join(missing)}.")

        # Remove columns whose names are in delete_columns
        self.columns = [col for col in self.columns if col.name not in delete_columns]

    def insert_row(self, row, primary_key_val=None):
        """
        Inserts a new row into the table. 

        :param row: The row data to insert.
        :type row: sqlito.types.internal.RowType
        :param primary_key_val: The value for the primary key. If left as None,
                                the primary key will be autoincremented if the
                                table has an INTEGER primary key. Otherwise, it
                                will raise a SQLitoValueError if the primary key
                                is not provided.

                                However, if the user provides a primary key 
                                value, it must be unique and match the primary 
                                key column's type. If the column was constructed
                                with AUTOINCREMENT, the key value must have 
                                never been used before.
        :type primary_key_val: Any, or None

        :raises SQLitoTypeError: If the row is not an instance of RowType.
        :raises SQLitoValueError: If the row data does not match the table's
                                  columns, if the primary key is missing, or if
                                  the primary key already exists in the table.
        """
        # Row validation
        if not isinstance(row, RowType):
            raise SQLitoTypeError("Row data must be an instance of RowType.")

        if sorted(row.columns) != sorted(self.columns):
            raise SQLitoValueError("Row data columns do not match table columns.")


        # Primary key validation
        if isinstance(primary_key_val, NullStorage):
            raise SQLitoValueError("Primary key value cannot be NULL. If you meant to autoincrement, leave it as None.")

        # Locate the primary key column
        primary_key_col = self._get_primary_key_column()
        if primary_key_col is None:
            # This would be exceptionally weird. Somehow the table got 
            # validated and then the primary key was later removed for some 
            # reason. Why the user would do this is beyond me.
            raise SQLitoValueError(f"Primary key '{self.primary_key}' was not defined in table columns. (How did you get here?)")

        # Since primary key columns are always strict, we can safely assume that
        # the primary key value is never going to be None. If it is None, then
        # the user is trying to insert a row without giving a primary key value.
        if primary_key_val is None:
            # If the primary key already exists in the row data, then we can use
            # that as our primary key value for this row instead.
            if self.primary_key in row.data and row.data[self.primary_key] is not None:
                primary_key_val = row.data[self.primary_key]

        # Otherwise, if the primary key value is still None, we need to
        # autoincrement the primary key if it is an INTEGER primary key.
        if primary_key_val is None:
            # If the primary key is not an INTEGER, then we cannot autoincrement it.
            if not primary_key_col.affinity == INTEGER:
                raise SQLitoValueError(f"SQLito requires explicit values for non-integer primary keys. Please provide a value for the primary key '{self.primary_key}'.")
            
            # Since it is an INTEGER primary key, we can autoincrement it.
            stored_pk = self._autoincrement_INTEGER_primary_key()
        else:
            # If the primary key value is provided, we should check whether it's
            # already stored under a storage class. If it is, we can extract
            # the value from it.
            if isinstance(primary_key_val, STORAGECLASSES):
                primary_key_val = primary_key_val.value
            
            # Now we can check if the primary key value conforms to the column's
            # affinity. If it does not, we raise a SQLitoTypeError.
            if not primary_key_col.conforms_to_affinity(primary_key_val):
                raise SQLitoTypeError(f"Primary key value '{primary_key_val}' does not conform to the type of the primary key column '{self.primary_key}'.")
            
            if primary_key_col.autoincrement and primary_key_val in self._used_primary_keys:
                raise SQLitoValueError(f"Primary key value '{primary_key_val}' has already been used.")
            elif primary_key_val in self.rows:
                raise SQLitoValueError(f"Primary key value '{primary_key_val}' already exists in the table.")
            
        # Store the the primary key under its appropriate storage class
        stored_pk = store_as_storageclass(primary_key_val)
        # Now add it to the set of used primary keys
        self._used_primary_keys.add(stored_pk)
        # In the row, grab the column that is set as the primary key, and set
        # its value to the generated (or provided) primary key value.
        row.data[self.primary_key] = stored_pk
        # Finally, store the row in the table's rows dictionary.
        self.rows[stored_pk] = row

    def insert_rows(self, *rows):
        """
        Inserts multiple rows into the table.

        :param rows: One or more RowType instances to insert.
        :type rows: tuple of sqlito.types.internal.RowType
        """
        for row in rows:
            self.insert_row(row)

        
    def update_row(self, primary_key, updates):
        """
        Updates an existing row in the table by its primary key.

        :param primary_key: The primary key of the row to update.
        :type primary_key: Any
        :param updates: The fields to update and their new values.
        :type updates: dict

        :return row: The updated RowType instance.
        :rtype: sqlito.types.internal.RowType

        :raises SQLitoValueError: If the row with the primary key does not exist,
                                  if the field to update does not exist,
                                  if the row data columns do not match the table columns,
                                  or if the new value cannot be stored under a
                                  storage class.
        """
        try:
            row: RowType = self.get_row(primary_key)
        except KeyError:
            raise SQLitoValueError(f"Row with primary key {primary_key} not found.")
        
        for field, new_value in updates.items():
            if field not in row.data:
                raise SQLitoValueError(f"Field '{field}' not found in row with primary key {primary_key}.")
            
            if not sorted(row.columns) == sorted(self.columns):
                raise SQLitoValueError("Row data columns do not match table columns.")

            row.data[field] = store_as_storageclass(new_value)

        return row

    def get_row(self, primary_key):
        """
        Retrieves a row from the table by its primary key.

        :param primary_key: The primary key of the row to retrieve.
        :type primary_key: Any

        :return: The RowType instance corresponding to the primary key.
        :rtype: sqlito.types.internal.RowType
        """
        return self.rows[primary_key]
    
    def get_column_data(self, column_name):
        """
        Retrieves the data for a specific column across all rows in the table.
        
        :param column_name: The name of the column to retrieve data for.
        :type column_name: str

        :return: A list of all values in the specified column.
        :rtype: list
        """
        if not isinstance(column_name, str):
            raise SQLitoTypeError("Column name must be a string.", str, column_name)

        if column_name not in {col.name for col in self.columns}:
            raise SQLitoValueError(f"Column '{column_name}' does not exist in the table '{self.name}'.")

        return [row.data.get(column_name, NullStorage()) for row in self.rows.values()]
    
    def _get_primary_key_column(self):
        return next((col for col in self.columns if col.name == self.primary_key), None)
    
    def _autoincrement_INTEGER_primary_key(self):
        """
        Finds the the next available primary key value for an INTEGER primary key.
        
        :return: The next available primary key value.
        :rtype: IntegerStorage
        """
        next_pk = self._auto_increment
        while next_pk in self._used_primary_keys or next_pk in self.rows:
            next_pk += 1
        self._auto_increment = next_pk + 1
        return IntegerStorage(next_pk)

    def _validate_table(self):
        """
        Validates the columns and rows of the table. 
        """
        # Check for table name
        if not self.name or not isinstance(self.name, str):
            raise SQLitoSyntaxError("Table must have a name.")

        # Check for existence of columns
        if not self.columns:
            raise SQLitoSyntaxError("Table must have at least one column.")

        # Check for duplicates in columns
        if len(self.columns) != len(set(self.columns)):
            raise SQLitoSyntaxError("Duplicate columns found in the table.")
        
        # Validate the columns
        for col in self.columns:
            if not isinstance(col, ColumnType):
                raise SQLitoTypeError("All columns must be instances of ColumnType.", ColumnType, col)
            if not isinstance(col.name, str):
                raise SQLitoTypeError("Column names must be strings.", str, col.name)
            if not issubclass(col.affinity, SQLITO_AFFINITIES):
                raise SQLitoTypeError("Column affinity must be a valid SQLito type affinity.", SQLITO_AFFINITIES, col.affinity)
            if not isinstance(col.strict, bool):
                raise SQLitoTypeError("Column strictness must be a boolean.", bool, col.strict)
            if not isinstance(col.nullable, bool):
                raise SQLitoTypeError("Column nullability must be a boolean.", bool, col.nullable)

        # Check if rows is a dictionary
        if not isinstance(self.rows, dict):
            raise SQLitoTypeError("Table rows must be a dictionary.")

        # Check if all rows have the same columns
        for i, row in enumerate(self.rows.values()):
            if not isinstance(row, RowType):
                raise SQLitoTypeError("Each row in the table must be a RowType instance.")
            
            if sorted(row.columns) != sorted(self.columns):
                raise SQLitoValueError(f"Row {i} does not match the table's columns. Expected: {self.columns}, Found: {row.columns}")
            
        # Check if primary key is defined in columns
        pk_column = next((col for col in self.columns if col.name == self.primary_key), None)

        if self.include_rowid:
            if pk_column is None:
                # Add implicit rowid if primary key is not defined
                self.columns.insert(0, ColumnType("rowid", INTEGER, strict=True, nullable=False))
                pk_column = self.columns[0]
            elif pk_column.affinity != INTEGER:
                raise SQLitoValueError(f"Primary key '{self.primary_key}' must be of type INTEGER when include_rowid is True.")
        elif pk_column is None:
            raise SQLitoValueError("A primary key is missing. Either define the primary key to match one of the columns, or set include_rowid to True.")
            
    def __getitem__(self, primary_key):
        return self.get_row(primary_key)
    
    def __contains__(self, primary_key):
        return primary_key in self.rows
    
    def __str__(self):
        return  f"""
                Table(
                    name={self.name},
                    columns={self.columns},
                    rows={self.rows}
                )
                """
    