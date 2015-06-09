# -*- coding: utf-8 -*-

from data import *
from strategy_example import StrategyExample

from datetime import datetime as dt
#import time



dateStart = '2013-01-01'
dateEnd = dt.strftime(dt.utcnow(), '%Y-%m-%d')
bars = getDataYahoo(dateStart, dateEnd)
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
print (('Result (buy & hold): € %s' % stratExam.getResultBuyAndHoldEuro()))
print (('Result (buy & hold): %% %s' % stratExam.getResultBuyAndHoldProcent()))
print (('####################################################################'))
print (('Total bars: %s' % stratExam.getBarsTotal()))
print (('In market bars: %s' % stratExam.getBarsInMarket()))
print (('In market: %% %s' % stratExam.getProcentInMarket()))
print (('####################################################################'))
print (('Total trades: %s' % stratExam.getTotalCount()))
print (('Total result: € %s' % stratExam.getResultEuro()))
print (('Total result: %% %s' % stratExam.getResultProcent()))
print (('Avg trade result: € %s' % stratExam.getAverageResultPerTradeEuro()))
print (('Avg trade result: %% %s' % stratExam.getAverageResultPerTradeProcent()))
print (('Standard Deviation: € %s' % stratExam.getStandardDeviationEuro()))
print (('Standard Deviation: %% %s' % stratExam.getStandardDeviationProcent()))
print (('Hitrate: %% %s' % stratExam.getHitrate()))
print (('####################################################################'))
print (('Bankruptcy date: %s' % stratExam.getBankruptcyDate()))
print (('Consecutive loss count: %s' % stratExam.getMaxConsecutiveLossCount()))
print (('Consecutive loss value: %s' % stratExam.getMaxConsecutiveLossValue()))
print (('####################################################################'))
print (('Risk of Ruin: %s' % stratExam.getRiskOfRuin()))
print (('Risk of Ruin fixed position size: %% %s' % stratExam.getRiskOfRuinFixedPositionSize()))
print (('Risk of Ruin fixed fraction position sizing: %% %s' % stratExam.getRiskOfRuinFixedFractionalPositionSizing()))
print (('Gambler Ruin problem using Markov Chains: %% %s' % stratExam.getGamblerRuinProblemUsingMarkovChains()))
print (('####################################################################'))
print (('WS Index: %s' % stratExam.getWsIndex()))
print (('RINA Index: %s' % stratExam.getRinaIndex()))
print (('####################################################################'))
print (('Profit trades: %s' % stratExam.getProfitCount()))
print (('Total profit result: € %s' % stratExam.getProfitValue()))
print (('Max profit result: € %s' % stratExam.getProfitValueMax()))
print (('Avg profit result: € %s' % stratExam.getProfitValueAverage()))
print (('Min profit result: € %s' % stratExam.getProfitValueMin()))
print (('####################################################################'))
print (('Loss trades: %s' % stratExam.getLossCount()))
print (('Total loss result: € %s' % stratExam.getLossValue()))
print (('Max loss result: € %s' % stratExam.getLossValueMin()))
print (('Avg loss result: € %s' % stratExam.getLossValueAverage()))
print (('Min loss result: € %s' % stratExam.getLossValueMax()))
print (('####################################################################'))

