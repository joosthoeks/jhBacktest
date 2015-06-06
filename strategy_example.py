# -*- coding: utf-8 -*-

from strategy import Strategy

import numpy as np
import talib as ta


class StrategyExample(Strategy):

    def __init__(self, bars, balanceStart, bankruptcyAt, balanceTarget,
        multiplier, transactionCosts, slippage, smaPeriod):

        Strategy.__init__(self, bars, balanceStart, bankruptcyAt, balanceTarget,
            multiplier, transactionCosts, slippage)

        self.__sma = ta.SMA(self._barsNP['close'], smaPeriod)

    def _onBars(self, bar):
        # Wait for enough bars to be available to calculate SMA
        if (np.isnan(self.__sma[self.getBarIndex()])):
            print (('%s is nan o: %s' % (bar['datetime'], bar['open'])))
            return

        # check and do long position:
        if self._longSignal:
            if self._longPos is False:
                self._enterLongPos(bar)
        else:
            if self._longPos:
                self._exitLongPos(bar)

        # check and do short position:
        if self._shortSignal:
            if self._shortPos is False:
                self._enterShortPos(bar)
        else:
            if self._shortPos:
                self._exitShortPos(bar)

        # current bar:
        print (('%s o: %s h: %s l: %s c: %s sma: %s' %
        (bar['datetime'],
            self._getFormatStr(bar['open']),
            self._getFormatStr(bar['high']),
            self._getFormatStr(bar['low']),
            self._getFormatStr(bar['close']),
            self._getFormatStr(self.__sma[self.getBarIndex()])
        )))

        # check and do long signals:
        if self._longSignal:
            if self.__checkExitLongSignal(bar):
                self._exitLongSignal(bar)
        else:
            if self.__checkEnterLongSignal(bar):
                self._enterLongSignal(bar)

        # check and do short signals:
        if self._shortSignal:
            if self.__checkExitShortSignal(bar):
                self._exitShortSignal(bar)
        else:
            if self.__checkEnterShortSignal(bar):
                self._enterShortSignal(bar)

    def __checkEnterLongSignal(self, bar):
        return (bar['close'] > self.__sma[self.getBarIndex()])

    def __checkExitLongSignal(self, bar):
        return (bar['close'] < self.__sma[self.getBarIndex()])

    def __checkEnterShortSignal(self, bar):
        return (bar['close'] < self.__sma[self.getBarIndex()])

    def __checkExitShortSignal(self, bar):
        return (bar['close'] > self.__sma[self.getBarIndex()])

