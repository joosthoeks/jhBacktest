# -*- coding: utf-8 -*-

from data import *
from strategy_example import StrategyExample

from datetime import datetime as dt


dateStart = '2013-01-01'
dateEnd = dt.strftime(dt.utcnow(), '%Y-%m-%d')
bars = getDataYahoo(dateStart, dateEnd, '^AEX')
#bars = getDataCsv('data.csv')
#bars = getDataDb('dbHost', 'dbUser', 'dbPass', 'dbName', 'dbTable', dateStart, dateEnd)
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

