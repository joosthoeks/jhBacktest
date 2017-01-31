from datetime import datetime as dt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot


def get_equity_curve(x_list, y1_list, y2_list, y3_list):
    host = host_subplot(111, axes_class=AA.Axes)
    par1 = host.twinx()
    par2 = host.twinx()

    par1.axis['right'] = par1.get_grid_helper().new_fixed_axis(loc='right', axes=par1, offset=(0, 0))
    par2.axis['right'] = par2.get_grid_helper().new_fixed_axis(loc='right', axes=par2, offset=(60, 0))
    
#    par2.axis['right'].toggle(all=True)

    host.set_ylabel('Price')
    par1.set_ylabel('Equity Curve')
    par2.set_ylabel('Open Equity Curve')

    x = [dt.strptime(d, '%Y%m%d').date() for d in x_list]

    p1, = host.plot(x, y1_list, color='b')
    p2, = par1.plot(x, y2_list, color='g')
    p3, = par2.plot(x, y3_list, color='r')

    par1.set_ylim(-40, 400)
    par2.set_ylim(-40, 400)

    host.axis['left'].label.set_color(p1.get_color())
    par1.axis['right'].label.set_color(p2.get_color())
    par2.axis['right'].label.set_color(p3.get_color())

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()

    plt.title('Symbol')
    plt.grid(True)
    plt.draw()
    plt.show()

def get_optimization_curve(x_list, y_list):
    x = x_list
    y = y_list

    plt.plot(x, y)

    plt.xlabel('Period')
    plt.ylabel('Result')

    plt.title('Optimization Curve')
    plt.grid(True)
    plt.draw()
    plt.show()

def get_benchmark_vs_result(x_list, y1_list, y2_list):
    x = [dt.strptime(d, '%Y%m%d').date() for d in x_list]

    plt.gca().set_color_cycle(['blue', 'green'])

    plt.plot(x, y1_list)
    plt.plot(x, y2_list)
    
    plt.legend(['Benchmark', 'Result'], loc='upper left')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()

    plt.title('Benchmark vs Result')
    plt.grid(True)
    plt.draw()
    plt.show()


