# -*- coding: utf-8 -*-

import numpy as np
import math
import scipy as sp
from scipy import stats
from tabulate import tabulate


class Strategy(object):

    def __init__(self, bars, balanceStart, bankruptcyAt, balanceTarget,
        multiplier, transactionCosts, slippage):

        self.__bars = bars
        self._barsNP = self.__getNumpyBars(bars)
        self._longSignal = False
        self._shortSignal = False
        self._longPos = False
        self._shortPos = False
        self.__barIndex = -1
        self.__barInMarket = 0
        self.__balanceStart = balanceStart
        self.__balance = balanceStart
        self.__bankruptcyAt = bankruptcyAt
        self.__bankruptcyDate = 0
        self.__balanceTarget = balanceTarget
        self.__multiplier = multiplier
        self.__transactionCosts = transactionCosts
        self.__slippage = slippage
        self._posBuyAndHoldStart = 0
        self._posBuyAndHoldEnd = 0
        self.__longPosStart = 0
        self.__longPosEnd = 0
        self.__shortPosStart = 0
        self.__shortPosEnd = 0
        self.__totalValuesArr = []
        self.__profitValuesArr = []
        self.__lossValuesArr = []
        self.__barDrawdownArr = []

    def __getNumpyBars(self, bars):
        datetimeArr = []
        openArr = []
        highArr = []
        lowArr = []
        closeArr = []
        volumeArr = []
        for row in bars:
            datetimeArr.append(row['datetime'])
            openArr.append(row['open'])
            highArr.append(row['high'])
            lowArr.append(row['low'])
            closeArr.append(row['close'])
            volumeArr.append(row['volume'])
        return {
            'datetime': np.array(datetimeArr),
            'open': np.array(openArr, dtype='f8'),
            'high': np.array(highArr, dtype='f8'),
            'low': np.array(lowArr, dtype='f8'),
            'close': np.array(closeArr, dtype='f8'),
            'volume': np.array(volumeArr, dtype='f8')
        }

    def __setBuyAndHold(self, bar):
        if self._posBuyAndHoldStart is 0:
            self._posBuyAndHoldStart = bar['open']
        self._posBuyAndHoldEnd = bar['close']

    def getResultBuyAndHoldValue(self):
        result = self._posBuyAndHoldEnd - self._posBuyAndHoldStart
        result = self.__addMultiplierTransactionCostsSlippage(result)
        return result

    def getResultBuyAndHoldProcent(self):
        return (
            float(self.getResultBuyAndHoldValue()) / self.__balanceStart * 100
            )

    def getBarIndex(self):
        return self.__barIndex

    def __setBarIndex(self):
        self.__barIndex += 1

    def getBarsTotal(self):
        return self.__barIndex + 1

    def getBarsInMarket(self):
        return self.__barInMarket

    def __setBarsInMarket(self):
        if self._longPos or self._shortPos:
            self.__barInMarket += 1

    def getProcentInMarket(self):
        return (float(self.getBarsInMarket()) / self.getBarsTotal() * 100)

    def getMaxBarDrawdownValue(self):
        if len(self.__barDrawdownArr) == 0:
            return 0
        return max(self.__barDrawdownArr) * -1

    def __setBarDrawdown(self, bar):
        if self._longPos:
            barDrawdown = (bar['open'] - bar['low']) * self.__multiplier
            self.__barDrawdownArr.append(barDrawdown)
        if self._shortPos:
            barDrawdown = (bar['high'] - bar['open']) * self.__multiplier
            self.__barDrawdownArr.append(barDrawdown)

    def getBankruptcyDate(self):
        return self.__bankruptcyDate

    def __setBankruptcyDate(self, bar):
        if self.__bankruptcyDate is 0:
            diff = self.__balanceStart - self.__bankruptcyAt
            if (self.getMaxBarDrawdownValue() > diff):
                self.__bankruptcyDate = bar['datetime']
        if self.__bankruptcyDate is 0:
            if (self.__balance < self.__bankruptcyAt):
                self.__bankruptcyDate = bar['datetime']

    def getMaxConsecutiveDrawdownCount(self):
        lossCount = 0
        lossCountArr = []
        for value in self.__totalValuesArr:
            if value <= 0:
                lossCount += 1
                lossCountArr.append(lossCount)
            else:
                lossCount = 0
                
        return max(lossCountArr)

    def getMaxConsecutiveDrawdownValue(self):
        lossValue = 0
        lossValueArr = []
        for value in self.__totalValuesArr:
            if value <= 0:
                lossValue += value
                lossValueArr.append(lossValue)
            else:
                lossValue = 0
                
        return min(lossValueArr)

    def getRiskOfRuin(self):
        if self.getLossAverageValue() == 0:
            return 'nan'
        edge = self.getHitrate() - 50
        capitalUnits = ((
            (self.__balanceStart - self.__bankruptcyAt)
        ) / (self.getLossAverageValue() * -1))
        return ((1 - edge) / (1 + edge)) ** round(capitalUnits)

    def getRiskOfRuinFixedPositionSize(self):
        if self.getTotalStandardDeviationProcent() == 0:
            return 'nan'
        e = 2.71828
        a = self.getTotalAverageProcent() / 100
        z = (float(self.__balanceStart - self.__bankruptcyAt) 
        / self.__balanceStart)
        d = self.getTotalStandardDeviationProcent() / 100
        return (e ** - (2 * a * z / d ** 2)) * 100

    def getRiskOfRuinFixedFractionalPositionSizing(self):
        if self.getTotalStandardDeviationProcent() == 0:
            return 'nan'
        e = 2.71828
        a = self.getTotalAverageProcent() / 100
        z = (float(self.__balanceStart - self.__bankruptcyAt) 
        / self.__balanceStart)
        d = self.getTotalStandardDeviationProcent() / 100
        return (e ** - ((2 * a / d) * math.log(1 - z) / math.log(1 - d))) * 100

    def getGamblerRuinProblemUsingMarkovChains(self):
        if self.getHitrate() == 50:
            return 'nan'
        edge = (self.getHitrate() - 50) / 100
        q = .5 - edge
        p = .5 + edge
#        z = self.__balanceStart
        z = round(self.__balanceStart / self.getTotalAverageValue())
#        m = self.__balanceTarget
        m = round(self.__balanceTarget / self.getTotalAverageValue())
        return (((q / p) ** m - (q / p) ** z) / ((q / p) ** m - 1)) * 100
        
    def getHitrate(self):
        if self.getProfitCount() == 0:
            return 0
        return (float(self.getProfitCount()) / self.getTotalCount() * 100)

    def getSharpeRatio(self):
        if self.getTotalStandardDeviationProcent() == 0:
            return 0
        return self.getTotalAverageProcent() / self.getTotalStandardDeviationProcent()

    def getWsIndex(self):
        if self.getLossMinValue() == 0:
            return 'nan'

        maxLoss = self.getLossMinValue() * -1
        return (
            (
                10000. * self.getTotalAverageValue()
            ) / (
                maxLoss * self.getProcentInMarket()
            )
        )

    def getRinaIndex(self):
        if self.getLossAverageValue() == 0:
            return 'nan'

        avgLoss = self.getLossAverageValue() * -1
        return (
            (
                self.getTotalValue()
            ) / (
                avgLoss * self.getProcentInMarket()
            )
        )

    def getTotalCount(self):
        return len(self.__totalValuesArr)

    def getTotalValue(self):
        return sum(self.__totalValuesArr)

    def getTotalProcent(self):
        if len(self.__totalValuesArr) == 0:
            return 0
        return (float(self.getTotalValue()) / self.__balanceStart * 100)

    def getTotalMinValue(self):
        if len(self.__totalValuesArr) == 0:
            return 0
        return min(self.__totalValuesArr)

    def getTotalMinProcent(self):
        if len(self.__totalValuesArr) == 0:
            return 0
        return (float(self.getTotalMinValue()) / self.__balanceStart * 100)

    def getTotalMaxValue(self):
        if len(self.__totalValuesArr) == 0:
            return 0
        return max(self.__totalValuesArr)

    def getTotalMaxProcent(self):
        if len(self.__totalValuesArr) == 0:
            return 0
        return (float(self.getTotalMaxValue()) / self.__balanceStart * 100)

    def getTotalAverageValue(self):
        return sp.mean(self.__totalValuesArr)

    def getTotalAverageProcent(self):
        if len(self.__totalValuesArr) == 0:
            return 0
        return (float(self.getTotalAverageValue()) / self.__balanceStart * 100)

    def getTotalMedianValue(self):
        return sp.median(self.__totalValuesArr)

    def getTotalMedianProcent(self):
        if len(self.__totalValuesArr) == 0:
            return 0
        return (float(self.getTotalMedianValue()) / self.__balanceStart * 100)

    def getTotalVarianceValue(self):
        return sp.var(self.__totalValuesArr)

    def getTotalVarianceProcent(self):
        if len(self.__totalValuesArr) == 0:
            return 0
        return (float(self.getTotalVarianceValue()) / self.__balanceStart * 100)

    def getTotalStandardDeviationValue(self):
        return sp.std(self.__totalValuesArr)

    def getTotalStandardDeviationProcent(self):
        if len(self.__totalValuesArr) == 0:
            return 0
        return (float(self.getTotalStandardDeviationValue()) / self.__balanceStart * 100)
    
    def getProfitCount(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return len(self.__profitValuesArr)

    def getProfitValue(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return sum(self.__profitValuesArr)

    def getProfitProcent(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return (float(self.getProfitValue()) / self.__balanceStart * 100)

    def getProfitMinValue(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return min(self.__profitValuesArr)

    def getProfitMinProcent(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return (float(self.getProfitMinValue()) / self.__balanceStart * 100)

    def getProfitMaxValue(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return max(self.__profitValuesArr)

    def getProfitMaxProcent(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return (float(self.getProfitMaxValue()) / self.__balanceStart * 100)

    def getProfitAverageValue(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return sp.mean(self.__profitValuesArr)

    def getProfitAverageProcent(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return (float(self.getProfitAverageValue()) / self.__balanceStart * 100)

    def getProfitMedianValue(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return sp.median(self.__profitValuesArr)
        
    def getProfitMedianProcent(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return (float(self.getProfitMedianValue()) / self.__balanceStart * 100)

    def getProfitVarianceValue(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return sp.var(self.__profitValuesArr)

    def getProfitVarianceProcent(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return (float(self.getProfitVarianceValue()) / self.__balanceStart * 100)

    def getProfitStandardDeviationValue(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return sp.std(self.__profitValuesArr)

    def getProfitStandardDeviationProcent(self):
        if len(self.__profitValuesArr) == 0:
            return 0
        return (float(self.getProfitStandardDeviationValue()) / self.__balanceStart * 100)

    def getLossCount(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return len(self.__lossValuesArr)

    def getLossValue(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return sum(self.__lossValuesArr)

    def getLossProcent(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return (float(self.getLossValue()) / self.__balanceStart * 100)

    def getLossMinValue(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return min(self.__lossValuesArr)

    def getLossMinProcent(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return (float(self.getLossMinValue()) / self.__balanceStart * 100)

    def getLossMaxValue(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return max(self.__lossValuesArr)

    def getLossMaxProcent(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return (float(self.getLossMaxValue()) / self.__balanceStart * 100)

    def getLossAverageValue(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return sp.mean(self.__lossValuesArr)

    def getLossAverageProcent(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return (float(self.getLossAverageValue()) / self.__balanceStart * 100)

    def getLossMedianValue(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return sp.median(self.__lossValuesArr)
        
    def getLossMedianProcent(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return (float(self.getLossMedianValue()) / self.__balanceStart * 100)

    def getLossVarianceValue(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return sp.var(self.__lossValuesArr)

    def getLossVarianceProcent(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return (float(self.getLossVarianceValue()) / self.__balanceStart * 100)

    def getLossStandardDeviationValue(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return sp.std(self.__lossValuesArr)

    def getLossStandardDeviationProcent(self):
        if len(self.__lossValuesArr) == 0:
            return 0
        return (float(self.getLossStandardDeviationValue()) / self.__balanceStart * 100)

    def __resultLong(self):
        result = 0
        if self.__longPosStart is not 0 and self.__longPosEnd is not 0:
            result = self.__longPosEnd - self.__longPosStart
            result = self.__addMultiplierTransactionCostsSlippage(result)
            if result > 0:
                self.__totalValuesArr.append(result)
                self.__profitValuesArr.append(result)
            if result <= 0:
                self.__totalValuesArr.append(result)
                self.__lossValuesArr.append(result)
            self.__longPosStart = 0
            self.__longPosEnd = 0

            self.__balance += result

    def __resultShort(self):
        result = 0
        if self.__shortPosStart is not 0 and self.__shortPosEnd is not 0:
            result = self.__shortPosStart - self.__shortPosEnd
            result = self.__addMultiplierTransactionCostsSlippage(result)
            if result > 0:
                self.__totalValuesArr.append(result)
                self.__profitValuesArr.append(result)
            if result <= 0:
                self.__totalValuesArr.append(result)
                self.__lossValuesArr.append(result)
            self.__shortPosStart = 0
            self.__shortPosEnd = 0

            self.__balance += result

    def __addMultiplierTransactionCostsSlippage(self, result):
        result = result * self.__multiplier
        if self.__slippage > 0:
            result = result - (self.__slippage * self.__multiplier * 2)
        if self.__transactionCosts > 0:
            result = result - (self.__transactionCosts * 2)
        return result

    def _getFormatStr(self, value):
        return ('%.2f' % round(value, 2))

    def _enterLongSignal(self, bar):
        self._longSignal = True
        print (('%s ENTER LONG SIGNAL' % bar['datetime']))
#        print (('\a'))

    def _exitLongSignal(self, bar):
        self._longSignal = False
        print (('%s EXIT LONG SIGNAL' % bar['datetime']))
#        print (('\a'))

    def _enterShortSignal(self, bar):
        self._shortSignal = True
        print (('%s ENTER SHORT SIGNAL' % bar['datetime']))
#        print (('\a'))

    def _exitShortSignal(self, bar):
        self._shortSignal = False
        print (('%s EXIT SHORT SIGNAL' % bar['datetime']))
#        print (('\a'))

    def _enterLongPos(self, bar):
        self._longPos = True
        self.__longPosStart = bar['open']
        print ('%s ENTER LONG at € %s' %
        (bar['datetime'], self._getFormatStr(bar['open'])))

    def _exitLongPos(self, bar):
        self._longPos = False
        self.__longPosEnd = bar['open']
        print ('%s EXIT LONG at € %s' %
        (bar['datetime'], self._getFormatStr(bar['open'])))

    def _enterShortPos(self, bar):
        self._shortPos = True
        self.__shortPosStart = bar['open']
        print ('%s ENTER SHORT at € %s' %
        (bar['datetime'], self._getFormatStr(bar['open'])))

    def _exitShortPos(self, bar):
        self._shortPos = False
        self.__shortPosEnd = bar['open']
        print ('%s EXIT SHORT at € %s' %
        (bar['datetime'], self._getFormatStr(bar['open'])))

    def run(self):
        for bar in self.__bars:
            self.__setBarIndex()
            self._onBars(bar)
            self.__setBuyAndHold(bar)
            self.__resultLong()
            self.__resultShort()
            self.__setBarsInMarket()
            self.__setBarDrawdown(bar)
            self.__setBankruptcyDate(bar)

    def getAnalysis(self):

        headers = ['Total trades %s' % self.getTotalCount(), u'€', '%', 'Profit trades %s' % self.getProfitCount(), u'€', '%', 'Loss trades %s' % self.getLossCount(), u'€', '%']

        table = [
            ['Total result', self.getTotalValue(), self.getTotalProcent(), 'Total result', self.getProfitValue(), self.getProfitProcent(), 'Total result', self.getLossValue(), self.getLossProcent()],
            ['Max result', self.getTotalMaxValue(), self.getTotalMaxProcent(), 'Max result', self.getProfitMaxValue(), self.getProfitMaxProcent(), 'Max result', self.getLossMinValue(), self.getLossMinProcent()],
            ['Min result', self.getTotalMinValue(), self.getTotalMinProcent(), 'Min result', self.getProfitMinValue(), self.getProfitMinProcent(), 'Min result', self.getLossMaxValue(), self.getLossMaxProcent()],
            ['Average', self.getTotalAverageValue(), self.getTotalAverageProcent(), 'Average', self.getProfitAverageValue(), self.getProfitAverageProcent(), 'Average', self.getLossAverageValue(), self.getLossAverageProcent()],
            ['Median', self.getTotalMedianValue(), self.getTotalMedianProcent(), 'Median', self.getProfitMedianValue(), self.getProfitMedianProcent(), 'Median', self.getLossMedianValue(), self.getLossMedianProcent()],
            ['Variance', self.getTotalVarianceValue(), self.getTotalVarianceProcent(), 'Variance', self.getProfitVarianceValue(), self.getProfitVarianceProcent(), 'Variance', self.getLossVarianceValue(), self.getLossVarianceProcent()],
            ['Standard Deviation', self.getTotalStandardDeviationValue(), self.getTotalStandardDeviationProcent(), 'Standard Deviation', self.getProfitStandardDeviationValue(), self.getProfitStandardDeviationProcent(), 'Standard Deviation', self.getLossStandardDeviationValue(), self.getLossStandardDeviationProcent()]
        ]

        print tabulate(table, headers, tablefmt='grid', floatfmt='.4f')

        headers = ['Description', 'Value']

        table = [
            ['Sharpe Ratio', self.getSharpeRatio()],
            ['Hitrate %', self.getHitrate()],
            ['WS Index', self.getWsIndex()],
            ['RINA Index', self.getRinaIndex()],
            ['Total bars', self.getBarsTotal()],
            ['In market bars', self.getBarsInMarket()],
            ['In market %', self.getProcentInMarket()],
            [u'Result (buy & hold) €', self.getResultBuyAndHoldValue()],
            ['Result (buy & hold) %', self.getResultBuyAndHoldProcent()],
            ['Bankruptcy date', self.getBankruptcyDate()],
            [u'Max bar drawdown value €', self.getMaxBarDrawdownValue()],
            ['Consecutive drawdown count', self.getMaxConsecutiveDrawdownCount()],
            [u'Consecutive drawdown value €', self.getMaxConsecutiveDrawdownValue()],
            ['Risk of Ruin', self.getRiskOfRuin()],
            ['Risk of Ruin fixed position size %', self.getRiskOfRuinFixedPositionSize()],
            ['Risk of Ruin fixed fraction sizing %', self.getRiskOfRuinFixedFractionalPositionSizing()],
            ['Gambler Ruin problem using Markov Chains %', self.getGamblerRuinProblemUsingMarkovChains()]
        ]

        print tabulate(table, headers, tablefmt='grid', floatfmt='.4f')

