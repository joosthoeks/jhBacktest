from jhbacktest.strategy import Strategy

import talib as ta


class StrategyMy(Strategy):

    def __init__(self, bars, timeperiod, slippage=0):
        """
        set trade indicator
        """
        Strategy.__init__(self, bars, slippage)

#        self._indicator = ta.SMA(self.get_bars_pd('Close'), timeperiod)
        self._indicator = ta.MOM(self.get_bars_np('Close'), timeperiod)

#    def on_bars(self, bar, print_output):
        """
        modify if you wish
        """
        
    def check_enter_long_signal(self, bar):
        """
        set enter long trade rules
        """
#        return (bar['Close'] > self._indicator[self.get_bar_index()])
        return (self._indicator[self.get_bar_index()] < 0)

    def check_exit_long_signal(self, bar):
        """
        set exit long trade rules
        """
#        return (bar['Close'] < self._indicator[self.get_bar_index()])
        return (self._indicator[self.get_bar_index()] > 0)
 
    def check_enter_short_signal(self, bar):
        """
        set enter short trade rules
        """
#        return (bar['Close'] < self._indicator[self.get_bar_index()])
        return (self._indicator[self.get_bar_index()] > 0)
 
    def check_exit_short_signal(self, bar):
        """
        set exit short trade rules
        """
#        return (bar['Close'] > self._indicator[self.get_bar_index()])
        return (self._indicator[self.get_bar_index()] < 0)

