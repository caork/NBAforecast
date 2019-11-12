# %%
# 绘图
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from mpl_toolkits.mplot3d import Axes3D




# %%
def plot(*data,d2 = 'line',d3 = 'scatter'):
    if len(data) == 1:
        x_values = np.arange(1, len(data[0])+1)
        plt.plot(x_values, data[0])
    if len(data) == 2:
        if len(data[0]) == len(data[1]):
            plt.plot(data[0], data[1])
        else:
            a = np.array(data[0])
            b = np.array(data[1])
            diff = len(a) - len(b)
            if diff < 0:
                b = b[0:diff]
            else:
                a = a[0:len(b)]
            plt.plot(a, b)
            print('数组有切尾长度：', abs(diff))
    if len(data) == 3:  
        from mpl_toolkits.mplot3d import Axes3D
        a,b,c = data
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        fig = plt.figure()
        axes3d = Axes3D(fig)
        if d3 == 'scatter':
            axes3d.scatter(a,b,c)
        elif d3 == 'line':
            axes3d.plot(a,b,c)
        elif d3 == 'surface':
            axes3d.plot_surface(a,b,c)


# %%
