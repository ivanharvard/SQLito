from funcsql import *
import time

def main():
    people = Table("people", [
        {"id": 1, "name": "John", "age": 30, "role": "Engineer"},
        {"id": 2, "name": "Jane", "age": 25, "role": "Manager"},
        {"id": 3, "name": "Alice", "age": 35, "role": "Engineer"},
        {"id": 4, "name": "Bob", "age": 40, "role": "Manager"},
        {"id": 5, "name": "Charlie", "age": 45, "role": "Engineer"},
        {"id": 6, "name": "David", "age": 50, "role": "Manager"},
        {"id": 7, "name": "Eve", "age": 55, "role": "Engineer"},
        {"id": 8, "name": "Frank", "age": 60, "role": "Manager"},
        {"id": 9, "name": "Grace", "age": 65, "role": "Engineer"},
        {"id": 10, "name": "Heidi", "age": 70, "role": "Manager"},
    ])

    db = Database([people])

    query = Query(db).SELECT("id", "age") \
                     .FROM("people") \
                     .WHERE("age > 30") \
                     .ORDER_BY("age") \
                     .LIMIT(3)
    
    start_time = time.time()
    results = query.execute()
    end_time = time.time()

    print(query)
    print(results)
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()