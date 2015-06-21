# -*- coding: utf-8 -*-

from yahoo_finance import Share
from datetime import datetime as dt
import csv
import MySQLdb
# only for ib data:
from ib.opt import ibConnection, message
import time



def getDataYahoo(dateStart, dateEnd, symbol='^AEX'):
    yahoo = Share(symbol)
    dataOrg = yahoo.get_historical(dateStart, dateEnd)
    dataOrg = sorted(dataOrg, key=lambda x: dt.strptime(x['Date'], '%Y-%m-%d'))
#        dataOrg.reverse()

    data = []
    for v in dataOrg:
        data.append({
            'datetime': v['Date'],
            'open': float(v['Open']),
            'high': float(v['High']),
            'low': float(v['Low']),
            'close': float(v['Close']),
#            'close': float(v['Adj_Close']),
            'volume': int(v['Volume'])
            })

    data.append({
        'datetime': yahoo.get_trade_datetime(),
        'open': float(yahoo.get_open()),
        'high': float(yahoo.get_days_high()),
        'low': float(yahoo.get_days_low()),
        'close': float(yahoo.get_price()),
        'volume': int(yahoo.get_volume())
        })

    return data


def getDataCsv(filename):
    
    data = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                'datetime': row['datetime'],
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': int(row['volume'])
                })

    return data


def getDataDb(dbHost, dbUser, dbPass, dbName, dbTable, dateStart, dateEnd):
    db = MySQLdb.connect(host=dbHost,
        user=dbUser,
        passwd=dbPass,
        db=dbName)

    cur = db.cursor()

    sql = """
    SELECT *
    FROM """ + dbTable + """
    WHERE (date BETWEEN '""" + dateStart + """' AND '""" + dateEnd + """')
    """

    cur.execute(sql)

    dataOrg = cur.fetchall()

    data = []
    for v in dataOrg:
        data.append({
            'datetime': v[1],
            'open': float(v[2]),
            'high': float(v[3]),
            'low': float(v[4]),
            'close': float(v[5]),
            'volume': int(v[6])
            })

    return data


def watcher(msg):
#    print msg
    if msg.open == -1:
        return
    data.append({
        'datetime': msg.date,
        'open': float(msg.open),
        'high': float(msg.high),
        'low': float(msg.low),
        'close': float(msg.close),
        'volume': int(msg.volume)
    })

def getDataIb(id, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate):

    global data
    data = []

    con = ibConnection()
    con.register(watcher, message.historicalData)
    con.connect()

    time.sleep(1)

    #con.reqMktData(id, contract, '', False)
    con.reqHistoricalData(id, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate)

    time.sleep(1)

    con.cancelHistoricalData(id)

    time.sleep(1)

    con.disconnect()

    return data

