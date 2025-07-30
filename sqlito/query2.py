
    

        


    # def FROM(self, table_name):
    #     self.table = self.db.get_table(table_name)
    #     return FROMQuery(self.db, self.args, self.table, self.distinct)

from sqlito.types import NUMERIC, TEXT, VARCHAR, INT2, INT4

users = Table("users", columns=[
    ColumnType("id", INT2, primary_key=True),
    ColumnType("name", TEXT(50), not_null=True),
    ColumnType("email", VARCHAR(100))
])

db = Database([users])

emp =  Query(db) \
      .CREATE_TABLE("employees") \
      .IF_NOT_EXISTS() \
      .COLUMN("id", INT4).PRIMARY_KEY() \
      .COLUMN("name", TEXT(20)).NOT_NULL() \
      .COLUMN("salary", NUMERIC).DEFAULT(0) \
      .execute()

result = Query(db) \
         .SELECT(emp.name, emp.salary) \
         .FROM("employees") \
         .WHERE(emp.salary > 1000) \
         .execute()