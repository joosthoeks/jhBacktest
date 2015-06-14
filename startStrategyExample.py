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
print (('Total result: € %s' % stratExam.getTotalValue()))
print (('Total result: %% %s' % stratExam.getTotalProcent()))
print (('Average: € %s' % stratExam.getTotalAverageValue()))
print (('Average: %% %s' % stratExam.getTotalAverageProcent()))
print (('Median: € %s' % stratExam.getTotalMedianValue()))
print (('Median: %% %s' % stratExam.getTotalMedianProcent()))
print (('Variance: € %s' % stratExam.getTotalVarianceValue()))
print (('Variance: %% %s' % stratExam.getTotalVarianceProcent()))
print (('Standard Deviation: € %s' % stratExam.getTotalStandardDeviationValue()))
print (('Standard Deviation: %% %s' % stratExam.getTotalStandardDeviationProcent()))
print (('Hitrate: %% %s' % stratExam.getHitrate()))
print (('####################################################################'))
print (('Bankruptcy date: %s' % stratExam.getBankruptcyDate()))
print (('Max daily drawdown value: %s' % stratExam.getMaxDailyDrawdownValue()))
print (('Consecutive drawdown count: %s' % stratExam.getMaxConsecutiveDrawdownCount()))
print (('Consecutive drawdown value: %s' % stratExam.getMaxConsecutiveDrawdownValue()))
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
print (('Max profit result: € %s' % stratExam.getProfitMaxValue()))
print (('Min profit result: € %s' % stratExam.getProfitMinValue()))
print (('Average: € %s' % stratExam.getProfitAverageValue()))
print (('Median: € %s' % stratExam.getProfitMedianValue()))
print (('Variance: € %s' % stratExam.getProfitVarianceValue()))
print (('Standard Deviation: € %s' % stratExam.getProfitStandardDeviationValue()))
print (('####################################################################'))
print (('Loss trades: %s' % stratExam.getLossCount()))
print (('Total loss result: € %s' % stratExam.getLossValue()))
print (('Max loss result: € %s' % stratExam.getLossMinValue()))
print (('Min loss result: € %s' % stratExam.getLossMaxValue()))
print (('Average: € %s' % stratExam.getLossAverageValue()))
print (('Median: € %s' % stratExam.getLossMedianValue()))
print (('Variance: € %s' % stratExam.getLossVarianceValue()))
print (('Standard Deviation: € %s' % stratExam.getLossStandardDeviationValue()))
print (('####################################################################'))

