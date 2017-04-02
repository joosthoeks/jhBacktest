import statistics


def get_hitrate(values_t, values_p):
    """
    Hitrate
    """
    if get_count(values_p) == 0:
        return 0
    return (float(get_count(values_p)) / get_count(values_t) * 100)

def get_profit_loss_ratio(mean_profit, mean_loss):
    """
    Profit/Loss Ratio
    """
    return mean_profit / (mean_loss * -1)

def get_expected_value(hitrate, mean_profit, mean_loss):
    """
    Expected Value
    """
    chance_profit = hitrate / 100
    chance_loss = 1 - chance_profit
    return (chance_profit * mean_profit) + (chance_loss * mean_loss)

def get_por_lucas_and_lebeau(hitrate, mean_profit, mean_loss):
    """
    Probability of Ruin (POR)
    Table of Lucas and LeBeau
    """
    hitrate_list = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    ratio_list = [.75, 1, 1.5, 2, 2.5, 3, 3.5, 4]
    matrix_list = []
    matrix_list.append([100, 100, 100, 100, 100, 98, 77, 15, 1, 0])
    matrix_list.append([100, 100, 100, 99, 92, 50, 7, 1, 0, 0])
    matrix_list.append([100, 99, 90, 50, 12, 2, 0, 0, 0, 0])
    matrix_list.append([97, 79, 35, 9, 1, 1, 0, 0, 0, 0])
    matrix_list.append([79, 38, 12, 4, 1, 0, 0, 0, 0, 0])
    matrix_list.append([50, 19, 6, 2, 1, 0, 0, 0, 0, 0])
    matrix_list.append([31, 12, 5, 2, 1, 0, 0, 0, 0, 0])
    matrix_list.append([21, 9, 4, 2, 1, 0, 0, 0, 0, 0])

    key_hitrate = min(range(len(hitrate_list)), key=lambda i: abs(hitrate_list[i] - hitrate))

    mean_loss *= -1
    ratio = mean_profit / mean_loss

    key_ratio = min(range(len(ratio_list)), key=lambda i: abs(ratio_list[i] - ratio))

    return matrix_list[key_ratio][key_hitrate]

def get_count(values_list):
    """
    Count
    """
    return len(values_list)

def get_absolute(values_list):
    """
    Absolute
    """
    return sum(values_list)

def get_min_absolute(values_list):
    """
    Minimal Absolute
    """
    if len(values_list) == 0:
        return 0
    return min(values_list)

def get_max_absolute(values_list):
    """
    Maximal Absolute
    """
    if len(values_list) == 0:
        return 0
    return max(values_list)

def get_mean_absolute(values_list):
    """
    Mean Absolute
    """
    return statistics.mean(values_list)

def get_median_absolute(values_list):
    """
    Median Absolute
    """
    return statistics.median(values_list)

def get_variance_absolute(values_list):
    """
    Variance Absolute
    """
    return statistics.variance(values_list)

def get_std_dev_absolute(values_list):
    """
    Standard Deviation Absolute
    """
    return statistics.stdev(values_list)

