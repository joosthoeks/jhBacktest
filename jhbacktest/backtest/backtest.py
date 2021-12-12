

# Import Built-Ins:
import csv
from datetime import datetime as dt
#from pprint import pprint as pp

# Import Third-Party:
import matplotlib.pyplot as plt
from tabulate import tabulate as tb
import termcolor as tc
import jhtalib as jhta

# Import Homebrew:


class Backtest(object):
    """
    Backtest.
    """
    
    def __init__(self, df):
        self.__df = df
        self.__add_col_trade_price()
        self.__add_cols(self.__df)
        self.__long_signal = 0
        self.__short_signal = 0
        self.__long_pos = False
        self.__short_pos = False
        self.__long_pos_start = 0
        self.__short_pos_start = 0
        self.__long_pos_count = 0
        self.__short_pos_count = 0
        self.__long_pnl = 0
        self.__long_pnl_cum = 0
        self.__short_pnl = 0
        self.__short_pnl_cum = 0
        self.__closed_equity_curve = 0
        self.__open_equity_curve = 0
        self.__trades_total_list = []
        self.__trades_profit_list = []
        self.__trades_loss_list = []
        self.__bars_up = 0
        self.__bars_down = 0
        self.__bars_in_market = 0
        self.__drawdown_bar_list = []
        self.__drawdown_position_list = []

    def __add_col_trade_price(self):
        self.__df['trade_price'] = list(self.__df['Open'])
        del self.__df['trade_price'][0]
        self.__df['trade_price'].append(float('NaN'))

    def __add_cols(self, df):
        self.__df['long_signal'] = []
        self.__df['short_signal'] = []
        self.__df['signal'] = []
        self.__df['long_pnl'] = []
        self.__df['long_pnl_cum'] = []
        self.__df['short_pnl'] = []
        self.__df['short_pnl_cum'] = []
        self.__df['pnl'] = []
        self.__df['closed_equity_curve'] = []
        self.__df['pnl_open'] = []
        self.__df['open_equity_curve'] = []
        self.__df['Benchmark'] = []

    def __check_do_long_signal(self, bar):
        # check and do long signal:
        self.__long_pnl = 0
        if self.__long_signal == 1:
            if self.check_exit_long_signal(bar):
                self.__exit_long_pos(bar['trade_price'])
        else:
            if self.check_enter_long_signal(bar):
                self.__enter_long_pos(bar['trade_price'])
        return self.__long_signal

    def __check_do_short_signal(self, bar):
        # check and do short signal:
        self.__short_pnl = 0
        if self.__short_signal == -1:
            if self.check_exit_short_signal(bar):
                self.__exit_short_pos(bar['trade_price'])
        else:
            if self.check_enter_short_signal(bar):
                self.__enter_short_pos(bar['trade_price'])
        return self.__short_signal

    def __enter_long_pos(self, price):
        self.__long_pos = True
        self.__long_pos_start = price
        self.__long_pos_count += 1
        self.__long_signal = 1

    def __exit_long_pos(self, price):
        self.__long_pnl = price - self.__long_pos_start
        self.__long_pos = False
        self.__long_pos_start = 0
        self.__long_signal = 0

    def __enter_short_pos(self, price):
        self.__short_pos = True
        self.__short_pos_start = price
        self.__short_pos_count += 1
        self.__short_signal = -1

    def __exit_short_pos(self, price):
        self.__short_pnl = self.__short_pos_start - price
        self.__short_pos = False
        self.__short_pos_start = 0
        self.__short_signal = 0

    def __get_bar(self, i):
        bar = {}
        bar['datetime'] = self.__df['datetime'][i]
        bar['Open'] = self.__df['Open'][i]
        bar['High'] = self.__df['High'][i]
        bar['Low'] = self.__df['Low'][i]
        bar['Close'] = self.__df['Close'][i]
        bar['Volume'] = self.__df['Volume'][i]
        bar['trade_price'] = self.__df['trade_price'][i]
        return bar

    def get_df(self):
        return self.__df

    def __set_df_index(self, i):
        self.__df_index = i

    def get_df_index(self):
        return self.__df_index

    def __get_format_str(self, value):
        return '{0:.8f}'.format(value)

    def __get_color(self, value, split=0):
        color = 'red'
        if float(value) > split:
            color = 'green'
        return tc.colored(value, color)

    def __get_pnl_open(self, price):
        long_pnl = 0
        short_pnl = 0
        if self.__long_pos:
            long_pnl = price - self.__long_pos_start
        if self.__short_pos:
            short_pnl = self.__short_pos_start - price
        return long_pnl + short_pnl

    def __set_trade(self, pnl):
        if pnl != 0:
            self.__trades_total_list.append(pnl)
            if pnl > 0:
                self.__trades_profit_list.append(pnl)
            else:
                self.__trades_loss_list.append(pnl)

    def get_mean(self, list):
        return sum(list) / len(list)

    def get_trades_total(self):
        return self.__trades_total_list

    def get_trades_profit(self):
        return self.__trades_profit_list
    
    def get_trades_loss(self):
        return self.__trades_loss_list
    
    def __set_bars_up(self, bar):
        if bar['Open'] < bar['Close']:
            self.__bars_up += 1

    def __set_bars_down(self, bar):
        if bar['Open'] > bar['Close']:
            self.__bars_down += 1
    
    def __set_bars_in_market(self):
        if self.__long_pos or self.__short_pos:
            self.__bars_in_market += 1

    def __set_drawdown(self, bar):
        if self.__long_pos:
#            drawdown_bar = (bar['Open'] - bar['Low'])
            drawdown_bar = (bar['trade_price'] - bar['Low'])
            drawdown_position = (self.__long_pos_start - bar['Low'])
        elif self.__short_pos:
#            drawdown_bar = (bar['High'] - bar['Open'])
            drawdown_bar = (bar['High'] - bar['trade_price'])
            drawdown_position = (bar['High'] - self.__short_pos_start)
        else:
            drawdown_bar = 0
            drawdown_position = 0
        self.__drawdown_bar_list.append(drawdown_bar)
        self.__drawdown_position_list.append(drawdown_position)

    def get_bars_total(self):
        return len(self.get_df()['Close'])

    def get_bars_up(self):
        return self.__bars_up

    def get_bars_down(self):
        return self.__bars_down
    
    def get_bars_in_market(self):
        return self.__bars_in_market

    def get_percent_in_market(self):
        return self.get_bars_in_market() / self.get_bars_total()

    def get_pos_long(self):
        return self.__long_pos_count

    def get_pos_short(self):
        return self.__short_pos_count

    def get_result_benchmark(self):
        return self.__df['Benchmark'][-2]

    def get_drawdown_bar_max(self):
#        if len(self.__drawdown_bar_list) == 0:
#            return 0
        return max(self.__drawdown_bar_list) * -1

    def get_drawdown_position_max(self):
#        if len(self.__drawdown_position_list) == 0:
#            return 0
        return max(self.__drawdown_position_list) * -1

    def get_max_consecutive_loss_count(self):
        loss_count = 0
        loss_count_list = []
        for pnl in self.__trades_total_list:
            if pnl < 0:
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
        for pnl in self.__trades_total_list:
            if pnl < 0:
                loss_value += pnl
                loss_value_list.append(loss_value)
            else:
                loss_value = 0
                
        if len(loss_value_list) == 0:
            return 0
        return min(loss_value_list)

    def get_max_consecutive_profit_count(self):
        profit_count = 0
        profit_count_list = []
        for pnl in self.__trades_total_list:
            if pnl > 0:
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
        for pnl in self.__trades_total_list:
            if pnl > 0:
                profit_value += pnl
                profit_value_list.append(profit_value)
            else:
                profit_value = 0
                
        if len(profit_value_list) == 0:
            return 0
        return max(profit_value_list)

    def run(self):

        for i in range(len(self.__df['Close'])):
            self.__set_df_index(i)
            bar = self.__get_bar(i)
            self.__df['long_signal'].append(self.__check_do_long_signal(bar))
            self.__df['short_signal'].append(self.__check_do_short_signal(bar))

            signal = self.__df['long_signal'][-1] + self.__df['short_signal'][-1]
            self.__df['signal'].append(signal)

            self.__df['long_pnl'].append(self.__long_pnl)
            self.__long_pnl_cum += self.__long_pnl
            self.__df['long_pnl_cum'].append(self.__long_pnl_cum)

            self.__df['short_pnl'].append(self.__short_pnl)
            self.__short_pnl_cum += self.__short_pnl
            self.__df['short_pnl_cum'].append(self.__short_pnl_cum)

            pnl = self.__long_pnl + self.__short_pnl
            self.__df['pnl'].append(pnl)
            self.__set_trade(pnl)
            self.__closed_equity_curve += pnl
            self.__df['closed_equity_curve'].append(self.__closed_equity_curve)

            pnl_open = self.__get_pnl_open(self.__df['trade_price'][i])
            self.__df['pnl_open'].append(pnl_open)

            open_equity_curve = pnl_open + self.__df['closed_equity_curve'][i]
            if self.__df['closed_equity_curve'][i] != self.__df['closed_equity_curve'][i - 1]:
                open_equity_curve = self.__df['closed_equity_curve'][i]
            self.__df['open_equity_curve'].append(open_equity_curve)

            benchmark = self.__df['trade_price'][i] - self.__df['trade_price'][0]
            self.__df['Benchmark'].append(benchmark)

            self.__set_bars_up(bar)
            self.__set_bars_down(bar)
            self.__set_bars_in_market()
            self.__set_drawdown(bar)

    def save(self, csv_file_path):
        with open(csv_file_path, 'w') as f:
            w = csv.writer(f)
            w.writerow(self.__df.keys())
            w.writerows(zip(*self.__df.values()))

    def print_result(self):

        headers = [
            'Total trades {}'.format(len(self.get_trades_total())), 'Absolute',
            'Profit trades {}'.format(len(self.get_trades_profit())), 'Absolute',
            'Loss trades {}'.format(len(self.get_trades_loss())), 'Absolute'
        ]

        table = [
            [
                'Total result', self.get_color(sum(self.get_trades_total())),
                'Total result', self.get_color(sum(self.get_trades_profit())),
                'Total result', self.get_color(sum(self.get_trades_loss()))
            ],
            [
                'Max result', self.get_color(max(self.get_trades_total())),
                'Max result', self.get_color(max(self.get_trades_profit())),
                'Max result', self.get_color(max(self.get_trades_loss()))
            ],
            [
                'Min result', self.get_color(min(self.get_trades_total())),
                'Min result', self.get_color(min(self.get_trades_profit())),
                'Min result', self.get_color(min(self.get_trades_loss()))
            ],
            [
                'Mean', self.get_color(self.get_mean(self.get_trades_total())),
                'Mean', self.get_color(self.get_mean(self.get_trades_profit())),
                'Mean', self.get_color(self.get_mean(self.get_trades_loss()))
            ],
        ]

        print (tb(table, headers, tablefmt='grid', floatfmt='.4f'))

        count_trades_total = len(self.get_trades_total())
        count_trades_profit = len(self.get_trades_profit())
        hitrate = jhta.HR(count_trades_profit, count_trades_total)
        mean_trades_total = self.get_mean(self.get_trades_total())
        mean_trades_profit = self.get_mean(self.get_trades_profit())
        mean_trades_loss = self.get_mean(self.get_trades_loss())
        mean_trades_loss *= -1
        profit_loss_ratio = jhta.PLR(mean_trades_profit, mean_trades_loss)
        expected_value = jhta.EV(hitrate, mean_trades_profit, mean_trades_loss)
        probability_of_ruin = jhta.POR(hitrate, profit_loss_ratio)

        headers = ['Description', 'Value']

        table = [
            ['Hitrate %', self.get_color(hitrate * 100, 50)],
            ['Profit Loss Ratio', self.get_color(profit_loss_ratio, 1)],
            ['Expected Value', self.get_color(expected_value)],
            ['Probability of Ruin (POR) (table of Lucas & LeBeau)', probability_of_ruin],
            ['Total bars', self.get_bars_total()],
            ['Up bars', self.get_bars_up()],
            ['Down bars', self.get_bars_down()],
            ['In market bars', self.get_bars_in_market()],
            ['In market %', self.get_percent_in_market() * 100],
            ['Long positions', self.get_pos_long()],
            ['Short positions', self.get_pos_short()],
            ['Result benchmark (buy & hold)', self.get_color(self.get_result_benchmark())]
        ]

        print (tb(table, headers, tablefmt='grid', floatfmt='.4f'))

        headers = ['Description', 'Value', 'Description', 'Value', 'Description', 'Value']

        table = [
            [
                'Consecutive profit count', self.get_max_consecutive_profit_count(),
                'Consecutive loss count', self.get_max_consecutive_loss_count(),
                'Max bar drawdown absolute', self.get_color(self.get_drawdown_bar_max())
            ],
            [
                'Consecutive profit absolute', self.get_color(self.get_max_consecutive_profit_absolute()),
                'Consecutive loss absolute', self.get_color(self.get_max_consecutive_loss_absolute()),
                'Max position drawdown absolute', self.get_color(self.get_drawdown_position_max())
            ]
        ]

        print (tb(table, headers, tablefmt='grid', floatfmt='.4f'))

    def plot_optimization_curve(self, x_list, y_list):
        plt.plot(x_list, y_list)
        plt.title('Optimization Curve')
        plt.grid(True)
        plt.show()

    def plot_benchmark_vs_result(self, date_format='%Y%m%d'):
        x = [dt.strptime(d, date_format).date() for d in self.__df['datetime']]
#        plt.plot(x, self.__df['trade_price'], label='trade_price')
        plt.plot(x, self.__df['Benchmark'], label='Benchmark')
        plt.plot(x, self.__df['closed_equity_curve'], label='closed_equity_curve')
        plt.plot(x, self.__df['open_equity_curve'], label='open_equity_curve')
        plt.legend(loc='upper left')
        plt.gcf().autofmt_xdate()
        plt.title('Benchmark vs Result')
        plt.grid(True)
        plt.show()

    def get_color(self, value, split=0):
        color = 'red'
        if value > split:
            color = 'green'
        return tc.colored(value, color)

