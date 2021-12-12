

from jhbacktest.backtest import Backtest

import jhtalib as jhta


class BacktestExample(Backtest):

    def __init__(self, df, n):
        """
        set trade indicator
        """
        super().__init__(df)

        self._indicator = jhta.SMA(self.get_df(), n)
#        self._indicator = jhta.MOM(self.get_df(), n)

    def check_enter_long_signal(self, bar):
        """
        set enter long trade rules
        """
        return (bar['Close'] > self._indicator[self.get_df_index()])
#        return (self._indicator[self.get_df_index()] > 0)

    def check_exit_long_signal(self, bar):
        """
        set exit long trade rules
        """
        return (bar['Close'] < self._indicator[self.get_df_index()])
#        return (self._indicator[self.get_df_index()] < 0)
 
    def check_enter_short_signal(self, bar):
        """
        set enter short trade rules
        """
        return (bar['Close'] < self._indicator[self.get_df_index()])
#        return (self._indicator[self.get_df_index()] < 0)
 
    def check_exit_short_signal(self, bar):
        """
        set exit short trade rules
        """
        return (bar['Close'] > self._indicator[self.get_df_index()])
#        return (self._indicator[self.get_df_index()] > 0)

