This code utilizes the IEX Cloud API to import stock data into a POSTGRES SQL Database.  

Running main.py will open a GUI that provide 4 options.

Reset/Initialize Database: Clears and resets database for stock symbols and prices
Read New Stock List: takes in stock list from stock_list.csv and pulls price from specified date in second column
Update All Stock Prices: updates the prices of all stocks in the database to current date
Delete Stocks: delete stocks in delete_list.csv from database