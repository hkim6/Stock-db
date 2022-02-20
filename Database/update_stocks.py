import datetime as dt
import requests
import tkinter as tk
import concurrent.futures
import datetime as dt

def update_stocks(cur, api_key):
    for stock in list_all_stocks(cur):
        query_date = last_date(stock, cur)
        today = dt.date.today()
        date_list = [(query_date+dt.timedelta(days=x+1)).strftime("%Y%m%d") for x in range((today-query_date).days)]
        with concurrent.futures.ThreadPoolExecutor(8) as executor:
            prices =  list(executor.map(pull_stock_price, [stock for i in range(len(date_list))], date_list, [api_key for i in range(len(date_list))]))
        for response in prices:
            if len(response.json()) > 0:
                res = response.json()[0]
                insert_one_row(stock, res['date'], res['open'], res['close'], res['high'], res['low'], res['volume'], cur)

def pull_stock_price(stock, str_date, api_key):
    return requests.get("https://cloud.iexapis.com/stable/stock/"
                            + stock + "/chart/date/" + str_date + "?chartByDay=true&token=" + api_key)


# get most recent date for stock
def last_date(stock, cur):
    sid = get_stock_id(stock, cur)

    cur.execute("""SELECT prices.date FROM stock_data.prices prices
                   WHERE prices.stock_id = (%s)
                   ORDER BY prices.date DESC
                   LIMIT 1""", (sid,))

    recent_date = cur.fetchone()

    return recent_date[0]

#Takes a single json response and insert into sql stock_data table
def insert_one_row(stock, date, op, close, high, low, vol, cur):
    # get most recent date for stock
    sid = get_stock_id(stock, cur)

    #Insert row
    sql = """INSERT INTO stock_data.prices(date, open, close, high, low, volume, stock_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT DO NOTHING"""
    cur.execute(sql, (date, op, close, high, low, vol, sid))

#Find the stock_id associated with stock
def get_stock_id(stock, cursor):
    cursor.execute("""SELECT id FROM stock_data.stocks st WHERE st.symbol = (%s)""", (stock,))
    stock_id = cursor.fetchone()

    return stock_id

def get_comp_name(symbol, api_key):
    return requests.get("https://cloud.iexapis.com/stable/stock/" + symbol + "/company?token=" + api_key).json()['companyName']

def new_stock(cur, api_key):
    #Read in Stocks from Stock List
    with open('Files\stock_list.csv', 'r') as f:
        data = f.read().split('\n')
    stock_dict = {}
    for stock in data:
        if len(stock) > 0:
            symbol = stock.split(',')[0]
            date = stock.split(',')[1].split('/')
            year = date[2]
            month = date[0]
            day = date[1]

            if len(month) == 1:
                month = '0' + month
            if len(day) == 1:
                day = '0' + day

            stock_dict[symbol] = year + month + day

    fail_list = []
    #for symbol in stock_dict.keys():
    with concurrent.futures.ThreadPoolExecutor(8) as executor:
        comp_names = list(executor.map(get_comp_name, list(stock_dict.keys()), [api_key for i in range(len(stock_dict))]))

    #comp_name = get_comp_name(symbol, api_key)
    with concurrent.futures.ThreadPoolExecutor(8) as executor:
        responses = list(executor.map(pull_stock_price, list(stock_dict.keys()), list(stock_dict.values()), [api_key for i in range(len(stock_dict))]))

    for i, symbol in enumerate(stock_dict.keys()):
        if len(responses[i].json()) > 0:
            res = responses[i].json()[0]
            cur.execute("""INSERT INTO stock_data.stocks(symbol, name) VALUES(%s, %s) ON CONFLICT DO NOTHING""",
                        (symbol.upper(), comp_names[i]))
            insert_one_row(symbol, res['date'], res['open'], res['close'], res['high'], res['low'], res['volume'], cur)
        else:
            fail_list.append(symbol)

    win = tk.Tk()
    fail_box = tk.Label(win, text='Failed to input: ' + ', '.join(str(x).upper() for x in fail_list))
    fail_box.pack()
    win.mainloop()

def list_all_stocks(cur):
    cur.execute("""SELECT symbol FROM stock_data.stocks""")
    return [symb[0] for symb in cur.fetchall()]

def delete_stocks(cur):
    with open('Files\delete_list.csv', 'r') as f:
        data = f.read().split('\n')
    stock_list = []
    for stock in data:
        cur.execute("""DELETE FROM stock_data.prices pr WHERE pr.stock_id = 
                        (SELECT id FROM stock_data.stocks st WHERE st.symbol = %s)""", (stock.upper(),))
        cur.execute("""DELETE FROM stock_data.stocks st WHERE st.symbol = %s""", (stock.upper(),))
        stock_list.append(stock)

    win = tk.Tk()
    fail_box = tk.Label(win, text='Successfully Removed: ' + ', '.join(str(x).upper() for x in stock_list))
    fail_box.pack()
    win.mainloop()
