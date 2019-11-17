# %%
# 绘图
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame


# %%
# format transforma
def transfor(data):
    tube = []
    for col in data.columns:
        try:
            cols = data[col].to_list()
            tube.append(cols)
        finally:
            a = 1
    tube = tuple(tube)
    return tube
        
# make the length similar


def flat(*data):
    if len(data) == 2:
        a = np.array(data[0])
        b = np.array(data[1])
        diff = len(a) - len(b)
        if diff < 0:
            b = b[0:diff]
        else:
            a = a[0:len(b)]
        return a, b
    elif len(data) == 3:
        a = np.array(data[0])
        b = np.array(data[1])
        c = np.array(data[2])
        theminimum = min(len(a), len(b), len(c))
        a = a[0:theminimum]
        b = b[0:theminimum]
        c = c[0:theminimum]
        return a, b, c



def plot(*data, d2='line', d3='scatter'):
    # 2d
    if len(data) != 3:

        if len(data) == 1:
            a = np.arange(1, len(data[0])+1)
            if isinstance(data[0], DataFrame):
                
                b = transfor(data[0])
            else:
                b = data[0]
        if len(data) == 2:
            a = np.array(data[0])
            b = np.array(data[1])
            if len(data[0]) != len(data[1]):
                diff = len(a) - len(b)
                if diff < 0:
                    b = b[0:diff]
                else:
                    a = a[0:len(b)]
                print('数组有切尾长度：', abs(diff))
        if isinstance(b, tuple):
            plt.rcParams['figure.figsize'] = (8.0, 4.0)
            plt.rcParams['figure.dpi'] = 300
            for col in b:
                plt.plot(a, col)
        else:

            plt.plot(a, b)

    # 3d
    if len(data) == 3:
        from mpl_toolkits.mplot3d import Axes3D
        a, b, c = data
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        fig = plt.figure()
        axes3d = Axes3D(fig)
        if d3 == 'scatter':
            axes3d.scatter(a, b, c)
        elif d3 == 'line':
            axes3d.plot(a, b, c)
        elif d3 == 'surface':
            axes3d.plot_surface(a, b, c)




# %%
