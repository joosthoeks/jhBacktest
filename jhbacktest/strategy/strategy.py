from jhbacktest.data import *
import jhbacktest.stats as jhstats

from tabulate import tabulate
import termcolor as tc


class Strategy(object):

    def __init__(self, df, slippage=0):

        self.__df = df
        __data = Data()
        self.__df_np = __data.df2numpy(self.__df)
        self.__df_index = -1
        self.__long_signal = False
        self.__short_signal = False
        self.__long_pos = False
        self.__short_pos = False
        self.__bar_in_market = 0
        self.__bar_up_count = 0
        self.__bar_down_count = 0
        self.__slippage = slippage
        self.__buy_and_hold_pos_start = 0
        self.__buy_and_hold_pos_end = 0
        self.__benchmark_start = 0
        self.__benchmark_list = []
        self.__pos_long_dict = {}
        self.__pos_short_dict = {}
        self.__long_pos_start = 0
        self.__long_pos_end = 0
        self.__long_pos_count = 0
        self.__short_pos_start = 0
        self.__short_pos_end = 0
        self.__short_pos_count = 0
        self.__last_trade_bar_index = 0
        self.__total_values_list = []
        self.__profit_values_list = []
        self.__loss_values_list = []
        self.__bar_drawdown_list = []
        self.__position_drawdown_list = []
        self.__equity_curve = 0
        self.__equity_curve_list = []
        self.__open_equity_curve = 0
        self.__open_equity_curve_list = []

    def get_df(self):
        return self.__df

    def get_df_np(self, price='Close', index=None):
        if index is None:
            return self.__df_np[price]
        return self.__df_np[price][index]
 
    def get_total_values_list(self):
        return self.__total_values_list

    def set_buy_and_hold(self, bar):
        if self.__buy_and_hold_pos_start is 0:
            self.__buy_and_hold_pos_start = bar['Open']
        self.__buy_and_hold_pos_end = bar['Close']

    def get_result_buy_and_hold_absolute(self):
        result = self.__buy_and_hold_pos_end - self.__buy_and_hold_pos_start
        result = self.add_slippage(result)
        return result

    def set_benchmark_list(self, bar):
        benchmark = 0
        if self.__benchmark_start is 0:
            self.__benchmark_start = bar['Open']
        else:
            benchmark = bar['Open'] - self.__benchmark_start

        self.__benchmark_list.append(benchmark)

    def get_benchmark_list(self):
        return self.__benchmark_list

    def set_pos_long(self, pos):
        self.__pos_long_dict[self.get_df_index()] = pos

    def get_pos_long(self, key):
        return self.__pos_long_dict[key]

    def set_pos_short(self, pos):
        self.__pos_short_dict[self.get_df_index()] = pos

    def get_pos_short(self, key):
        return self.__pos_short_dict[key]

    def get_long_pos_start(self):
        return self.__long_pos_start

    def get_long_pos_end(self):
        return self.__long_pos_end

    def get_long_pos_count(self):
        return self.__long_pos_count

    def get_short_pos_start(self):
        return self.__short_pos_start

    def get_short_pos_end(self):
        return self.__short_pos_end

    def get_short_pos_count(self):
        return self.__short_pos_count

    def get_last_trade_bar_index(self):
        return self.__last_trade_bar_index

    def set_last_trade_bar_index(self, index):
        self.__last_trade_bar_index += 1

    def get_df_index(self):
        return self.__df_index

    def set_df_index(self):
        self.__df_index += 1

    def get_bars_total(self):
        return self.__df_index + 1

    def get_bars_in_market(self):
        return self.__bar_in_market

    def set_bars_in_market(self):
        if self.__long_pos or self.__short_pos:
            self.__bar_in_market += 1

    def get_procent_in_market(self):
        return (float(self.get_bars_in_market()) / self.get_bars_total() * 100)

    def set_bar_up_count(self, bar):
        if bar['Open'] < bar['Close']:
            self.__bar_up_count += 1

    def get_bar_up_count(self):
        return self.__bar_up_count

    def set_bar_down_count(self, bar):
        if bar['Open'] > bar['Close']:
            self.__bar_down_count += 1

    def get_bar_down_count(self):
        return self.__bar_down_count

    def get_long_pos_count(self):
        return self.__long_pos_count

    def get_short_pos_count(self):
        return self.__short_pos_count

    def get_max_bar_drawdown_absolute(self):
        if len(self.__bar_drawdown_list) == 0:
            return 0
        return max(self.__bar_drawdown_list) * -1

    def get_max_position_drawdown_absolute(self):
        if len(self.__position_drawdown_list) == 0:
            return 0
        return max(self.__position_drawdown_list) * -1

    def set_drawdown(self, bar):
        if self.__long_pos:
            bar_drawdown = (bar['Open'] - bar['Low'])
            position_drawdown = (self.__long_pos_start - bar['Low'])
        elif self.__short_pos:
            bar_drawdown = (bar['High'] - bar['Open'])
            position_drawdown = (bar['High'] - self.__short_pos_start)
        else:
            bar_drawdown = 0
            position_drawdown = 0
        self.__bar_drawdown_list.append(bar_drawdown)
        self.__position_drawdown_list.append(position_drawdown)

    def get_max_consecutive_loss_count(self):
        loss_count = 0
        loss_count_list = []
        for value in self.__total_values_list:
            if value < 0:
                loss_count += 1
                loss_count_list.append(loss_count)
            else:
                loss_count = 0
                
        if len(loss_count_list) == 0:
            return 0
        return max(loss_count_list)

    def get_max_consecutive_loss_absolute(self):
        loss_value = 0
        loss_value_list = []
        for value in self.__total_values_list:
            if value < 0:
                loss_value += value
                loss_value_list.append(loss_value)
            else:
                loss_value = 0
                
        if len(loss_value_list) == 0:
            return 0
        return min(loss_value_list)

    def get_max_consecutive_profit_count(self):
        profit_count = 0
        profit_count_list = []
        for value in self.__total_values_list:
            if value > 0:
                profit_count += 1
                profit_count_list.append(profit_count)
            else:
                profit_count = 0
                
        if len(profit_count_list) == 0:
            return 0
        return max(profit_count_list)

    def get_max_consecutive_profit_absolute(self):
        profit_value = 0
        profit_value_list = []
        for value in self.__total_values_list:
            if value > 0:
                profit_value += value
                profit_value_list.append(profit_value)
            else:
                profit_value = 0
                
        if len(profit_value_list) == 0:
            return 0
        return max(profit_value_list)

    def set_equity_curve(self, bar):
        """
        set equity curve
        """
        result = 0
        if self.__long_pos_start is not 0 and self.__long_pos_end is not 0:
            result = self.__long_pos_end - self.__long_pos_start
            result = self.add_slippage(result)
            self.__total_values_list.append(result)
            if result > 0:
                self.__profit_values_list.append(result)
            else:
                self.__loss_values_list.append(result)
            self.__long_pos_start = 0
            self.__long_pos_end = 0

        if self.__short_pos_start is not 0 and self.__short_pos_end is not 0:
            result = self.__short_pos_start - self.__short_pos_end
            result = self.add_slippage(result)
            self.__total_values_list.append(result)
            if result > 0:
                self.__profit_values_list.append(result)
            else:
                self.__loss_values_list.append(result)
            self.__short_pos_start = 0
            self.__short_pos_end = 0

        self.__equity_curve += result
        self.__equity_curve_list.append(self.__equity_curve)

    def get_equity_curve_list(self):
        return self.__equity_curve_list
        
# TODO
# problem with open equity curve:
    def set_open_equity_curve(self, bar):
        """
        set open equity curve
        """
        open_price = bar['Open']
        price = bar['Close']
        last_price = self.__df['Close'][self.get_df_index() - 1]
        open_result = 0

        open_result_long = 0
        if self.get_pos_long(self.get_df_index()) is 'start':
            open_result_long = price - open_price
        if self.get_pos_long(self.get_df_index()) is 'end':
            open_result_long = last_price - open_price
        if self.get_pos_long(self.get_df_index()) is 'in':
            open_result_long = price - last_price
        
        open_result_short = 0
        if self.get_pos_short(self.get_df_index()) is 'start':
            open_result_short = open_price - price
        if self.get_pos_short(self.get_df_index()) is 'end':
            open_result_short = open_price - last_price
        if self.get_pos_short(self.get_df_index()) is 'in':
            open_result_short = last_price - price
        
        open_result = open_result_long + open_result_short
        self.__open_equity_curve += open_result
        self.__open_equity_curve_list.append(self.__open_equity_curve)

    def get_open_equity_curve_list(self):
        return self.__open_equity_curve_list
        
    def add_slippage(self, result):
        if self.__slippage > 0:
            result = result - (self.__slippage * 2)
        return result

    def get_format_str(self, value):
        return ('%.2f' % round(value, 2))

    def enter_long_signal(self, bar, print_output):
        self.__long_signal = True
        if print_output:
            print ('%s ################################################### ENTER LONG SIGNAL ############################' % bar['datetime'])

    def exit_long_signal(self, bar, print_output):
        self.__long_signal = False
        if print_output:
            print ('%s ################################################### EXIT LONG SIGNAL #############################' % bar['datetime'])

    def enter_short_signal(self, bar, print_output):
        self.__short_signal = True
        if print_output:
            print ('%s ################################################### ENTER SHORT SIGNAL ###########################' % bar['datetime'])

    def exit_short_signal(self, bar, print_output):
        self.__short_signal = False
        if print_output:
            print ('%s ################################################### EXIT SHORT SIGNAL ############################' % bar['datetime'])

    def enter_long_pos(self, bar, print_output):
        self.__long_pos = True
        self.__long_pos_start = bar['Open']
        self.__long_pos_count += 1
        self.set_pos_long('enter')
        self.set_last_trade_bar_index(self.get_df_index())
        if print_output:
            print ('%s ################################################### ENTER LONG AT %s #########################' % \
            (bar['datetime'], self.get_format_str(bar['Open'])))

    def exit_long_pos(self, bar, print_output):
        self.__long_pos = False
        self.__long_pos_end = bar['Open']
        self.set_pos_long('exit')
        self.set_last_trade_bar_index(0)
        profit = self.__long_pos_end - self.__long_pos_start
        color = 'red'
        if profit > 0:
            color = 'green'
        if print_output:
            print ('%s ################################################### EXIT LONG AT %s ########################## PROFIT: %s' % \
            (bar['datetime'], self.get_format_str(bar['Open']), tc.colored(profit, color)))

    def enter_short_pos(self, bar, print_output):
        self.__short_pos = True
        self.__short_pos_start = bar['Open']
        self.__short_pos_count += 1
        self.set_pos_short('enter')
        self.set_last_trade_bar_index(self.get_df_index())
        if print_output:
            print ('%s ################################################### ENTER SHORT AT %s ########################' % \
            (bar['datetime'], self.get_format_str(bar['Open'])))

    def exit_short_pos(self, bar, print_output):
        self.__short_pos = False
        self.__short_pos_end = bar['Open']
        self.set_pos_short('exit')
        self.set_last_trade_bar_index(0)
        profit = self.__short_pos_start - self.__short_pos_end
        color = 'red'
        if profit > 0:
            color = 'green'
        if print_output:
            print ('%s ################################################### EXIT SHORT AT %s ######################### PROFIT: %s' % \
            (bar['datetime'], self.get_format_str(bar['Open']), tc.colored(profit, color)))

    def check_do_long_pos(self, bar, print_output):
        # check and do long position:
        if self.__long_signal:
            if self.__long_pos is False:
                self.enter_long_pos(bar, print_output)
        else:
            if self.__long_pos:
                self.exit_long_pos(bar, print_output)

    def check_do_short_pos(self, bar, print_output):
        # check and do short position:
        if self.__short_signal:
            if self.__short_pos is False:
                self.enter_short_pos(bar, print_output)
        else:
            if self.__short_pos:
                self.exit_short_pos(bar, print_output)

    def on_bars(self, bar, print_output):
        # current bar:
        if print_output:
            print (('%s Open: %s High: %s Low: %s Close: %s Volume: %s indicator: %s' % \
            (
                bar['datetime'],
                self.get_format_str(bar['Open']),
                self.get_format_str(bar['High']),
                self.get_format_str(bar['Low']),
                self.get_format_str(bar['Close']),
                bar['Volume'],
#                self.get_format_str(indicator)
                self.get_color(self._indicator[self.get_df_index()])
            )))

    def check_do_long_signal(self, bar, print_output):
        # check and do long signal:
        if self.__long_signal:
            if self.check_exit_long_signal(bar):
                self.exit_long_signal(bar, print_output)
        else:
            if self.check_enter_long_signal(bar):
                self.enter_long_signal(bar, print_output)

    def check_do_short_signal(self, bar, print_output):
        # check and do short signal:
        if self.__short_signal:
            if self.check_exit_short_signal(bar):
                self.exit_short_signal(bar, print_output)
        else:
            if self.check_enter_short_signal(bar):
                self.enter_short_signal(bar, print_output)

    def run(self, print_output=True):
        i = 0
        while i < len(self.__df['Close']):
            bar = {}
            bar['datetime'] = self.__df['datetime'][i]
            bar['Open'] = self.__df['Open'][i]
            bar['High'] = self.__df['High'][i]
            bar['Low'] = self.__df['Low'][i]
            bar['Close'] = self.__df['Close'][i]
            bar['Volume'] = self.__df['Volume'][i]
            self.set_df_index()
            self.check_do_long_pos(bar, print_output)
            self.check_do_short_pos(bar, print_output)
            self.set_pos_long('out')
            if self.__long_pos:
                self.set_pos_long('in')
            self.set_pos_short('out')
            if self.__short_pos:
                self.set_pos_short('in')
            self.on_bars(bar, print_output)
            self.check_do_long_signal(bar, print_output)
            self.check_do_short_signal(bar, print_output)
            self.set_buy_and_hold(bar)
            self.set_benchmark_list(bar)
            self.set_equity_curve(bar)
            self.set_open_equity_curve(bar)
            self.set_bars_in_market()
            self.set_bar_up_count(bar)
            self.set_bar_down_count(bar)
            self.set_drawdown(bar)
            i += 1

    def get_analysis(self):

        headers = [
            'Total trades %s' % jhstats.get_count(self.__total_values_list), 'Absolute',
            'Profit trades %s' % jhstats.get_count(self.__profit_values_list), 'Absolute',
            'Loss trades %s' % jhstats.get_count(self.__loss_values_list), 'Absolute'
        ]

        table = [
            [
                'Total result', self.get_color(jhstats.get_absolute(self.__total_values_list)),
                'Total result', self.get_color(jhstats.get_absolute(self.__profit_values_list)),
                'Total result', self.get_color(jhstats.get_absolute(self.__loss_values_list))
            ],
            [
                'Max result', self.get_color(jhstats.get_max_absolute(self.__total_values_list)),
                'Max result', self.get_color(jhstats.get_max_absolute(self.__profit_values_list)),
                'Max result', self.get_color(jhstats.get_max_absolute(self.__loss_values_list))
            ],
            [
                'Min result', self.get_color(jhstats.get_min_absolute(self.__total_values_list)),
                'Min result', self.get_color(jhstats.get_min_absolute(self.__profit_values_list)),
                'Min result', self.get_color(jhstats.get_min_absolute(self.__loss_values_list))
            ],
            [
                'Mean', self.get_color(jhstats.get_mean_absolute(self.__total_values_list)),
                'Mean', self.get_color(jhstats.get_mean_absolute(self.__profit_values_list)),
                'Mean', self.get_color(jhstats.get_mean_absolute(self.__loss_values_list))
            ],
            [
                'Median', self.get_color(jhstats.get_median_absolute(self.__total_values_list)),
                'Median', self.get_color(jhstats.get_median_absolute(self.__profit_values_list)),
                'Median', self.get_color(jhstats.get_median_absolute(self.__loss_values_list))
            ],
            [
                'Variance', self.get_color(jhstats.get_variance_absolute(self.__total_values_list)),
                'Variance', self.get_color(jhstats.get_variance_absolute(self.__profit_values_list)),
                'Variance', self.get_color(jhstats.get_variance_absolute(self.__loss_values_list))
            ],
            [
                'Std Dev', self.get_color(jhstats.get_std_dev_absolute(self.__total_values_list)),
                'Std Dev', self.get_color(jhstats.get_std_dev_absolute(self.__profit_values_list)),
                'Std Dev', self.get_color(jhstats.get_std_dev_absolute(self.__loss_values_list))
            ]
        ]

        print (tabulate(table, headers, tablefmt='grid', floatfmt='.4f'))

        headers = ['Description', 'Value']

        table = [
            ['Hitrate %', self.get_color(jhstats.get_hitrate(self.__total_values_list, self.__profit_values_list), 50)],
            ['Profit Loss Ratio', self.get_color(jhstats.get_profit_loss_ratio(jhstats.get_mean_absolute(self.__profit_values_list), jhstats.get_mean_absolute(self.__loss_values_list)), 1)],
            ['Expected Value', self.get_color(jhstats.get_expected_value(jhstats.get_hitrate(self.__total_values_list, self.__profit_values_list), jhstats.get_mean_absolute(self.__profit_values_list), jhstats.get_mean_absolute(self.__loss_values_list)))],
            ['Probability of Ruin (POR) (table of Lucas & LeBeau)', jhstats.get_por_lucas_and_lebeau(jhstats.get_hitrate(self.__total_values_list, self.__profit_values_list), jhstats.get_mean_absolute(self.__profit_values_list), jhstats.get_mean_absolute(self.__loss_values_list))],
            ['Total bars', self.get_bars_total()],
            ['Up bars', self.get_bar_up_count()],
            ['Down bars', self.get_bar_down_count()],
            ['In market bars', self.get_bars_in_market()],
            ['In market %', self.get_procent_in_market()],
            ['Long positions', self.get_long_pos_count()],
            ['Short positions', self.get_short_pos_count()],
            ['Result (buy & hold) absolute', self.get_color(self.get_result_buy_and_hold_absolute())]
        ]

        print (tabulate(table, headers, tablefmt='grid', floatfmt='.4f'))

        headers = ['Description', 'Value', 'Description', 'Value', 'Description', 'Value']

        table = [
            [
                'Consecutive profit count', self.get_max_consecutive_profit_count(),
                'Consecutive loss count', self.get_max_consecutive_loss_count(),
                'Max bar drawdown absolute', self.get_color(self.get_max_bar_drawdown_absolute())
            ],
            [
                'Consecutive profit absolute', self.get_color(self.get_max_consecutive_profit_absolute()),
                'Consecutive loss absolute', self.get_color(self.get_max_consecutive_loss_absolute()),
                'Max position drawdown absolute', self.get_color(self.get_max_position_drawdown_absolute())
            ]
        ]

        print (tabulate(table, headers, tablefmt='grid', floatfmt='.4f'))

    def get_color(self, value, split=0):
        color = 'red'
        if value > split:
            color = 'green'
        return tc.colored(value, color)

