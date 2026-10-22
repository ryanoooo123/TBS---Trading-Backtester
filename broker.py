import random as rd
import pyarrow.parquet as pq

init_cap = 10000
curr = 'USD'
init_lev = 100

table = pq.read_table('/Users/ryanyang/Desktop/TBS/BTCUSDT_5m.parquet')

for lentable in range(len(table)):

    temp = table.slice(lentable, 1)
    temp_tp = temp['timestamp'][0].as_py()
    temp_open = temp['open'][0].as_py()
    temp_high = temp['high'][0].as_py()
    temp_low = temp['low'][0].as_py()
    temp_close = temp['close'][0].as_py()
    temp_volume = temp['volume'][0].as_py()




def buy_function():
    ...
