#!/usr/bin/env python2.7
#coding=utf-8
# 解析MOPITTCO数据——day
"""
---- author = "liang wu" ----
---- time = "20151229" ----
---- Email = "wl062345@gmail.com" ----
"""
import numpy.ma as ma
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt


## -----++++++-----------++++++-----------++++++-----------++++++------ ##
## -----++++++-----------++++++-----------++++++-----------++++++------ ##

def run_surfaceMixRatio_day(hdf_file):

    with h5py.File(hdf_file, mode='r') as f:
        group = f['/HDFEOS/GRIDS/MOP03/Data Fields']
        ds_name = 'RetrievedCOSurfaceMixingRatioDay'
        data = group[ds_name][:]
        year = hdf_file[71:75]
        month = hdf_file[75:77]
        day = hdf_file[77:79]

        arr = np.zeros((180, 360))
        for i in range(180):
            arr[i, :] = data[:, 179-i].T
        out_dir = 'day' + os.sep + 'surfaceMixRatio_day' + os.sep + str(year)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        out_file =  out_dir + os.sep + year + month + day + '.txt'
        np.savetxt(out_file, arr)

def read_surfaceMixRatio_day():
    '''
    # 读取表面混合比 by day
    :return:
    '''
    folder = '/Users/wuliang/Documents/数据/卫星数据/CO/2012/'
    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)==28:
                hdf_file = root + os.sep + name
                run_surfaceMixRatio_day(hdf_file)

## -----++++++-----------++++++-----------++++++-----------++++++------ ##
## -----++++++-----------++++++-----------++++++-----------++++++------ ##

def filter_zero(txt_file):
    '''
    # 将为0的值改为np.nan
    :param txt_file:
    :return:
    '''
    new_data = np.loadtxt(txt_file)
    for i in range(new_data.shape[0]):
        for j in range(new_data.shape[1]):
            if new_data[i][j] < 0:
                new_data[i][j] = np.nan
            else:
                pass
    return new_data

def getThreeDaysCO_SMR():
    '''
    # 1DAY 合成3DAY 表面混合比率
    :return:
    '''
    folder = 'day/surfaceMixRatio_day/2012/'
    out_folder = 'day/surfaceMixRatio_3days/2012/'
    if not os.path.exists(out_folder):
            os.makedirs(out_folder)
    count = 0
    list_file = []
    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)>11:
                count += 1
                txt_file = root + os.sep + name
                arr = filter_zero(txt_file)
                list_file.append(folder + str(count) + '.txt')
                np.savetxt(folder + str(count) + '.txt', arr)

    for i in range(0, count-3, 3):
        new_data = np.loadtxt(list_file[i])
        sum_arr = new_data[:, :]
        num_add = np.zeros((180, 360))

        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if sum_arr[m][n] >0:
                    num_add[m][n] = num_add[m][n] + 1

        print "-----=====-----"

        for j in range(i+1, i+3):
            now = np.loadtxt(list_file[j])
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
        np.savetxt(out_folder + os.sep + str(i+1) + ".txt", sum_arr)


def getSixDaysCO_SMR():
    '''
    # 1DAY 合成6DAY 表面混合比率
    :return:
    '''
    folder = 'day/surfaceMixRatio_day/2012/'
    out_folder = 'day/surfaceMixRatio_d6ays/2012'
    if not os.path.exists(out_folder):
            os.makedirs(out_folder)
    count = 0
    list_file = []

    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)>11:
                count += 1
                txt_file = root + os.sep + name
                arr = filter_zero(txt_file)
                list_file.append(folder + str(count) + '.txt')
                #np.savetxt(folder + str(count) + '.txt', arr)

    for i in range(0, count-6, 6):
        new_data = np.loadtxt(list_file[i])
        sum_arr = new_data[:, :]
        num_add = np.zeros((180, 360))

        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if sum_arr[m][n] >0:
                    num_add[m][n] = num_add[m][n] + 1

        print "-----=====-----"

        for j in range(i+1, i+6):
            now = np.loadtxt(list_file[j])
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
        np.savetxt(out_folder + os.sep + str(i+1) + "_six.txt", sum_arr)


def getTenDaysCO_SMR():
    '''
    # 1DAY 合成10DAY 表面混合比率
    :return:
    '''
    folder = 'day/surfaceMixRatio_day/2012/'
    out_folder = 'day/surfaceMixRatio_10days/2012'
    if not os.path.exists(out_folder):
            os.makedirs(out_folder)
    count = 0
    list_file = []

    for root, dirs, files in os.walk(folder):
        for name in files:
            if len(name)>11:
                count += 1
                txt_file = root + os.sep + name
                arr = filter_zero(txt_file)
                list_file.append(folder + str(count) + '.txt')
                #np.savetxt(folder + str(count) + '.txt', arr)

    for i in range(0, count-10, 10):
        new_data = np.loadtxt(list_file[i])
        sum_arr = new_data[:, :]
        num_add = np.zeros((180, 360))

        for m in range(sum_arr.shape[0]):
            for n in range(sum_arr.shape[1]):
                if sum_arr[m][n] >0:
                    num_add[m][n] = num_add[m][n] + 1

        print "-----=====-----"

        for j in range(i+1, i+10):
            now = np.loadtxt(list_file[j])
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
        np.savetxt(out_folder + os.sep + str(i+1) + "_ten.txt", sum_arr)
## -----++++++-----------++++++-----------++++++-----------++++++------ ##
## -----++++++-----------++++++-----------++++++-----------++++++------ ##

if __name__=="__main__":

    print "BINGO !!!"

