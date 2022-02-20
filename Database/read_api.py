import requests

symbol = 'amc'
response = requests.get("https://cloud.iexapis.com/stable/stock/" + symbol + "/chart/6m?token=" + key)
cols = list(response.json()[0].keys())
df = pd.DataFrame(columns = cols)
symbols = ['UBER', 'TSLA', 'NFLX', 'ZM', 'PTON', 'COIN', 'NVDA', 'AMD', 'TWTR', 'SNAP','ABNB','SQ', 'FB']

for symbol in symbols:
    response = requests.get("https://cloud.iexapis.com/stable/stock/" + symbol + "/chart/6m?token=" + key)
    for chart in response.json():
        d_list = pd.Series(list(chart.values()), index = cols)#, high_time, low_time]
        df = df.append(d_list, ignore_index=True)