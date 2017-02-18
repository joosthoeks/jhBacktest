#!/usr/bin/env python

from jhbacktest.data import *
import jhbacktest.graph as jhgraph
import jhbacktest.stats as jhstats
from strategy_example import StrategyMy


def main():
    # set df:
    data = Data()
    df = data.csv2df('data/data.csv')

    # set slippage:
    slippage = 0

    # set best n:
    best_result = -1000000
    best_n = 0
    result_list = []
    n_list = []
    for n in range(2, 200):
        strat_exam = StrategyMy(
            df,
            n,
            slippage
        )
        strat_exam.run(False)

        result = jhstats.get_absolute(strat_exam.get_total_values_list())

        if result > best_result:
            best_result = result
            best_n = n

        result_list.append(result)
        n_list.append(n)

    print (('############################################################'))
    print best_result
    print best_n
    print (('############################################################'))

    # get analysis with best n:
    n = best_n
#    n = 4
    strat_exam = StrategyMy(
        df,
        n,
        slippage
    )
    strat_exam.run(True)
    print (('############################################################'))
    print (('best n: %s' % n))
    print (('slippage: %s' % slippage))
    print (('############################################################'))
    strat_exam.get_analysis()

    # equity curve:
    jhgraph.get_equity_curve(strat_exam.get_df()['datetime'], strat_exam.get_df()['Close'], strat_exam.get_equity_curve_list(), strat_exam.get_open_equity_curve_list())

    # optimization curve:
    jhgraph.get_optimization_curve(n_list, result_list)

    # benchmark vs result:
    jhgraph.get_benchmark_vs_result(strat_exam.get_df()['datetime'], strat_exam.get_benchmark_list(), strat_exam.get_equity_curve_list())


if __name__ == '__main__':
    main()

