from funcsql import *
import time

def main():
    # people = Table("people", [
    #     {"id": 1, "name": "John", "age": 30, "role": "Engineer", "salary": 1000},
    #     {"id": 2, "name": "Jane", "age": 25, "role": "Manager", "salary": 2000},
    #     {"id": 3, "name": "Alice", "age": 35, "role": "Engineer", "salary": 3000},
    #     {"id": 4, "name": "Bob", "age": 40, "role": "Manager", "salary": 4000},
    #     {"id": 5, "name": "Charlie", "age": 45, "role": "Engineer", "salary": 5000},
    #     {"id": 6, "name": "David", "age": 50, "role": "Manager", "salary": 1000},
    #     {"id": 7, "name": "Eve", "age": 55, "role": "Engineer", "salary": 2000},
    #     {"id": 8, "name": "Frank", "age": 60, "role": "Manager", "salary": 2000},
    #     {"id": 9, "name": "Grace", "age": 65, "role": "Engineer", "salary": 5000},
    #     {"id": 10, "name": "Heidi", "age": 70, "role": "Manager", "salary": 4000},
    # ])

    # db = Database(people)

    print("Loading database...")
    db = sqlite_to_db(file="shows.db")
    print("Finished.")

    query = Query(db).SELECT("*") \
                     .FROM("shows") \
                     .WHERE("title") \
                     .LIKE("%The%") \
                     .LIMIT(10)
    
    start_time = time.time()
    results = query.execute()
    end_time = time.time()

    print(query)
    print(results)
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()