# -*- coding: utf-8 -*-

from yahoo_finance import Share
from datetime import datetime as dt


def getDataYahoo(dateStart, dateEnd, symbol='^AEX'):
    yahoo = Share(symbol)
    dataOrg = yahoo.get_historical(dateStart, dateEnd)
    dataOrg = sorted(dataOrg, key=lambda x: dt.strptime(x['Date'], '%Y-%m-%d'))
#        dataOrg.reverse()

    data = []
    for v in dataOrg:
        data.append({'datetime': v['Date'],
            'open': float(v['Open']),
            'high': float(v['High']),
            'low': float(v['Low']),
            'close': float(v['Close']),
#            'close': float(v['Adj_Close']),
            'volume': int(v['Volume'])})

    data.append({'datetime': yahoo.get_trade_datetime(),
        'open': float(yahoo.get_open()),
        'high': float(yahoo.get_days_high()),
        'low': float(yahoo.get_days_low()),
        'close': float(yahoo.get_price()),
        'volume': int(yahoo.get_volume())})

    return data
