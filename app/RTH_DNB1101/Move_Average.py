from statistics import mean
import pandas as pd


import numpy as np

# 生成模拟的1分钟内数据，例如每秒一个数据点，共60个数据点
np.random.seed(0)  # 为了可重复性设置随机种子
data = np.random.rand(60)  # 生成60个随机数模拟1分钟内的数据

# 设置窗口大小，例如5秒的移动平均
window_size = 5

# 计算移动平均
moving_averages = [np.mean(data[i:i+window_size]) for i in range(len(data) - window_size + 1)]

# 计算相邻移动平均值之间的差值
differences = [moving_averages[i] - moving_averages[i-1] for i in range(1, len(moving_averages))]

# 检查差值是否小于0.1，并记录满足条件的最后一项
recorded_values = [moving_averages[i-1] for i, diff in enumerate(differences) if diff < 0.1]

# 如果有满足条件的记录，取最后一项，否则为None
last_recorded_value = recorded_values[-1] if recorded_values else None

print(last_recorded_value)


'''data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
window_size = 3
moving_avg = data.rolling(window=window_size).mean()
print(moving_avg)

# 重新定义数据和窗口大小
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
window_size = 3

# 计算移动平均
moving_averages = [sum(data[i:i+window_size]) / window_size for i in range(len(data) - window_size + 1)]

# 计算移动平均序列中相邻数据的差值
differences = [moving_averages[i] - moving_averages[i-1] for i in range(1, len(moving_averages))]

print(moving_averages, differences)

 
    def moving_average(iterable, n=3):
    it = iter(iterable)
    series = list(islice(it, n))
    if len(series) == n:
        yield mean(series)  # First n-1 values will yield None
    for item in it:
        series.append(item)
        series.pop(0)
        yield mean(series)
 
# 使用移动平均算法的例子
data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
ma = moving_average(data, n=4)
 
for i, avg in enumerate(ma):
    if avg is not None:
        print(f"Moving average for the last {len(ma)-i} values: {avg}")'''