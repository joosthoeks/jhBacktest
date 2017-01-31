import csv
import numpy as np
import pandas as pd
from datetime import datetime as dt
import urllib2
import time

# only for yahoo:
from yahoo_finance import Share

# only for IbPy:
from ib.ext.Contract import Contract
from ib.opt import Connection, message


class Data(object):
    def __init__(self):
        self.data = []
        
    def set_data_csv(self, filename, data):
        
        with open(filename, 'w') as csvfile:
            fieldnames = ['datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in data:
                writer.writerow({
                    'datetime': int(row['datetime']),
                    'Open': float(row['Open']),
                    'High': float(row['High']),
                    'Low': float(row['Low']),
                    'Close': float(row['Close']),
                    'Volume': int(row['Volume'])
                    })
        

    def get_data_csv(self, filename):
    
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data.append({
                    'datetime': row['datetime'],
                    'Open': float(row['Open']),
                    'High': float(row['High']),
                    'Low': float(row['Low']),
                    'Close': float(row['Close']),
                    'Volume': int(row['Volume'])
                    })

        return self.data


    def get_data_csv_url(self, url):
        csvfile = urllib2.urlopen(url)
        reader = csv.DictReader(csvfile)
        for row in reader:
            self.data.append({
                'datetime': row['datetime'],
                'Open': float(row['Open']),
                'High': float(row['High']),
                'Low': float(row['Low']),
                'Close': float(row['Close']),
                'Volume': int(row['Volume'])
            })

        return self.data


    def get_data_yahoo(self, date_start, date_end, symbol='^AEX'):
        yahoo = Share(symbol)
        data_org = yahoo.get_historical(date_start, date_end)
        data_org = sorted(data_org, key=lambda x: dt.strptime(x['Date'], '%Y-%m-%d'))
#        date_org.reverse()

        for v in data_org:
            self.data.append({
                'datetime': v['Date'].replace('-', ''),
                'Open': float(v['Open']),
                'High': float(v['High']),
                'Low': float(v['Low']),
                'Close': float(v['Close']),
#                'Close': float(v['Adj_Close']),
                'Volume': int(v['Volume'])
                })

        self.data.append({
            'datetime': yahoo.get_trade_datetime().replace('-', '')[0:8],
            'Open': float(yahoo.get_open()),
            'High': float(yahoo.get_days_high()),
            'Low': float(yahoo.get_days_low()),
            'Close': float(yahoo.get_price()),
            'Volume': int(yahoo.get_volume())
            })

        return self.data


    def set_contract_ib(self, symbol, sec_type, exchange, currency, multiplier, expiry):
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_secType = sec_type
        contract.m_exchange = exchange
        contract.m_currency = currency
        contract.m_multiplier = multiplier
        contract.m_expiry = expiry
        self.contract = contract


    def get_data_ib(self, id, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate):

        con = Connection.create(port=7496, clientId=1)
        con.connect()
        con.register(self.watcher, message.historicalData)

        con.reqHistoricalData(id, self.contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate)

        time.sleep(1)

        con.cancelHistoricalData(id)

        time.sleep(1)

        con.disconnect()

        return self.data

    def watcher(self, msg):
#        print msg
        if msg.open == -1:
            return
        self.data.append({
            'datetime': msg.date,
            'Open': float(msg.open),
            'High': float(msg.high),
            'Low': float(msg.low),
            'Close': float(msg.close),
            'Volume': int(msg.volume)
        })

    def get_numpy_bars(self, bars):
        datetime_list = []
        Open_list = []
        High_list = []
        Low_list = []
        Close_list = []
        Volume_list = []
        for row in bars:
            datetime_list.append(row['datetime'])
            Open_list.append(row['Open'])
            High_list.append(row['High'])
            Low_list.append(row['Low'])
            Close_list.append(row['Close'])
            Volume_list.append(row['Volume'])
        return {
            'datetime': np.array(datetime_list),
            'Open': np.array(Open_list, dtype='float'),
            'High': np.array(High_list, dtype='float'),
            'Low': np.array(Low_list, dtype='float'),
            'Close': np.array(Close_list, dtype='float'),
            'Volume': np.array(Volume_list, dtype='int')
        }

    def get_pandas_bars(self, bars_np):
        return pd.Series(bars_np)
            
