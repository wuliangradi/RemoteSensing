#coding=utf-8
# 此脚本实现了火点数据并进行栅格化
"""
---- author = "liang wu" ----
---- time = "20150705" ----
---- Email = "wl062345@gmail.com" ----
"""
import pandas as pd
import csv
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import cm
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import sqlite3

con = sqlite3.connect("finn2013.db")
cur = con.cursor()
cur.execute("create table if not EXISTS FINN(DAY int, LAT float, LON float, CO2 float, CO float, NO1 float, NO2 float, SO2 float, PM10 float, PM25 float)")


def txt2csv(txt_name):
    csv_file = open(txt_name[:-4]+'.csv', 'w')
    cwriter = csv.writer(csv_file, delimiter=',')
    with open(txt_name) as fp:
        for line in fp.readlines():
            li = line.split(',')
            li = map(lambda s: s.strip(), li)
            lenth = len(li)
            if lenth>=43:
            #for i in range(3,46):
            #    try:
            #        li[i] = float(li[i][:-4])*(10**int(float(li[i][-1])))
            #    except ValueError,e:
            #        print "error",e,"on low",i,"on line",line
                item = [li[0], li[3], li[4], li[6], li[7], li[9], li[10], li[11], li[43], li[40]]
                cwriter.writerow(item)

def splitCsv(csv_name):
    df = pd.read_csv(csv_name, sep=',', index_col=False)
    df = df[df['DAY']>=213]
    dfTemp = df[df['DAY']<=243]
    outName = 'month/'+str(8) + '.csv'
    dfTemp.to_csv(outName, sep=',', index=False)

    #for day in range(1,266):
    #    print "第  %d  天"%day
    #    dfTemp = df[df['DAY'] == day]
    #    outName = 'day/'+str(day) + '.csv'
    #    dfTemp.to_csv(outName, sep=',', index=False)

def txt2sqlite(txt_name):
    with open(txt_name) as fp:
        for line in fp.readlines():
            li = line.split(',')
            li = map(lambda s: s.strip(), li)
            lenth = len(li)
            if lenth>=47:
                try:
                    item = [li[0], li[3], li[4], li[6], li[7], li[9], li[10], li[11], li[43], li[40]]
                    cur.execute("INSERT INTO FINN VALUES(?,?,?,?,?,?,?,?,?,?)",item)      #将item的值插入已经建好的数据库的表中
                except ValueError,e:
                    print "error",e,"on line",line

def stere(data,latitude,longitude):
    ax = plt.gca()
    m = Basemap(width=10000000,height=7500000,
            resolution='l',projection='stere',\
            lat_ts=35,lat_0=35,lon_0=107.)

    m.drawcoastlines()
    m.drawcountries()
    m.drawparallels(np.arange(-80.,81.,20.),labels=[1,0,0,0])#画平行的纬度,前一个参数是表示起点，终点，间距的序列，后一个参数是指在哪一个方向显示纬度、经度值
    m.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1])#画平行的经度

    sc = m.scatter(longitude, latitude, c=data, s=1, cmap=plt.cm.jet,
                   edgecolors=None, linewidth=0)
    #im = m.pcolormesh(longitude,latitude,data,shading='flat',cmap=plt.cm.jet,latlon=True)
    plt.show()

def plotMap(data,latitude,longitude):
    m = Basemap(projection='cyl', resolution='l',
                llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180)
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90, 91, 45))
    m.drawmeridians(np.arange(-180, 180, 45), labels=[True,False,False,True])
    sc = m.scatter(longitude, latitude, c=data, s=1, cmap=plt.cm.jet,
                   edgecolors=None, linewidth=0)
    cb = m.colorbar()
    fig = plt.gcf()
    plt.show()

def main():
    start = dt.datetime.now()
    #splitCsv("GLOBAL_FINNv15_2013_MOZ4_7112014.csv")
    df = pd.read_csv("month/3.csv", sep=',', index_col=False)
    count = 0
    for (la, lon), group in df.groupby(['LATI', 'LONGI']):
        print group.shape
        print "+++++++++++"
    print df.shape
    end = dt.datetime.now()
    print "程序运行时间：%d"%(end-start).seconds
    # txt_name = "GLOBAL_FINNv15_2013_MOZ4_7112014.txt"
    # txt2csv(txt_name)
    #txt2sqlite(txt_name)
    #cur.close()
    #con.commit()
    #df = pd.read_csv("GLOBAL_FINNv15_2013_MOZ4_7112014.csv", sep=',', index_col=False)
    #print df.shape
    #df.to_csv('my.txt',sep=',')
    #array = df.values
    #print type(array[0,3])
    # latitude = array[:,3]
    # longtude = array[:,4]
    # coValue = array[:,7]
    # plotMap(coValue, latitude, longtude)
    # stere(coValue, latitude, longtude)
    # plt.show()

main()