#coding=utf-8
# 此脚本实现了CO地面监测数据功率谱分析，并分析了周期

"""
---- author = "liang wu" ----
---- time = "20150305" ----
---- Email = "wl062345@gmail.com" ----
"""

from __future__ import division
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from matplotlib import mlab
import pywt
from pandas import Series, DataFrame, Panel
import wavelets

def plot_powerspectrum():
    conn = sqlite3.connect("co.db")
    cur = conn.cursor()
    sql = "select * from month_avr where YEAR>=1998"
    rows = cur.execute(sql)
    timeseries = []
    co = []
    point = []
    for row in rows:
        year = row[0]
        month = row[1]
        day = 1
        #print year,month
        t = datetime.date(year, month, day)
        timeseries.append(t)
        point.append((year-1998)*12+month)
        co.append(row[2])
    ts = Series(co,index=timeseries)
    # 先从数据库中取出时间序列
    mean_co = np.mean(co)
    dif_co = co - mean_co
    std_co = np.std(co)
    a = dif_co/std_co
    data = np.array(a)
    dt = np.array(data)
    N = len(data)                               # 标准化数据
    df = 1. / (N * dt)
    PSD = np.abs(fftpack.fft(data))**2          # 计算功率谱
    freqs = fftpack.fftfreq(data.size,d = 1)    # 计算对应的频率值
    periods = 1 / freqs
    idx = np.argsort(freqs)                     # 计算索引值

    plt.subplot(2,1,1)
    plt.plot(dt,data)
    plt.xlabel('Time (month)')
    plt.subplot(2,1,2)
    plt.plot(freqs[idx],PSD[idx])
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.show()
    plt.savefig("powerspectrum.png")

    conn.commit()


if __name__ == '__main__':
    plot_powerspectrum()