#coding=utf-8
# 此脚本实现从各种格式的遥感数据中读取数值，并按照要求存入数据库中
"""
---- author = "liang wu" ----
---- time = "20150616" ----
---- Email = "wl062345@gmail.com" ----
"""
import os, re
import csv, sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from pandas import *

def analysis():
    conn = sqlite3.connect("co_column.db")
    cur = conn.cursor()
    sql = "select * from co_total_column"
    rows = cur.execute(sql)

    year = []
    month = []
    co_CJ = []
    co_DXAL = []
    co_HH = []
    co_JJJ = []
    co_QZGY = []

    for row in rows:
        year.append(row[0])
        month.append(row[1])
        co_JJJ.append(row[2])
        co_HH.append(row[3])
        co_CJ.append(row[4])
        co_DXAL.append(row[5])
        co_QZGY.append(row[6])
    df = pandas.DataFrame(columns=['year', 'month', 'co_jjj', 'co_hh', 'co_dxal', 'co_qzgy', 'co_cj'])
    df['year'] =  Series(year)
    df['month'] =  Series(month)
    df['co_jjj'] =  Series(co_JJJ)
    df['co_hh'] =  Series(co_HH)
    df['co_dxal'] =  Series(co_DXAL)
    df['co_qzgy'] =  Series(co_QZGY)
    df['co_cj'] =  Series(co_CJ)

    df.to_csv('CO.csv', sep=',', encoding='utf-8', index=False)

def seasonAvr(csvName):
    df = pd.read_csv(csvName, sep=',',)
    df_01 = df[df['month']>=4]
    df_01 = df_01[df_01['month']<=6]

    print df_01.mean(axis=0)
    df_02 = df[df['month']>=7]
    df_02 = df_02[df_02['month']<=9]
    print df_02.mean(axis=0)

    df_03 = df[df['month']>=10]
    df_03 = df_03[df_03['month']<=12]
    print df_03.mean(axis=0)

    df_04 = df[df['month']>=1]
    df_04 = df_04[df_04['month']<=3]
    print df_04.mean(axis=0)

def yearAvr(csvName):
    df = pd.read_csv(csvName, sep=',',)
    csv_file = open('year'+csvName, 'a+')
    cwriter = csv.writer(csv_file, delimiter=',')
    for year, same_day_rows in df.groupby('year'):
        jjj = same_day_rows['co_jjj'].mean(axis=0)
        hh = same_day_rows['co_hh'].mean(axis=0)
        cj = same_day_rows['co_cj'].mean(axis=0)
        qzgy = same_day_rows['co_qzgy'].mean(axis=0)
        item = [year, jjj, hh, cj, qzgy]
        cwriter.writerow(item)

# analysis()
# seasonAvr("CO.csv")