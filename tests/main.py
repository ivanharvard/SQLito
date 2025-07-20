from sqlito import *

def main():
    people = Table("people", [
        {"id": 1,  "name": "John",    "age": 30, "role": "Engineer", "salary": 1000, "warnings": None},
        {"id": 2,  "name": "Jane",    "age": 25, "role": "Manager",  "salary": 2000, "warnings": None},
        {"id": 3,  "name": "Alice",   "age": 35, "role": "Engineer", "salary": 3000, "warnings": None},
        {"id": 4,  "name": "Bob",     "age": 40, "role": "Manager",  "salary": 4000, "warnings": 1},
        {"id": 5,  "name": "Charlie", "age": 45, "role": "Engineer", "salary": 5000, "warnings": None},
        {"id": 6,  "name": "David",   "age": 50, "role": "Manager",  "salary": 1000, "warnings": 2},
        {"id": 7,  "name": "Eve",     "age": 55, "role": "Engineer", "salary": 2000, "warnings": None},
        {"id": 8,  "name": "Frank",   "age": 60, "role": "Manager",  "salary": 2000, "warnings": None},
        {"id": 9,  "name": "Grace",   "age": 65, "role": "Engineer", "salary": 5000, "warnings": None},
        {"id": 10, "name": "Heidi",   "age": 70, "role": "Manager",  "salary": 4000, "warnings": 2},
    ])

    db = Database([people])
    
    # Comment out the following lines if you want to use the database from a file
    # print("Loading database...")
    # db = sqlite_to_db(file="shows.db")
    # print("Finished.")

    # print(db.schema())

    db = db.timer("on")
    db = db.mode("tabs")

    query = Query(db).SELECT("name", "age") \
                     .FROM("people") \
                     .WHERE("warnings") \
                     .IS_NULL() \
                     .AND("salary") \
                     .BETWEEN("1000", "3000") \
                     .OR("age > 50") \
                     .ORDER_BY("age", "DESC") \
                     .execute()
    
    db = db.CREATE_TABLE("passwords") \
           .IF_NOT_EXISTS() \
           .COLUMN("id", "INTEGER").PRIMARY_KEY() \
           .COLUMN("password", "TEXT").NOT_NULL() \
           .COLUMN("strength", "REAL") \
           .COLUMN("created_at", "TEXT").NOT_NULL().UNIQUE() \
           .execute()
    
    
    # db = db.INSERT_INTO("passwords", ["id", "password"]) \
    #        .VALUES([1, "password123"]) \
    #        .execute()
        
    
    # print(db.schema())

if __name__ == "__main__":
    main()