

# Import Built-Ins:
from pprint import pprint as pp

# Import Third-Party:
import jhtalib as jhta

# Import Homebrew:
from backtest_example import BacktestExample


def main():
    df = jhta.CSV2DF('data/data.csv')
#    pp (df)

    # set best n:
    best_result = -1000000
    best_n = 0
    result_list = []
    n_list = []
    for n in range(2, 200):
        backtest_example = BacktestExample(df, n)
        backtest_example.run()

        result = sum(backtest_example.get_trades_total())

        if result > best_result:
            best_result = result
            best_n = n

        result_list.append(result)
        n_list.append(n)

    pp ('############################################################')
    pp (best_result)
    pp (best_n)
    pp ('############################################################')

    # get analysis with best n:
    n = best_n
#    n = 4
    pp ('############################################################')
    pp ('best n: {}'.format(n))
    pp ('best result: {}'.format(best_result))
    pp ('############################################################')

    backtest_example = BacktestExample(df, n)
    backtest_example.run()
    backtest_example.save('data/tmp.csv')
    backtest_example.print_result()
    backtest_example.plot_optimization_curve(n_list, result_list)
    backtest_example.plot_benchmark_vs_result('%Y%m%d')

if __name__ == '__main__':
    main()
