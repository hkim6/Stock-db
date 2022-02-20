import psycopg2 as pg2

def create_schema(cur):
    cur.execute("""DROP SCHEMA IF EXISTS stock_data CASCADE;
                    SET timezone = 'America/Los_Angeles';
                    CREATE SCHEMA stock_data;
                        CREATE TABLE stock_data.stocks(
                            id		        SERIAL PRIMARY KEY,
                            symbol	        VARCHAR(20) NOT NULL UNIQUE,
                            name	        VARCHAR(100) NOT NULL UNIQUE);
                        CREATE TABLE stock_data.prices(
                            id              SERIAL PRIMARY KEY,
                            date            DATE NOT NULL,
                            open    	    DECIMAL NOT NULL,
                            close           DECIMAL NOT NULL,
                            high            DECIMAL NOT NULL,
                            low     	    DECIMAL NOT NULL,
                            volume          INTEGER NOT NULL,
                            stock_id        INTEGER REFERENCES stock_data.stocks (id) NOT NULL,
                            UNIQUE(date, stock_id));
                """)




