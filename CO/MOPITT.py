#coding=utf-8
# 此脚本实现MOPITT数据（HDF格式）的打开、坐标转换、另存为TIFF格式、获取特定坐标的值以及可视化图像

"""
---- author = "liang wu" ----
---- time = "20150305" ----
---- Email = "wl062345@gmail.com" ----
"""

import os
import re

import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import cm
import numpy as np
import gdal,gdalnumeric
import osr
import sqlite3

coon = sqlite3.connect("co_column.db")
cur = coon.cursor()
cur.execute("create table if not EXISTS co_total_column(year int,month int,wlg float,bj float)")
# 连接数据库并创建表

def run(hdf_file,file_name):
    """
    :param hdf_file: 要处理的HDF文件路径
    :param file_name: 读取数据并另存为Tiff的文件名
    :return:
    """

    with h5py.File(hdf_file, mode='r') as f:
        # 调用h5py模块实现HDF的读取
        group = f['/HDFEOS/GRIDS/MOP03/Data Fields']     # 读取CO浓度所在的数据域
        dsname = 'RetrievedCOTotalColumnDay'             # 要读取的数据区名称，这里指“白天反演的总CO柱浓度”
        data = group[dsname][:].T                        # 读取CO浓度矩阵
        fillvalue = group[dsname].attrs['_FillValue']
        data[data == fillvalue] = np.nan                 # 获得数据中值缺失的部分
        data = np.ma.masked_array(data, np.isnan(data))  # 对值缺失部分作掩膜处理

        y = f['/HDFEOS/GRIDS/MOP03/Data Fields/Latitude'][:]    # 获取数据的纬度
        x = f['/HDFEOS/GRIDS/MOP03/Data Fields/Longitude'][:]   # 获取数据的经度
        longitude, latitude = np.meshgrid(x, y)                 # 并将经纬度转换成格网

        la_wlg,lo_wlg = [36.2700,100.9200]       # 对应地面监测站”瓦里关“的经纬度
        la_bj,lo_bj = [39.9073,116.4112]         # 北京经纬度
        row = round(la_wlg-latitude.min())
        col = round(lo_wlg-longitude.min())
        line = round(la_bj-latitude.min())
        pix = round(lo_bj-longitude.min())       # 瓦里关和北京的经纬度转换为格网
        year = int(hdf_file[52:56])
        month = int(hdf_file[56:58])             # 获取HDF文件路径中的”年、月“等时间信息
        if type(data[row][col]) != np.float32:
            data[row][col] = 0
        a = data[row][col].item()
        if type(data[line][pix]) != np.float32:
            data[line][pix] = 0
        a = data[row][col].item()
        b = data[line][pix].item()               # 获取瓦里关和北京两点的CO浓度
    item = [year,month,a,b]    # item包括四项内容的列表
    cur.execute("INSERT INTO co_total_column VALUES(?,?,?,?)",item)      #将item的值插入已经建好的数据库的表中

    save2Tiff(data,y,x,file_name)
    # 调用save2Tiff函数将CO浓度数据存储为TIFF格式数据

    #plotMap(data,latitude,longitude)
    # 调用plotMap函数将CO浓度数据在地图上可视化出来

    #stere(data,y,x,file_name)
    # 调用stere函数将CO浓度数据在地图上可视化出来，与plotMap不同的是地图设置、投影不同


def save2Tiff(array,lat,lon,file_name):
    """
    :param array: CO浓度数据矩阵
    :param lat: 经度
    :param lon: 纬度
    :param file_name: tiff存储文件名
    :return:
    """
    xmin,ymin,xmax,ymax = [lon.min(),-lat.min(),lon.max(),-lat.max()]
    nrows,ncols = np.shape(array)
    xres = 1.0
    yres = 1.0
    geotransform=(xmin,xres,0,ymax,0, yres)      # 以上五行计算“坐标系统”参数

    outpath = file_name+'.tif'                   # 加后缀的文件名
    output_raster = gdal.GetDriverByName('GTiff').Create(outpath,ncols,nrows,1,gdal.GDT_Float32)
    # 利用"gdal"模块创建tiff对象
    output_raster.SetGeoTransform(geotransform)          # 构建“坐标系统”
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    output_raster.SetProjection( srs.ExportToWkt() )
    output_raster.GetRasterBand(1).WriteArray(array)     # 写tiff,完成数据的存储

def plotMap(data,latitude,longitude):
    """
    :param data: CO浓度数据矩阵
    :param latitude: 纬度
    :param longitude: 经度
    :return:
    """

    m = Basemap(projection='cyl', resolution='l',
                llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180)
    # m为构建的地图基础，包括投影、分辨率、地图范围
    m.drawcoastlines(linewidth=0.5)           # 给地图添加海岸线、以及内陆水体边界
    m.drawparallels(np.arange(-90, 91, 45))
    m.drawmeridians(np.arange(-180, 180, 45), labels=[True,False,False,True])   # 画出经度纬度线，并标注大小
    m.readshapefile("China",'good',drawbounds=1)                                # 添加矢量显示到地图中

    sc = m.scatter(longitude, latitude, c=data, s=1, cmap=plt.cm.jet,
                   edgecolors=None, linewidth=0)                                # 这里以散点的形式画出（简洁处理）
    cb = m.colorbar()                                                           # 添加值对应的颜色条
    plt.show()


def stere(data,latitude,longitude,filename):
    """
    :param data: CO浓度数据矩阵
    :param latitude: 纬度
    :param longitude: 经度
    :param filename:
    :return:
    """
    ax = plt.gca()
    fig = plt.figure()
    m = Basemap(width=10000000,height=7500000,
            resolution='l',projection='stere',\
            lat_ts=35,lat_0=35,lon_0=107.)
    nx = int((m.xmax-m.xmin)/5000.)+1
    ny = int((m.ymax-m.ymin)/5000.)+1
    topodat = m.transform_scalar(data,longitude,latitude,nx,ny)
    im = m.imshow(topodat,cm.GMT_haxby,vmin=0,vmax=4e18)
    m.drawcoastlines()
    m.drawcountries()
    m.drawparallels(np.arange(-80.,81.,20.),labels=[1,0,0,0])
    # 画平行的纬度,前一个参数是表示起点，终点，间距的序列，后一个参数是指在哪一个方向显示纬度、经度值
    m.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1])
    # 画平行的经度
    m.colorbar(im)
    plt.title("CO"+filename[12:14])
    outname = filename+'.png'
    fig.savefig(outname, dpi=fig.dpi)
    # 将画出的图保存


def hdf2tif(i):
    """
    在本地，共有15个文件夹分别存储2000-2014年的影像，需要按年份遍历每个文件夹内的影像（每年12景影像）
    :param i: 年份
    :return:
    """
    print "the num of year: %d"%i
    year = str(i)
    folder = '/Users/wuliang/Documents/coDATA/MOPITT'+os.sep+year    # 文件夹路径

    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)>15:
                hdf_file = folder+os.sep+name
                # 得到单个HDF文件的路径
                try:
                    hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
                except KeyError:
                    pass
                run(hdf_file,name)
                # 调用run()函数，实现下一步功能


if __name__ == "__main__":

    # MOPITT数据包括从2000年到2014年一共一百多景影像
    i = 2000
    while i<=2014:
        hdf2tif(i)
        # 调用hdf2tif()实现整个任务，这是此脚本的起点
        i = i+1
    coon.commit()
    coon.close()
    # 关闭数据库连接
