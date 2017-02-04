from jhbacktest.strategy import Strategy

import talib as ta
import jhtalib as jhta


class StrategyMy(Strategy):

    def __init__(self, df, n, slippage=0):
        """
        set trade indicator
        """
        Strategy.__init__(self, df, slippage)

        # problem with data:
#        self._indicator = ta.SMA(self.get_df_np('Close'), n)
#        self._indicator = jhta.SMA(self.get_df(), n)
        self._indicator = ta.MOM(self.get_df_np('Close'), n)
#        self._indicator = jhta.MOM(self.get_df(), n)

#    def on_bars(self, bar, print_output):
        """
        modify if you wish
        """
        
    def check_enter_long_signal(self, bar):
        """
        set enter long trade rules
        """
#        return (bar['Close'] > self._indicator[self.get_df_index()])
        return (self._indicator[self.get_df_index()] < 0)

    def check_exit_long_signal(self, bar):
        """
        set exit long trade rules
        """
#        return (bar['Close'] < self._indicator[self.get_df_index()])
        return (self._indicator[self.get_df_index()] > 0)
 
    def check_enter_short_signal(self, bar):
        """
        set enter short trade rules
        """
#        return (bar['Close'] < self._indicator[self.get_df_index()])
        return (self._indicator[self.get_df_index()] > 0)
 
    def check_exit_short_signal(self, bar):
        """
        set exit short trade rules
        """
#        return (bar['Close'] > self._indicator[self.get_df_index()])
        return (self._indicator[self.get_df_index()] < 0)

