#coding=utf-8
# 此脚本实现了从地面监测数据（txt格式）读取数据、存入数据库并可视化

"""
---- author = "liang wu" ----
---- time = "20150305" ----
---- Email = "wl062345@gmail.com" ----
"""

import os
import csv
import re
import sqlite3

def txt2sqlite():
    file = open('co_wlg_surface-flask_1_ccgg_event.txt')
    conn = sqlite3.connect('co.db')
    cur = conn.cursor()
    sql = "create table if NOT EXISTS co_surface(site_code CHAR,year int,month int,day int,hour int,minute int," \
          "seconds int,parameter_formula char,value FLOAT,uncertainty FLOAT,latitude FLOAT,longitude FLOAT,altitude FLOAT)"
    cur.execute(sql)
    pattern = re.compile(r"[^\s]+")    # 因为文件中包括非数据部分，需要用正则表达式匹配数值区域

    for line in file:
        if line[0]!='#':
            line_list = pattern.findall(line)
            item = [line_list[0],int(line_list[1]),int(line_list[2]),int(line_list[3]),int(line_list[4]),int(line_list[5]),
                    int(line_list[6]),line_list[9],float(line_list[11]),float(line_list[12]),float(line_list[21]),
                    float(line_list[22]),float(line_list[23])]
            cur.execute("INSERT INTO co_surface VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",item)
    file.close()
    conn.commit()

def avr(rows):
    """
    计算某一个月的CO数值序列，需要考虑该月缺少值的情况，所以有一个if判断
    :param rows: 某一个月的CO数值序列
    :return: avr,某一个月平均值
    """
    n = 0
    sum = 0
    for row in rows:
        n = n+1
        sum = sum + row[0]
    if n==0:
        avr = 0.0
    else:
        avr = sum/n
    return avr


def get_avr():
    """
    从数据库中取出数据，并计算月平均值
    :return:
    """
    coon = sqlite3.connect('co.db')
    cur = coon.cursor()
    sql = "create table if NOT EXISTS month_avr(year int,month int,avr_value FLOAT)"
    cur.execute(sql)
    # 连接数据库并创建表

    y = 1991
    while y<=2013:
        m = 1
        while m<=12:
            sql_avr = "select value from co_surface where year=%d AND month=%d"%(y,m)
            rows = coon.execute(sql_avr)
            avt = avr(rows)
            i = [y,m,avt]
            cur.execute("insert into month_avr values(?,?,?)",i)
            m = m+1
        y = y+1
    coon.commit()


if __name__ == "__main__":
    txt2sqlite()      # 将CO地面监测站数据文件打开、读取、提取并存入数据库
    get_avr()         # 计算CO地面监测站数据的月平均值

