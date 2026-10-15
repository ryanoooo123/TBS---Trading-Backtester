import ccxt
import inspect
import pyarrow as pa
import pyarrow.parquet as pq
import os.path
import datetime as dt
import math as mt


exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '5m'
since = 1672502400000
#limit = 1000
sincedate = dt.datetime.fromtimestamp(int(since/1000)).strftime('%Y-%m-%d %H:%M:%S')
nowtstamp = int(dt.datetime.now().timestamp() * 1000)

print(os.path.isfile(f'/Users/ryanyang/Desktop/TBS/histdata/{timeframe}.txt'))
#print(exchange.fetch_ohlcv(symbol = symbol, timeframe = timeframe, since = 1672502400000, limit = 1000))
#5min = 300,000
def turn(timeframe, since, nowtstamp):

    if timeframe[-1] == 'm':
        time = int(timeframe[0])
        millsec = time * 60 * 1000

    if timeframe[-1] == 'h':
        time = int(timeframe[0])
        millsec = time * 60 * 60 * 1000

    ranges = nowtstamp - since
    turns = mt.ceil((ranges / millsec)/500)

    return turns, millsec


turns, millsec = turn(timeframe, since, nowtstamp)
#start reading file
schema = pa.schema([('symbol', pa.string()), ('timestamp', pa.int64()),('open', pa.float64()), ('high', pa.float64()), ('low', pa.float64()), ('close', pa.float64()), ('volume', pa.float64())])
temp = since

with pq.ParquetWriter(f'{symbol.replace("/", "")}_{timeframe}.parquet', schema) as writer:
    for i in range(turns):

        templist = exchange.fetch_ohlcv(symbol = symbol, timeframe = timeframe, since = temp)

        table = pa.table({
            'symbol':    [symbol] * len(templist),
            'timestamp': [c[0] for c in templist],
            'open':      [c[1] for c in templist],
            'high':      [c[2] for c in templist],
            'low':       [c[3] for c in templist],
            'close':     [c[4] for c in templist],
            'volume':    [c[5] for c in templist],
        }, schema=schema)

        writer.write_table(table)

        temp += millsec * 500






'''
ohlcv:
o = open
h = high
l = low
c = close 
v = volume
'''


