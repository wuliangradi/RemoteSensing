#!/usr/bin/env python2.7
#coding=utf-8
# 解析MOPITTCO数据——month
"""
---- author = "liang wu" ----
---- time = "20151111" ----
---- Email = "wl062345@gmail.com" ----
"""

import os
import h5py
import numpy as np
import matplotlib.pyplot as plt


def runColumnMonth(hdf_file):
    with h5py.File(hdf_file, mode='r') as f:
        group = f['/HDFEOS/GRIDS/MOP03/Data Fields']
        ds_name = 'RetrievedCOTotalColumnDay'
        data = group[ds_name][:].T
        year = hdf_file[77:81]
        month = hdf_file[81:83]

        out_dir = 'month' + os.sep + 'TotalColumn'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        TC_name = out_dir + os.sep + year + month+'.txt'
        np.savetxt(TC_name, data)


def readColumnMonth():
    '''
    # 读取柱浓度数据 by month
    :return:
    '''
    folder = '/Users/wuliang/Documents/数据/卫星数据/CO/allYear_j'
    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)==28:
                hdf_file = root + os.sep + name
                runColumnMonth(hdf_file)

## -----++++++-----------++++++-----------++++++-----------++++++------ ##
## -----++++++-----------++++++-----------++++++-----------++++++------ ##

def runSurfaceMixRatioMonth(hdf_file):

    with h5py.File(hdf_file, mode='r') as f:
        group = f['/HDFEOS/GRIDS/MOP03/Data Fields']
        ds_name = 'RetrievedCOSurfaceMixingRatioDay'
        data = group[ds_name][:]

        year = hdf_file[77:81]
        month = hdf_file[81:83]

        arr = np.zeros((180, 360))
        for i in range(180):
            arr[i, :] = data[:, 179-i].T

        out_dir = 'month' + os.sep + 'SurfaceMixingRatio'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        SMR_name = out_dir + os.sep + year + month+'.txt'
        np.savetxt(SMR_name, arr)

def readSurfaceMixRatioMonth():
    '''
    # 读取表面混合比 by month
    :return:
    '''
    folder = '/Users/wuliang/Documents/数据/卫星数据/CO/allYear_j'

    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)==28:
                hdf_file = root + os.sep + name
                runSurfaceMixRatioMonth(hdf_file)

## -----++++++-----------++++++-----------++++++-----------++++++------ ##
## -----++++++-----------++++++-----------++++++-----------++++++------ ##


def read_latlon():
    '''
    # 解析经纬度格网
    :return:
    '''
    hdf_file = '/Users/wuliang/Documents/数据/卫星数据/CO/MOPITT/2000/MOP03TM-200004-L3V94.2.1.he5'
    with h5py.File(hdf_file, mode='r') as f:
        y = f['/HDFEOS/GRIDS/MOP03/Data Fields/Latitude'][:]
        x = f['/HDFEOS/GRIDS/MOP03/Data Fields/Longitude'][:]
        longitude, latitude = np.meshgrid(x, y)
        np.savetxt('lonlat_data' + os.sep + 'longitude.txt', longitude)
        np.savetxt('lonlat_data' + os.sep + 'latitude.txt', latitude)

## -----++++++-----------++++++-----------++++++-----------++++++------ ##
## -----++++++-----------++++++-----------++++++-----------++++++------ ##

def plotImage(arr):
    '''
    # 粗略画图
    :param arr:
    :return:
    '''
    fig  = plt.figure(figsize=(10,6), dpi=80, facecolor='w', edgecolor='w', frameon=True)
    imAx = plt.imshow(arr, origin='lower', interpolation='nearest')
    fig.colorbar(imAx, pad=0.01, fraction=0.1, shrink=1.00, aspect=20)

def plotHistogram(arr):
    '''
    # 分布图
    :param arr:
    :return:
    '''
    fig  = plt.figure(figsize=(5,5), dpi=80, facecolor='w',edgecolor='w',frameon=True)
    plt.hist(arr.flatten(), bins=100)

## -----++++++-----------++++++-----------++++++-----------++++++------ ##
## -----++++++-----------++++++-----------++++++-----------++++++------ ##

def year_save(txt_file):

    new_data = np.loadtxt(txt_file)
    for i in range(new_data.shape[0]):
        for j in range(new_data.shape[1]):
            if new_data[i][j] < 0:
                new_data[i][j] = np.nan
            else:
                pass
    return new_data

def year_average(item):
    '''
    # 每一年的平均值
    :return:
    '''
    folder = 'month/' + item
    out_folder = 'yearAvr_data/' + item
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for y in range(2000, 2016):
        with open(out_folder + os.sep + str(y) + ".txt", 'w') as outfile:

            for root, dirs, files in os.walk(folder):
                for name in files:
                    if len(name)>9 and int(name[:4])==y:
                        txt_file = root + os.sep + name
                        arr = year_save(txt_file)
                        np.savetxt(outfile, arr)

        print "-----=====-----"

        new_data = np.loadtxt(out_folder + os.sep + str(y) + ".txt")
        mon_num = int(new_data.shape[0]/180)
        sum_arr = new_data[0:180, :]
        num_add = np.zeros((180, 360))

        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if sum_arr[m][n] >0:
                    num_add[m][n] = num_add[m][n] + 1

        for i in range(1, mon_num):
            now = new_data[180*i : 180*(i+1), :]
            for m in range(sum_arr.shape[0]):
                for n in range(sum_arr.shape[1]):
                    if now[m][n] > 0:
                        num_add[m][n] += 1
                        if sum_arr[m][n] > 0:
                            sum_arr[m][n] += now[m][n]
                        else:
                            sum_arr[m][n] = now[m][n]

        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if type(sum_arr[m][n]) == np.float64:
                    sum_arr[m][n] = sum_arr[m][n]/num_add[m][n]

        np.savetxt(out_folder + os.sep + str(y) + "_avr.txt", sum_arr)


## -----++++++-----------++++++-----------++++++-----------++++++------ ##
## -----++++++-----------++++++-----------++++++-----------++++++------ ##

def month_average(item):
    '''
    # 每季度的多年平均值
    :return:
    '''
    folder = 'month/'+item
    out_folder = 'monthAvr_data/'+item
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for mon in range(1, 13):
        with open(out_folder + os.sep + str(mon) + ".txt", 'w') as outfile:

            for root, dirs, files in os.walk(folder):
                for name in files:

                    if len(name)>9 and int(name[4:6])==mon:
                        txt_file = root + os.sep + name
                        arr = year_save(txt_file)
                        np.savetxt(outfile, arr)

        print "-----=====-----"

        new_data = np.loadtxt(out_folder + os.sep + str(mon) + ".txt")
        mon_num = int(new_data.shape[0]/180)
        sum_arr = new_data[0:180, :]
        num_add = np.zeros((180, 360))

        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if sum_arr[m][n] >0:
                    num_add[m][n] = num_add[m][n] + 1

        for i in range(1, mon_num):
            now = new_data[180*i : 180*(i+1), :]
            for m in range(sum_arr.shape[0]):
                for n in range(sum_arr.shape[1]):
                    if now[m][n] > 0:
                        num_add[m][n] += 1
                        if sum_arr[m][n] > 0:
                            sum_arr[m][n] += now[m][n]
                        else:
                            sum_arr[m][n] = now[m][n]

        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if type(sum_arr[m][n]) == np.float64:
                    sum_arr[m][n] = sum_arr[m][n]/num_add[m][n]

        np.savetxt(out_folder + os.sep + str(mon) + "_avr.txt", sum_arr)
## -----++++++-----------++++++-----------++++++-----------++++++------ ##
## -----++++++-----------++++++-----------++++++-----------++++++------ ##

def season_average(item):
    '''
    # 每一月的多年平均值
    :return:
    '''
    input_folder = 'monthAvr_data/' + item
    out_folder = 'seasonAvr_data/' + item
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    month_list = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2]
    for season in range(1, 5):

        print "-----=====-----"

        new_data = np.loadtxt(input_folder + os.sep + str(3*(season-1)+1) + "_avr.txt")
        sum_arr = new_data[0:180, :]
        num_add = np.zeros((180, 360))

        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if sum_arr[m][n] >0:
                    num_add[m][n] = num_add[m][n] + 1
        start = (season-1)*3
        for i in month_list[start+1:start+3]:
            now = np.loadtxt(input_folder + os.sep + str(i) + "_avr.txt")
            for m in range(sum_arr.shape[0]):
                for n in range(sum_arr.shape[1]):
                    if now[m][n] > 0:
                        num_add[m][n] += 1
                        if sum_arr[m][n] > 0:
                            sum_arr[m][n] += now[m][n]
                        else:
                            sum_arr[m][n] = now[m][n]

        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if type(sum_arr[m][n]) == np.float64:
                    sum_arr[m][n] = sum_arr[m][n]/num_add[m][n]

        np.savetxt(out_folder + os.sep + str(season) + "_seasonAvr.txt", sum_arr)


def allYear_average(item):
    '''
    # 每一月的多年平均值
    :return:
    '''
    input_folder = 'yearAvr_data/' + item
    out_folder = 'allYearAvr_data/' + item
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    month_list = range(2002,2015)

    new_data = np.loadtxt(input_folder + os.sep + "2001_avr.txt")
    sum_arr = new_data[0:180, :]
    num_add = np.zeros((180, 360))

    for m in range(sum_arr.shape[0]):
        for n in range(sum_arr.shape[1]):
            if sum_arr[m][n] >0:
                num_add[m][n] = num_add[m][n] + 1

    for i in month_list:
        now = np.loadtxt(input_folder + os.sep + str(i) + "_avr.txt")
        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if now[m][n] > 0:
                    num_add[m][n] += 1
                    if sum_arr[m][n] > 0:
                        sum_arr[m][n] += now[m][n]
                    else:
                        sum_arr[m][n] = now[m][n]

    for m in range(sum_arr.shape[0]):
        for n in range(sum_arr.shape[1]):
            if type(sum_arr[m][n]) == np.float64:
                sum_arr[m][n] = sum_arr[m][n]/num_add[m][n]

    np.savetxt(out_folder + os.sep  + "allYearAvr.txt", sum_arr)


if __name__=="__main__":
    #year_average('TotalColumn')
    #month_average('TotalColumn')
    #season_average('TotalColumn')
    #allYear_average('SurfaceMixingRatio')
    print "BINGO !!!"

