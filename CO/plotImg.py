#coding=utf-8
# 此脚本画出研究区域
"""
---- author = "liang wu" ----
---- time = "20150916" ----
---- Email = "wl062345@gmail.com" ----
"""
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.basemap import maskoceans
from matplotlib.patches import Polygon

def draw_basemap_mixratio(txt_file, day,out_folder):

    fig = plt.figure(figsize=(11, 8), facecolor="w")
    data = np.loadtxt(txt_file)
    arr = np.zeros((180, 360))
    for i in range(180):
        arr[i, :] = data[179-i, :]

    longitude = np.loadtxt('lonlat_data/longitude.txt')
    latitude = np.loadtxt('lonlat_data/latitude.txt')

    m = Basemap(llcrnrlon=65, llcrnrlat=5, urcrnrlon=145, urcrnrlat=55, projection='mill', resolution='h')
    m.drawparallels(np.arange(5.,90.,10.), labels=[1,0,0,0])
    m.drawmeridians(np.arange(60.,181.,15.), labels=[0,0,1,0])
    m.readshapefile("shp/CHINA", 'CHINA', drawbounds=1, color='black')

    im = m.pcolormesh(longitude, latitude, arr, shading='flat', cmap=plt.cm.bwr, latlon=True, vmin=0, vmax=600)
    cbar = m.colorbar()
    cbar.ax.set_ylabel("CO surfaceMixRatio(molecules $cm^{-2}$)", color='black', fontsize='13', rotation=90)
    plt.title("MOPITT V6T average CO surfaceMixRatio for " + str(day), y=1.06, fontsize='13')
    plt.savefig(out_folder + str(day) + ".png")

def plot_tenday_mixratio():
    out_folder = 'tenDay_mixratio_img/'
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for i in range(0,34):
        txt_file = 'day/surfaceMixRatio_10days/2012/'+ str(1+10*i) + '_ten.txt'
        draw_basemap_mixratio(txt_file, 1+10*i, out_folder)
    print " "

def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""
    #    Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    #    The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

def draw_screen_poly(lats, lons, m):

    x, y = m(lons, lats)
    xy = zip(x,y)
    poly = Polygon(xy, 'black', facecolor='None', edgecolor='black', linewidth=1.5, alpha=1)
    plt.gca().add_patch(poly)

def ResearchRegion_surface():
    '''
    在地图上画出柱表面混合比图
    :return:
    '''

    fig = plt.figure(figsize=(11, 8), facecolor="white")
    #data = np.loadtxt('seasonAvr_data/SurfaceMixingRatio/1_seasonAvr.txt')
    data = np.loadtxt('allYearAvr_data/SurfaceMixingRatio/allYearAvr.txt')
    arr = np.zeros((180, 360))
    for i in range(180):
        arr[i, :] = data[179-i, :]

    longitude = np.loadtxt('lonlat_data/longitude.txt')
    latitude = np.loadtxt('lonlat_data/latitude.txt')

    m = Basemap(llcrnrlon=70, llcrnrlat=15, urcrnrlon=138, urcrnrlat=55, projection='mill', resolution='h')
    m.drawparallels(np.arange(5.5,90.5,1.), color='w', linewidth=0.5, dashes=[1,1],labels=[0,0,0,0])
    m.drawmeridians(np.arange(60.5,181.5,1.), color='w', linewidth=0.5, dashes=[1,1],labels=[0,0,0,0])
    m.drawmapboundary(fill_color='0.3')
    m.readshapefile("shp/CHINA", 'CHINA', drawbounds=1, color='black')

    topo = maskoceans(longitude, latitude, arr)
    im = m.pcolormesh(longitude, latitude, topo, shading='flat', cmap=plt.cm.jet, latlon=True, vmin=0, vmax=500)
    m.drawlsmask(ocean_color='w', lsmask=0)

    cbar = m.colorbar()
    cbar.ax.set_ylabel("SurfaceMixingRatio", color='black', fontsize='14', rotation=90)
    plt.show()


def plotCOColumn():
    '''
    在地图上画出柱浓度图
    '''
    fig = plt.figure(figsize=(11, 8))
    rect = fig.patch
    rect.set_facecolor('white')
    data = np.loadtxt('seasonAvr_data/TotalColumn/1_seasonAvr.txt')
    longitude = np.loadtxt('lonlat_data/longitude.txt')
    latitude = np.loadtxt('lonlat_data/latitude.txt')

    m = Basemap(llcrnrlon=75, llcrnrlat=15, urcrnrlon=138, urcrnrlat=55, projection='mill', resolution='h')
    m.drawparallels(np.arange(5.,90.,10.), labels=[1,0,0,0])
    m.drawmeridians(np.arange(60.,181.,15.), labels=[0,0,1,0])
    m.readshapefile("shp/CHINA", 'CHINA', drawbounds=1, color='black')
    topo = maskoceans(longitude, latitude, data)

    im = m.pcolormesh(longitude, latitude, topo, shading='flat', cmap=plt.cm.jet, latlon=True, vmin=1.e18, vmax=4.e18)
    m.drawlsmask(ocean_color='w', lsmask=0)
    cbar = m.colorbar()
    cbar.ax.set_ylabel("CO coloumn(molecules $cm^{-2}$)", color='black', fontsize='13', rotation=90)
    plt.show()

if __name__=="__main__":
    # ResearchRegion_surface()
    print "Bingo"