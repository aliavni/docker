import datetime
import psycopg2

def fun():
    now = datetime.datetime.now()
    print(now)


if __name__ == '__main__':
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", port=5432, host="docker-postgres")
    conn.autocommit = True
    cursor = conn.cursor() 

    sql = """
    select * from information_schema.tables
    """
    cursor.execute(sql) 
    results = cursor.fetchall()
    print(results) 

    counter = 0
    while counter < 10:
        fun()
        counter += 1
