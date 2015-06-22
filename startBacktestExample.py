# -*- coding: utf-8 -*-

from data import *
from strategy_example import StrategyExample

import time
from datetime import datetime as dt

# only for ib:
#from ib.ext.Contract import Contract

ts = int(time.time())
tsStart = ts - (60*60*24*365.25)  # a year
tsEnd = ts - (60*60*24*1)  # a day
dateStart = dt.fromtimestamp(tsStart).strftime('%Y-%m-%d')
dateEnd = dt.fromtimestamp(tsEnd).strftime('%Y-%m-%d')
bars = getDataYahoo(dateStart, dateEnd, '^AEX')
#bars = getDataCsv('data.csv')
#bars = getDataDb('dbHost', 'dbUser', 'dbPass', 'dbName', 'dbTable', dateStart, dateEnd)

# only for ib:
#contract = Contract()
#contract.m_symbol = 'EOE'
#contract.m_secType = 'IND'
#contract.m_exchange = 'FTA'
#endDateTime = dt.fromtimestamp(tsEnd).strftime('%Y%m%d %H:%M:%S UTC')
#bars = getDataIb(1, contract, endDateTime, '1 Y', '1 day', 'TRADES', 0, 1)

balanceStart = 12500  # normal 12500 for mini 1250
bankruptcyAt = 7500  # normal: 7500 for mini: 750
balanceTarget = 25000
multiplier = 200  # normal 200 for mini 20
transactionCosts = 2.9  # normal: 2.9 for mini: .5
slippage = 0
timeperiod = 25

stratExam = StrategyExample(
    bars,
    balanceStart,
    bankruptcyAt,
    balanceTarget,
    multiplier,
    transactionCosts,
    slippage,
    timeperiod
)
stratExam.run()
print (('####################################################################'))
print (('dateStart: %s' % dateStart))
print (('dateEnd: %s' % dateEnd))
print (('balanceStart: %s' % balanceStart))
print (('bankruptcyAt: %s' % bankruptcyAt))
print (('balanceTarget: %s' % balanceTarget))
print (('multiplier: %s' % multiplier))
print (('transactionCosts: %s' % transactionCosts))
print (('slippage: %s' % slippage))
print (('timeperiod: %s' % timeperiod))
print (('####################################################################'))
stratExam.getAnalysis()

