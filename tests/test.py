# from sqlito.query import Query
# from sqlito.database import Database
# from sqlito.types import INTEGER, TEXT
# from sqlito.operators import STAR

# db = Database()
# users = Query(db) \
#         .CREATE_TABLE("users") \
#         .IF_NOT_EXISTS() \
#         .COLUMN("id", INTEGER).PRIMARY_KEY() \
#         .COLUMN("username", TEXT).NOT_NULL() \
#         .execute()

# results = Query(db) \
#           .SELECT(STAR) \
#           .FROM(users) \
#           .WHERE(users.id == 1) \
#           .execute()