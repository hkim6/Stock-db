import psycopg2 as pg2

# PG Admin Credentials
DB_HOST = ''
DB_NAME = ''
DB_USER = ''
DB_PASS = ''

conn = pg2.connect(database = DB_NAME, user=DB_USER, password = DB_PASS, host = DB_HOST, port=5432)



cur = conn.cursor()
sql_create_schema = """CREATE SCHEMA sales_cube;"""
sql_create_table = """CREATE TABLE sales_cube.states(
                        id	SERIAL PRIMARY KEY,
                        name VARCHAR(20) NOT NULL UNIQUE
                        );
                        """
cur.execute(sql_create_schema)
cur.execute(sql_create_table)

cur.close()
conn.commit()

conn.close()