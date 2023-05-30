from os import path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
import myconfig
import requests


def interp1d(kind, start, end, num, x_colName, y_colName, fileName):
    input_path = path.join(requests.request("GET", "http://127.0.0.1:1234/syspath").text, myconfig.input_path,
                           fileName)
    # 读取数据
    df = pd.read_excel(input_path)
    x = np.array(df.loc[:, x_colName])

    x_new = np.linspace(start, end, num)
    data = {x_colName: x_new}

    # 把新的数据都存起来
    y_raw_list = []
    y_new_list = []

    for col in y_colName:
        y = np.array(df.loc[:, col])
        y_raw_list.append(y)

        fit = interpolate.interp1d(x, y, kind=kind)

        y_new = fit(x_new)
        y_new_list.append(y_new)
        # 添加数据
        temp_dict = {col: y_new}
        data.update(**temp_dict)

    out_path = plotResult(x=x, y=y_raw_list, x_new=x_new, y_news=y_new_list, colNames=y_colName,fileName=fileName)

    # print("最终结果", data)
    return pd.DataFrame(data, index=None),out_path


def plotResult(x, y, x_new, y_news, colNames, fileName):
    plt.figure()

    # 画上面一半
    plt.subplot(211)
    # 这里有一个坑，我们的数据结构是外面一层list[里面是np.array对象]，不要当做矩阵来取数据
    for i in range(len(colNames)):
        plt.scatter(x, y[i])
        plt.plot(x, y[i], label=f"{colNames[i]}")
    plt.grid()
    plt.legend()

    # 画上面一半
    plt.subplot(212)
    for i in range(len(colNames)):
        plt.plot(x_new, y_news[i], label=f"{colNames[i]}_new",linestyle='--')
        plt.scatter(x_new, y_news[i])
        plt.plot(x, y[i], label=f"{colNames[i]}")

    plt.legend()
    plt.grid()

    out_path = path.join(requests.request("GET", "http://127.0.0.1:1234/syspath").text, myconfig.output_path,
                         fileName.replace("xlsx", "png").replace("xls", "png"))

    print("结果保存在", out_path)
    plt.savefig(out_path)
    # plt.show()
    return out_path


