#coding=utf-8
# 此脚本实现了从地面监测数据（txt格式）读取数据、存入数据库并可视化

"""
---- author = "liang wu" ----
---- time = "20150305" ----
---- Email = "wl062345@gmail.com" ----
"""

import sqlite3
import datetime
import numpy as np
from pandas import Series, DataFrame, Panel
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt

def getdatafrom_co_site():
    """
    从数据库中取出瓦里关地面监测站CO值序列
    :return:
    """
    conn = sqlite3.connect("co.db")
    cur = conn.cursor()
    sql = "select * from month_avr"
    rows = cur.execute(sql)

    timeseries = []
    co = []
    for row in rows:
        year = row[0]
        month = row[1]
        day = 1
        t = datetime.date(year, month, day)

        if row[2]>0 and year>=2000:
            timeseries.append(t)
            co.append(row[2])

    ts = Series(co,index=timeseries)
    conn.commit()
    return ts


def getdatafrom_co_column():
    """
    从数据库中取出卫星观测的CO浓度序列（北京和瓦里关）
    :return:
    """
    conn = sqlite3.connect("co_column.db")
    cur = conn.cursor()
    sql = "select * from co_total_column"
    rows = cur.execute(sql)

    timeseries = []
    co_wlg = []
    co_bj = []
    for row in rows:
        year = row[0]
        month = row[1]
        day = 1
        if row[2]!=0 and row[3]!=0:
            t = datetime.date(year, month, day)
            if year<=2013 and year >=2000:
                timeseries.append(t)
                co_wlg.append(row[2])
                co_bj.append(row[3])
    ts = Series(co_wlg,index=timeseries)
    conn.commit()
    return ts,co_wlg

def pear_self(co_list,co_column_list):
    """
    计算两个序列的相关系数
    :param co_list: 地面站CO监测数据序列
    :param co_column_list: 卫星观测的CO浓度序列
    :return:
    """
    mean_co = np.mean(co_list)
    dif_co = co_list - mean_co
    std_co = np.std(co_list)
    mean_column = np.mean(co_column_list)
    dif_column = co_column_list - mean_column
    std_column = np.mean(co_column_list)
    i=0
    total=0
    while i <len(co_list):
        total = total+dif_column[i]*dif_co[i]
        i = i+1
    Expectation = total/len(co_list)
    PPMCC = Expectation/(std_co*std_column)


if __name__ == "__main__":
    co_site = getdatafrom_co_site()                        # 从数据库中获取地面站CO监测数据序列
    co_column,co_column_list = getdatafrom_co_column()     # 从数据库中获取卫星观测的CO浓度序列
    new_co_site = []
    co_list = []
    for index in co_column.index:
        co_list.append(co_site[index])
    new_co_site = Series(co_list,index=co_column.index)    # 匹配地面站CO监测值和卫星观测值

    mean_co = np.mean(co_list)                   # 计算地面站CO监测值序列平均值
    dif_co = co_list - mean_co                   # 计算地面站CO监测值与平均值差值
    std_co = np.std(co_list)                     # 计算地面站CO监测值方差
    mean_column = np.mean(co_column_list)        # 计算卫星CO浓度序列平均值
    dif_column = co_column_list - mean_column    # 计算卫星CO浓度与平均值差值
    std_column = np.std(co_column_list)          # 计算卫星CO浓度方差
    a = dif_co/std_co
    b = dif_column/std_column
    ts_a = Series(a,index=co_column.index)       # 获得地面站CO监测值时间序列
    ts_b = Series(b,index=co_column.index)       # 获得卫星CO浓度时间序列

    plt.figure(num=None,figsize=(16,4))
    ts_a.plot()
    ts_b.plot()
    plt.savefig("coTimeseries.png")              # 画出两个时间序列并保存图像
    plt.show()

    person = pearsonr(co_list,co_column_list)    # 计算两个序列的皮尔逊相关系数，考察两个数据的相关性
    print person

















