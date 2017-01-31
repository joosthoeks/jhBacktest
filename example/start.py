#!/usr/bin/env python

from jhbacktest.data import *
import jhbacktest.graph as jhgraph
import jhbacktest.stats as jhstats
from strategy_example import StrategyMy

from datetime import datetime as dt
import time


def main():
    # set slippage:
    slippage = 0

    # get data:
    data = Data()
#    bars = data.get_data_csv('data/data-EOE-IND-FTA-EUR-1Y-1day-2010.csv')
#    bars = data.get_data_csv('data/data-EOE-IND-FTA-EUR-1Y-1day-2011.csv')
#    bars = data.get_data_csv('data/data-EOE-IND-FTA-EUR-1Y-1day-2012.csv')
#    bars = data.get_data_csv('data/data-EOE-IND-FTA-EUR-1Y-1day-2013.csv')
#    bars = data.get_data_csv('data/data-EOE-IND-FTA-EUR-1Y-1day-2014.csv')
    bars = data.get_data_csv('data/data-EOE-IND-FTA-EUR-1Y-1day-2015.csv')
#    bars = data.get_data_csv('data/data-EOE-IND-FTA-EUR-5Y-1day-2015.csv')

    # only for yahoo:
#    data = Data()
#    ts = int(time.time())
#    ts_start = ts - (60*60*24*365.25*1)
#    ts_end = ts - (60*60*24*0)
#    date_start = dt.fromtimestamp(ts_start).strftime('%Y-%m-%d')
#    date_end = dt.fromtimestamp(ts_end).strftime('%Y-%m-%d')
#    bars = data.get_data_yahoo(date_start, date_end, '^AEX')

    # only for IbPy:
#    ts = int(time.time())
#    ts_end = ts - (60*60*24*0)  # current day
#    end_date_time = dt.fromtimestamp(ts_end).strftime('%Y%m%d %H:%M:%S UTC')
#    data.set_contract_ib('EOE', 'IND', 'FTA', 'EUR', 200, '201510')
#    bars = data.get_data_ib(1, end_date_time, '1 Y', '1 day', 'TRADES', 0, 1)
#    bars = data.get_data_ib(1, end_date_time, '1 M', '1 day', 'TRADES', 0, 1)
#    bars = data.get_data_ib(1, end_date_time, '2 D', '5 mins', 'TRADES', 0, 1)
#    bars = data.get_data_ib(1, end_date_time, '3600 S', '5 mins', 'TRADES', 0, 1)

    # get best timeperiod:
    best_result = -1000000
    best_timeperiod = 0
    result_list = []
    timeperiod_list = []
    for timeperiod in range(2, 200):
        strat_exam = StrategyMy(
            bars,
            timeperiod,
            slippage
        )
        strat_exam.run(False)

        result = jhstats.get_absolute(strat_exam.get_total_values_list())

        if result > best_result:
            best_result = result
            best_timeperiod = timeperiod

        result_list.append(result)
        timeperiod_list.append(timeperiod)

    print (('############################################################'))
    print best_result
    print best_timeperiod
    print (('############################################################'))

    # get analysis with best timeperiod:
    timeperiod = best_timeperiod
    strat_exam = StrategyMy(
        bars,
        timeperiod,
        slippage
    )
    strat_exam.run(True)
    print (('############################################################'))
    print (('best timeperiod: %s' % timeperiod))
    print (('slippage: %s' % slippage))
    print (('############################################################'))
    strat_exam.get_analysis()

    # equity curve:
    jhgraph.get_equity_curve(strat_exam.get_bars_pd('datetime'), strat_exam.get_bars_pd('Close'), strat_exam.get_equity_curve_list(), strat_exam.get_open_equity_curve_list())

    # optimization curve:
    jhgraph.get_optimization_curve(timeperiod_list, result_list)

    # benchmark vs result:
    jhgraph.get_benchmark_vs_result(strat_exam.get_bars_pd('datetime'), strat_exam.get_benchmark_list(), strat_exam.get_equity_curve_list())


if __name__ == '__main__':
    main()

