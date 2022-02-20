import tkinter as tk
from create_tables import create_schema
import update_stocks as ups
import psycopg2 as pg2

# PG Admin Credentials
DB_HOST = ''
DB_NAME = ''
DB_USER = ''
DB_PASS = ''
pg2.autocommit = True

key = 'ENTER API KEY'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #Make Connection to Database
    conn = pg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port="5432")

    cur = conn.cursor()


    root = tk.Tk()
    frame = tk.Frame(root,height = 200, width = 200)
    frame.pack()
    root.title("Database Options")
    # Code to add widgets will go here...
    init_B = tk.Button(frame, text='Reset/Initialize Database', command=lambda: create_schema(cur))
    new_stock_B = tk.Button(frame, text='Read New Stock List', command=lambda: ups.new_stock(cur, key))
    update_stocks_B = tk.Button(frame, text='Update All Stock Prices', command=lambda: ups.update_stocks(cur, key))
    delete_stocks_B = tk.Button(frame, text='Delete Stocks', command=lambda: ups.delete_stocks(cur))

    init_B.pack(padx=10,pady=5)
    new_stock_B.pack(padx=10,pady=5)
    update_stocks_B.pack(padx=10, pady=5)
    delete_stocks_B.pack(padx=10, pady=5)
    root.mainloop()

    cur.close()
    conn.commit()
    conn.close()



