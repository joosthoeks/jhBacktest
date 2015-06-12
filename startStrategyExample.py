# -*- coding: utf-8 -*-

from data import *
from strategy_example import StrategyExample

from datetime import datetime as dt
#import time



dateStart = '2013-01-01'
dateEnd = dt.strftime(dt.utcnow(), '%Y-%m-%d')
bars = getDataYahoo(dateStart, dateEnd, '^AEX')
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
print (('Result (buy & hold): € %s' % stratExam.getResultBuyAndHoldValue()))
print (('Result (buy & hold): %% %s' % stratExam.getResultBuyAndHoldProcent()))
print (('####################################################################'))
print (('Total bars: %s' % stratExam.getBarsTotal()))
print (('In market bars: %s' % stratExam.getBarsInMarket()))
print (('In market: %% %s' % stratExam.getProcentInMarket()))
print (('####################################################################'))
print (('Total trades: %s' % stratExam.getTotalCount()))
print (('Total result: € %s' % stratExam.getResultValue()))
print (('Total result: %% %s' % stratExam.getResultProcent()))
print (('Average: € %s' % stratExam.getAverageResultPerTradeValue()))
print (('Average: %% %s' % stratExam.getAverageResultPerTradeProcent()))
print (('Variance: € %s' % stratExam.getVarianceValue()))
print (('Variance: %% %s' % stratExam.getVarianceProcent()))
print (('Standard Deviation: € %s' % stratExam.getStandardDeviationValue()))
print (('Standard Deviation: %% %s' % stratExam.getStandardDeviationProcent()))
print (('Median: € %s' % stratExam.getMedianValue()))
print (('Median: %% %s' % stratExam.getMedianProcent()))
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
print (('Min profit result: € %s' % stratExam.getProfitValueMin()))
print (('Average: € %s' % stratExam.getProfitValueAverage()))
print (('Variance: € %s' % stratExam.getProfitValueVariance()))
print (('Standard Deviation: € %s' % stratExam.getProfitValueStandardDeviation()))
print (('Median: € %s' % stratExam.getProfitValueMedian()))
print (('####################################################################'))
print (('Loss trades: %s' % stratExam.getLossCount()))
print (('Total loss result: € %s' % stratExam.getLossValue()))
print (('Max loss result: € %s' % stratExam.getLossValueMin()))
print (('Min loss result: € %s' % stratExam.getLossValueMax()))
print (('Average: € %s' % stratExam.getLossValueAverage()))
print (('Variance: € %s' % stratExam.getLossValueVariance()))
print (('Standard Deviation: € %s' % stratExam.getLossValueStandardDeviation()))
print (('Median: € %s' % stratExam.getLossValueMedian()))
print (('####################################################################'))

