#coding=utf-8
# 此脚本实现了从数据库中取出数据时间序列可视化的过程
"""
---- author = "liang wu" ----
---- time = "20150520" ----
---- Email = "wl062345@gmail.com" ----
"""

import sqlite3
import datetime
import numpy as np
from pandas import Series, DataFrame, Panel
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math


def getdatafrom_fire():
    coon = sqlite3.connect("NO2.db")
    cur = coon.cursor()
    sql = "select * from NO2"
    rows = cur.execute(sql)

    timeseries = []
    count = []
    for row in rows:
        year = row[0]
        month = row[1]
        day = 1
        t = datetime.date(year, month, day)

        if row[2]>=0:
            timeseries.append(t)
            count.append(row[2])

    ts = Series(count, index=timeseries)
    coon.commit()
    return timeseries, count

def getdatafrom_co():
    coon = sqlite3.connect("华东/co_column.db")
    cur = coon.cursor()
    sql = "select * from co_total_column"
    rows = cur.execute(sql)

    timeseries = []
    co_column = []
    for row in rows:
        year = row[0]
        month = row[1]
        day = 1
        t = datetime.date(year, month, day)

        if row[2]>=0:
            timeseries.append(t)
            co_column.append(row[2])

    ts = Series(co_column, index=timeseries)
    coon.commit()
    return timeseries, co_column

def getdatafrom_no2():
    coon = sqlite3.connect("NO2.db")
    cur = coon.cursor()
    sql = "select * from NO2"
    rows = cur.execute(sql)

    timeseries = []
    co_column = []
    for row in rows:
        year = row[1]
        month = row[2]
        day = 1
        t = datetime.date(year, month, day)

        if row[2]>=0:
            timeseries.append(t)
            co_column.append(row[0])

    ts = Series(co_column, index=timeseries)
    coon.commit()
    return timeseries, co_column

def getdatafrom_AOD():
    coon = sqlite3.connect("MODIS_AOD.db")
    cur = coon.cursor()
    sql = "select * from AOD"
    rows = cur.execute(sql)

    timeseries = []
    co_column = []
    for row in rows:
        year = row[0]
        month = row[1]
        day = 1
        t = datetime.date(year, month, day)
        if row[2]>=0:
            timeseries.append(t)
            co_column.append(row[2])

    ts = Series(co_column, index=timeseries)
    coon.commit()
    return timeseries, co_column


def make_format(current, other):
    def format_coord(x, y):
        display_coord = current.transData.transform((x,y))
        inv = other.transData.inverted()
        ax_coord = inv.transform(display_coord)
        coords = [ax_coord, (x, y)]
        return ('Left: {:<40}    Right: {:<}'
                .format(*['({:.3f}, {:.3f})'.format(x, y) for x,y in coords]))
    return format_coord

#[time1, count] = getdatafrom_fire()
[time2, co] = getdatafrom_co()
#time1 = np.array(time1)
#count = np.array(count)
time2 = np.array(time2)
co = np.array(co)


[time3, AOD] = getdatafrom_AOD()
time3 = np.array(time3)
AOD = np.array(AOD)
#ts = Series(AOD, time)
#ts.plot()

"""
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax2.format_coord = make_format(ax2, ax1)
ax1.plot(time3, AOD, 'r-s', label='y1')
ax2.plot(time2, co, 'g-^', label='y2')

#plt.savefig("华东区域.png")              # 画出两个时间序列并保存图像
"""

fig = plt.figure(figsize=(18,5))
ax1 = fig.add_subplot(111)

rect = fig.patch
rect.set_facecolor('white')

ax1.set_xlabel("DATE", color='black', fontsize='14')
plot1, = ax1.plot(time3, AOD, marker='s', linestyle='-', color='r', label='AOD', alpha=0.8)
#ax1.set_xticklabels()

ax1.set_ylabel("AOD", color='black', fontsize='14')
for tl in ax1.get_yticklabels():
    tl.set_color('r')
    tl.set_fontsize(14)

for tl in ax1.get_xticklabels():
    tl.set_color('black')
    tl.set_rotation(45)
    tl.set_fontsize(16)
# plt.legend()

ax2 = ax1.twinx()
plot2, = ax2.plot(time2, co, marker='^', linestyle='--', color='g', label='CO', alpha=0.8)
ax2.set_ylabel("CO(ppbv)", color='black', fontsize='14')
for tl in ax2.get_yticklabels():
    tl.set_color('g')
    tl.set_fontsize(14)

#ax2.grid(True, color='grey', linestyle='--', linewidth=2, alpha=0.8)

# plt.title("")
# plt.legend()

fig.legend([plot1, plot2], ['AOD', 'CO'], loc=2)
#fig.tight_layout() # http://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
plt.show()





