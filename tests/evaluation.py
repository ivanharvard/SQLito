import sys
import os

# Add parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from sqlito.types.internal import Field, Expression, ColumnType, RowType
from sqlito.references import TableReference, ColumnReference
from sqlito.table import Table
from sqlito.database import Database
from sqlito.types import INTEGER, TEXT, REAL, BLOB

columns = [
    ColumnType(name="id", affinity=INTEGER, strict=True, default=None, nullable=False, autoincrement=True),
    ColumnType(name="name", affinity=TEXT, strict=True, default=None, nullable=False),
    ColumnType(name="salary", affinity=REAL, strict=True, default=None, nullable=False),
]
employees = Table(
    name="employees",
    columns=columns,
    rows={},
    primary_key="id"
)
employees.insert_rows(
    RowType(columns=columns, data={"id": 1, "name": "Alice", "salary": 50000}),
    RowType(columns=columns, data={"id": 2, "name": "Bob", "salary": 60000}),
    RowType(columns=columns, data={"id": 3, "name": "Charlie", "salary": 70000}),
)

db = Database("my_database", tables={"employees": employees})

emp = TableReference("employees", ["id", "name", "salary"])

import time
start = time.time()
for row in employees.rows.values():
    row.data
assert print(type(emp.salary.to_field().evaluate(db)))
assert emp.id.to_field().evaluate(db) == [1, 2, 3]
assert ((emp.salary + emp.id) - (emp.id + emp.id) + emp.id).evaluate(db).data == [50000, 60000, 70000]
assert (emp.salary - 50).AS("decreased_salary").evaluate(db).data == [49950, 59950, 69950]
end = time.time()
print(f"Time taken: {end - start:.6f} seconds")


