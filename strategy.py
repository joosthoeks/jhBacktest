# -*- coding: utf-8 -*-

import numpy as np
import math


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

    def getResultBuyAndHoldEuro(self):
        result = self._posBuyAndHoldEnd - self._posBuyAndHoldStart
        result = self.__addMultiplierTransactionCostsSlippage(result)
        return result

    def getResultBuyAndHoldProcent(self):
        return (
            float(self.getResultBuyAndHoldEuro()) / self.__balanceStart * 100
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

    def getBankruptcyDate(self):
        return self.__bankruptcyDate

    def __setBankruptcyDate(self, bar):
        if self.__bankruptcyDate is 0:
            if (self.__balance < self.__bankruptcyAt):
                self.__bankruptcyDate = bar['datetime']

    def getMaxConsecutiveLossCount(self):
        lossCount = 0
        lossCountArr = []
        for value in self.__totalValuesArr:
            if value <= 0:
                lossCount += 1
            else:
                lossCountArr.append(lossCount)
                lossCount = 0
                
        return max(lossCountArr)

    def getMaxConsecutiveLossValue(self):
        lossValue = 0
        lossValueArr = []
        for value in self.__totalValuesArr:
            if value <= 0:
                lossValue += value
            else:
                lossValueArr.append(lossValue)
                lossValue = 0
                
        return min(lossValueArr)

    def getRiskOfRuin(self):
        edge = self.getHitrate() - 50
        capitalUnits = ((
            (self.__balanceStart - self.__bankruptcyAt)
        ) / (self.getLossValueAverage() * -1))
        return ((1 - edge) / (1 + edge)) ** round(capitalUnits)

    def getRiskOfRuinFixedPositionSize(self):
        e = 2.71828
        a = self.getAverageResultPerTradeProcent() / 100
        z = (float(self.__balanceStart - self.__bankruptcyAt) 
        / self.__balanceStart)
        d = self.getStandardDeviationProcent() / 100
        return (e ** - (2 * a * z / d ** 2)) * 100

    def getRiskOfRuinFixedFractionalPositionSizing(self):
        e = 2.71828
        a = self.getAverageResultPerTradeProcent() / 100
        z = (float(self.__balanceStart - self.__bankruptcyAt) 
        / self.__balanceStart)
        d = self.getStandardDeviationProcent() / 100
        return (e ** - ((2 * a / d) * math.log(1 - z) / math.log(1 - d))) * 100

    def getGamblerRuinProblemUsingMarkovChains(self):
        edge = (self.getHitrate() - 50) / 100
        q = .5 - edge
        p = .5 + edge
#        z = self.__balanceStart
        z = round(self.__balanceStart / self.getAverageResultPerTradeEuro())
#        m = self.__balanceTarget
        m = round(self.__balanceTarget / self.getAverageResultPerTradeEuro())
        return (((q / p) ** m - (q / p) ** z) / ((q / p) ** m - 1)) * 100
        
    def getTotalCount(self):
        return len(self.__totalValuesArr)

    def getResultEuro(self):
        return sum(self.__totalValuesArr)

    def getResultProcent(self):
        return (float(self.getResultEuro()) / self.__balanceStart * 100)

    def getAverageResultPerTradeEuro(self):
        return (float(self.getResultEuro()) / self.getTotalCount())

    def getAverageResultPerTradeProcent(self):
        return (
            float(self.getAverageResultPerTradeEuro()) 
            / self.__balanceStart * 100
        )

    def getStandardDeviationEuro(self):
        deviationsArr = []
        for result in self.__totalValuesArr:
            deviationsArr.append(result - self.getAverageResultPerTradeEuro())

        squareArr = []
        for deviation in deviationsArr:
            squareArr.append(deviation * deviation)

        averageSquare = sum(squareArr) / float(len(squareArr))

        standardDeviation = math.sqrt(averageSquare)

        return standardDeviation

    def getStandardDeviationProcent(self):
        return (
            float(self.getStandardDeviationEuro())
            / self.__balanceStart * 100
        )

    def getHitrate(self):
        return (float(self.getProfitCount()) / self.getTotalCount() * 100)

    def getWsIndex(self):
        return (
            (
                10000. * self.getAverageResultPerTradeEuro()
            ) / (
                self.getLossValueMin() * self.getProcentInMarket()
            )
        )

    def getRinaIndex(self):
        return (
            (
                self.getResultEuro()
            ) / (
                self.getLossValueAverage() * self.getProcentInMarket()
            )
        )

    def getProfitCount(self):
        return len(self.__profitValuesArr)

    def getProfitValue(self):
        return sum(self.__profitValuesArr)

    def getProfitValueMin(self):
        return min(self.__profitValuesArr)

    def getProfitValueMax(self):
        return max(self.__profitValuesArr)

    def getProfitValueAverage(self):
        return sum(self.__profitValuesArr) / float(len(self.__profitValuesArr))

    def getLossCount(self):
        return len(self.__lossValuesArr)

    def getLossValue(self):
        return sum(self.__lossValuesArr)

    def getLossValueMin(self):
        return min(self.__lossValuesArr)

    def getLossValueMax(self):
        return max(self.__lossValuesArr)

    def getLossValueAverage(self):
        return sum(self.__lossValuesArr) / float(len(self.__lossValuesArr))

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

    def _exitLongSignal(self, bar):
        self._longSignal = False
        print (('%s EXIT LONG SIGNAL' % bar['datetime']))

    def _enterShortSignal(self, bar):
        self._shortSignal = True
        print (('%s ENTER SHORT SIGNAL' % bar['datetime']))

    def _exitShortSignal(self, bar):
        self._shortSignal = False
        print (('%s EXIT SHORT SIGNAL' % bar['datetime']))

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
            self.__setBankruptcyDate(bar)

