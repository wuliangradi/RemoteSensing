#coding=utf-8
# 此脚本实现从各种格式的遥感数据中读取数值，并按照要求存入数据库中
"""
---- author = "liang wu" ----
---- time = "20150616" ----
---- Email = "wl062345@gmail.com" ----
"""
import os
import re
import h5py
import gdal
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

def draw_screen_poly( lats, lons, m ):
    '''
    画矩形
    '''
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, 'red', facecolor='None', edgecolor='red', linewidth=2, alpha=1 )
    plt.gca().add_patch(poly)

def ResearchRegion():
    '''
    在地图上画出研究区域
    '''
    lats_01 = [ 38, 41, 41, 38 ]
    lons_01 = [ 115, 115, 119, 119 ]
    lats_02 = [ 33, 36, 36, 33 ]
    lons_02 = [ 113, 113, 119, 119 ]
    lats_03 = [ 30, 33, 33, 30 ]
    lons_03 = [ 118, 118, 122, 122 ]
    lats_04 = [ 50, 53, 53, 50 ]
    lons_04 = [ 120, 120, 126, 126 ]
    lats_05 = [ 30, 35, 35, 30 ]
    lons_05 = [ 87, 87, 94, 94 ]

    fig = plt.figure()
    rect = fig.patch
    rect.set_facecolor('grey')
    m = Basemap(llcrnrlon=70, llcrnrlat=5, urcrnrlon=135, urcrnrlat=55, projection='mill', resolution='h')
    m.bluemarble()
    m.drawparallels(np.arange(5.,90.,10.),labels=[1,1,0,0])
    m.drawmeridians(np.arange(80.,181.,10.),labels=[0,0,1,1])
    m.readshapefile("shp/CHINA", 'CHINA', drawbounds=1, color='black')
    x1, y1 = m(110, 41)
    x2, y2 = m(105, 34)
    x3, y3 = m(122.5, 30)
    x4, y4 = m(119, 48.5)
    x5, y5 = m(80, 32)
    draw_screen_poly( lats_01, lons_01, m )
    plt.annotate(u'京津冀', xy=(x1, y1), color = 'r')
    draw_screen_poly( lats_02, lons_02, m )
    plt.annotate(u'淮河流域', xy=(x2, y2), color = 'r')
    draw_screen_poly( lats_03, lons_03, m )
    plt.annotate(u'长江下游流域', xy=(x3, y3), color = 'r')
    draw_screen_poly( lats_04, lons_04, m )
    plt.annotate(u'大兴安岭地区', xy=(x4, y4), color = 'r')
    draw_screen_poly( lats_05, lons_05, m )
    plt.annotate(u'青藏高原', xy=(x5, y5), color = 'r')
    plt.show()


def GetAverage(data, laMax, laMin, loMin, loMax):
    '''
    求解矩阵平均值，需要处理矩阵中的异常值
    '''
    count = 0
    sum = 0
    co_avr = 0
    for i in range(laMin, laMax+1):
        for j in range(loMin, loMax+1):
            count = count + 1
            if (data[i][j] == -999):
                data[i][j] = 0
                count = count - 1
            a = data[i][j].item()
            sum = sum + a

    if count == 0:
        co_avr = 0
    else:
        co_avr = sum/count
    return co_avr


def run(hdf_file, file_name, cur):

    with h5py.File(hdf_file, mode='r') as f:

        group = f['/HDFEOS/GRIDS/MOP03/Data Fields']     # 读取CO浓度所在的数据域
        dsname = 'RetrievedCOTotalColumnDay'             # 要读取的数据区名称，这里指“白天反演的总CO柱浓度”
        data = group[dsname][:].T                        # 读取CO浓度矩阵
        fillvalue = group[dsname].attrs['_FillValue']
        data[data == fillvalue] = np.nan                 # 获得数据中值缺失的部分
        data = np.ma.masked_array(data, np.isnan(data))  # 对值缺失部分作掩膜处理

        y = f['/HDFEOS/GRIDS/MOP03/Data Fields/Latitude'][:]    # 获取数据的纬度
        x = f['/HDFEOS/GRIDS/MOP03/Data Fields/Longitude'][:]   # 获取数据的经度
        longitude, latitude = np.meshgrid(x, y)                 # 并将经纬度转换成格网

        laMin01 = int(round(38-latitude.min()))
        laMax01 = int(round(41-latitude.min()))
        loMin01 = int(round(115-longitude.min()))
        loMax01 = int(round(119-longitude.min()))

        laMin02 = int(round(33-latitude.min()))
        laMax02 = int(round(36-latitude.min()))
        loMin02 = int(round(113-longitude.min()))
        loMax02 = int(round(119-longitude.min()))

        laMin03 = int(round(30-latitude.min()))
        laMax03 = int(round(33-latitude.min()))
        loMin03 = int(round(118-longitude.min()))
        loMax03 = int(round(122-longitude.min()))

        laMin04 = int(round(50-latitude.min()))
        laMax04 = int(round(53-latitude.min()))
        loMin04 = int(round(120-longitude.min()))
        loMax04 = int(round(126-longitude.min()))

        laMin05 = int(round(30-latitude.min()))
        laMax05 = int(round(35-latitude.min()))
        loMin05 = int(round(87-longitude.min()))
        loMax05 = int(round(94-longitude.min()))

        print laMin01, laMax01, loMin01, loMax01
        year = int(hdf_file[-20:-16])
        month = int(hdf_file[-16:-14])             # 获取HDF文件路径中的”年、月“等时间信息

        avr_01 = GetAverage(data, laMin01, laMax01, loMin01, loMax01)
        avr_02 = GetAverage(data, laMin02, laMax02, loMin02, loMax02)
        avr_03 = GetAverage(data, laMin03, laMax03, loMin03, loMax03)
        avr_04 = GetAverage(data, laMin04, laMax04, loMin04, loMax04)
        avr_05 = GetAverage(data, laMin05, laMax05, loMin05, loMax05)

        # plt.imshow(data)
        # plt.show()
        item = [year, month, avr_01, avr_02, avr_03, avr_04, avr_05]
        cur.execute("INSERT INTO co_total_column VALUES(?,?,?,?,?,?,?)",item)

def hdf2tif(i, cur):
    """
    在本地，共有16个文件夹分别存储2000-2015年的影像，需要按年份遍历每个文件夹内的影像（每年12景影像）
    :param i: 年份
    :return:
    """
    print "the num of year: %d"%i
    year = str(i)
    folder = '/Users/wuliang/Documents/数据/卫星数据/CO/MOPITT/'+os.sep+year    # 文件夹路径

    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)>15:
                hdf_file = folder+os.sep+name
                # 得到单个HDF文件的路径
                try:
                    hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
                except KeyError:
                    pass
                print hdf_file
                run(hdf_file, name, cur)

def ExtractCO():
    '''
    提取一氧化碳数据
    '''
    coon = sqlite3.connect("co_column.db")
    cur = coon.cursor()
    cur.execute("create table if not EXISTS co_total_column(year int, month int, co_avr_JJJ float,"
                "co_avr_HH float, co_avr_CJ float, co_avr_DXAL float, co_avr_QZGY float)")
    i = 2000
    while i<=2015:
        hdf2tif(i, cur)
        i = i+1
    coon.commit()
    coon.close()

def tiff2sqlite(filename, year, month, cur):
    '''
    读取tiff数据并将感兴趣区域存入数据库中
    '''
    tiff = filename
    ds = gdal.Open(tiff)
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray()
    gt = ds.GetGeoTransform()

    laMin01 = int(round(38-gt[3])*(1/gt[5]))
    laMax01 = int(round(41-gt[3])*(1/gt[5]))
    loMin01 = int(round(115-gt[0])*(1/gt[1]))
    loMax01 = int(round(119-gt[0])*(1/gt[1]))

    laMin02 = int(round(33-gt[3])*(1/gt[5]))
    laMax02 = int(round(36-gt[3])*(1/gt[5]))
    loMin02 = int(round(116-gt[0])*(1/gt[1]))
    loMax02 = int(round(119-gt[0])*(1/gt[1]))

    laMin03 = int(round(30-gt[3])*(1/gt[5]))
    laMax03 = int(round(33-gt[3])*(1/gt[5]))
    loMin03 = int(round(118-gt[0])*(1/gt[1]))
    loMax03 = int(round(122-gt[0])*(1/gt[1]))

    laMin04 = int(round(50-gt[3])*(1/gt[5]))
    laMax04 = int(round(53-gt[3])*(1/gt[5]))
    loMin04 = int(round(120-gt[0])*(1/gt[1]))
    loMax04 = int(round(126-gt[0])*(1/gt[1]))

    laMin05 = int(round(30-gt[3])*(1/gt[5]))
    laMax05 = int(round(35-gt[3])*(1/gt[5]))
    loMin05 = int(round(87-gt[0])*(1/gt[1]))
    loMax05 = int(round(94-gt[0])*(1/gt[1]))
    '''
    mean01 = np.mean(data[laMax01:laMin01, loMin01:loMax01])
    mean02 = np.mean(data[laMax02:laMin02, loMin02:loMax02])
    mean03 = np.mean(data[laMax03:laMin03, loMin03:loMax03])
    mean04 = np.mean(data[laMax04:laMin04, loMin04:loMax04])
    mean05 = np.mean(data[laMax05:laMin05, loMin05:loMax05])
    '''
    avr_01 = GetAverage(data, laMin01, laMax01, loMin01, loMax01)
    avr_02 = GetAverage(data, laMin02, laMax02, loMin02, loMax02)
    avr_03 = GetAverage(data, laMin03, laMax03, loMin03, loMax03)
    avr_04 = GetAverage(data, laMin04, laMax04, loMin04, loMax04)
    avr_05 = GetAverage(data, laMin05, laMax05, loMin05, loMax05)

    year = int(float(year))
    month = int(float(month))
    item = [year, month, avr_01, avr_02, avr_03, avr_04, avr_05]
    cur.execute("INSERT INTO NO2 VALUES(?,?,?,?,?,?,?)",item)

def ExtractAOD():
    '''
    提取感兴趣区域AOD
    :return:
    '''
    conn = sqlite3.connect('MODIS_AOD.db')
    cur = conn.cursor()
    sql = "create table if NOT EXISTS AOD(year int, month int, AOD_avr_JJJ float, " \
          "AOD_avr_HH float, AOD_avr_CJ float, AOD_avr_DXAL float, AOD_avr_QZGY float)"
    cur.execute(sql)

    folder = '/Users/wuliang/Documents/数据/卫星数据/AOD/MONTH_0.1'
    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)>9:
                fire_name = folder+os.sep+name
                year = name[-28:-24]
                month = name[-23:-21]
                print fire_name
                tiff2sqlite(fire_name, year, month, cur)
    conn.commit()
    conn.close()

def ExtractNO2():
    '''
    提取感兴趣区域NO2
    :return:
    '''
    conn = sqlite3.connect('NO2.db')
    cur = conn.cursor()
    sql = "create table if NOT EXISTS NO2(year int, month int, NO2_avr_JJJ float, " \
          "NO2_avr_HH float, NO2_avr_CJ float, NO2_avr_DXAL float, NO2_avr_QZGY float)"
    cur.execute(sql)

    folder = '/Users/wuliang/Documents/数据/卫星数据/NO2/NO2_TIFF'    # 文件夹路径
    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)>9:
                fire_name = folder+os.sep+name
                year = name[-10:-6]
                month = name[-6:-4]
                tiff2sqlite(fire_name, year, month, cur)
    conn.commit()


def csv2sqlite(fire_name, year, month, cur):
    '''
    将csv文件导入sqlite数据库中
    :param fire_name:
    :param year:
    :param month:
    :param cur:
    :return:
    '''
    df = pd.read_csv(fire_name, sep = ',')

    df01 = df[df['lat']>=38]
    df01 = df01[df01['lat']<=41]
    df01 = df01[df01['lon']>=115]
    df01 = df01[df01['lon']<=119]
    count01 = df01.shape[0]

    df02 = df[df['lat']>=33]
    df02 = df02[df02['lat']<=36]
    df02 = df02[df02['lon']>=116]
    df02 = df02[df02['lon']<=119]
    count02 = df02.shape[0]


    df03 = df[df['lat']>=30]
    df03 = df03[df03['lat']<=33]
    df03 = df03[df03['lon']>=118]
    df03 = df03[df03['lon']<=122]
    count03 = df03.shape[0]


    df04 = df[df['lat']>=50]
    df04 = df04[df04['lat']<=53]
    df04 = df04[df04['lon']>=120]
    df04 = df04[df04['lon']<=126]
    count04 = df04.shape[0]


    df05 = df[df['lat']>=30]
    df05 = df05[df05['lat']<=35]
    df05 = df05[df05['lon']>=87]
    df05 = df05[df05['lon']<=94]
    count05 = df05.shape[0]

    year = int(float(year))
    month = int(float(month))
    item = [year, month, count01, count02, count03, count04, count05]
    cur.execute("INSERT INTO fire_counts VALUES(?,?,?,?,?,?,?)",item)

def ExtractFireCount():
    '''
    提取感兴趣区域火点数量
    :return:
    '''
    conn = sqlite3.connect('fire.db')
    cur = conn.cursor()
    sql = "create table if NOT EXISTS fire_counts(year int, month int, COUNT_avr_JJJ float, " \
          "COUNT_avr_HH float, COUNT_avr_CJ float, COUNT_avr_DXAL float, COUNT_avr_QZGY float)"
    cur.execute(sql)

    folder = '/Users/wuliang/Documents/数据/火点数据/fire_count'    # 文件夹路径
    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)>9:
                fire_name = folder+os.sep+name
                year = name[-10:-6]
                month = name[-6:-4]
                print year, month
                csv2sqlite(fire_name, year, month, cur)
    conn.commit()


if __name__=="__main__":

    # ResearchRegion() ## Plot the research regions
    # ExtractCO()
    # ExtractAOD()
    # ExtractNO2()
    # ExtractFireCount()
    print "bingo"