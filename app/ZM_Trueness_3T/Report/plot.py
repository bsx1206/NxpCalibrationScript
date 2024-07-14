'''
Created on Dec 12nd, 2021

@author: Mark.Kan
'''
import math

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
import xlwings as xw

base_dir=os.path.dirname(os.path.abspath(__file__))
import numpy as np

from matplotlib.transforms import (
    Bbox, TransformedBbox, blended_transform_factory)
from mpl_toolkits.axes_grid1.inset_locator import (
    BboxPatch, BboxConnector, BboxConnectorPatch)
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def zm_plot1(filepath):
    df = pd.read_csv(filepath, skiprows=2)
    newlist=[]
    for i,idf in enumerate(df.groupby(['Tset','Gain'])):
        if idf[0][0]==27 and idf[0][1]=='1x':
            print(idf[1])
            for j,freqdf in enumerate(idf[1].groupby(['Freq(Hz)'])):
                freq=freqdf[0]
                freqstdvr = freqdf[1]['Vr(uV)'].std() * 3
                freqstdvi = freqdf[1]['Vi(uV)'].std() * 3
                newlist.append({'freq':freq,'stdvr':freqstdvr,'stdvi':freqstdvi})
    newDf=pd.DataFrame(newlist)
    print(newDf)
    figOne, axesOne = plt.subplots(1, 1)
    ret = newDf.plot(x='freq', y='stdvr', ax=axesOne, label='vr',
                   xlabel='freq', ylabel='Offset(%)', logx=True, rot=30, fontsize=5)
    ret = newDf.plot(x='freq', y='stdvi', ax=axesOne, label='vi',
                     xlabel='freq', ylabel='Offset(%)', logx=True, rot=30, fontsize=5)
    plt.show()
    return
def zm_plot(filepath):
    df = pd.read_csv(filepath, skiprows=2)
    newlist=[]
    df['Amp'] = (df['Zr(mohm)'] ** 2 + df['Zi(mohm)'] ** 2) ** 0.5
    df['Ang'] = np.arctan(-df['Zi(mohm)'] / df['Zr(mohm)'])
    for i,idf in enumerate(df.groupby(['chip_id','Gain','Tset(C)','Vset(mV)'])):
        id=idf[0][0]
        gain=idf[0][1]
        Tset=idf[0][2]
        Vset=idf[0][3]
        for j,freqdf in enumerate(idf[1].groupby(['Freq(Hz)'])):
            freq=freqdf[0]
            ampMean=freqdf[1]['Amp'].mean()
            angMean=freqdf[1]['Ang'].mean()*180/3.1415926
            ampOffset=(freqdf[1]['Amp'].mean()-0.255)/0.255*100
            newlist.append({'chip_id':id,'Gain':gain,'Tset(C)':Tset,'Vset(mV)':Vset,'Freq(Hz)':freq,'ampMean':ampMean,'angMean':angMean,'ampOffset':ampOffset})
    newDf=pd.DataFrame(newlist)
    print(newDf)

    fileName=os.path.splitext(os.path.split(filepath)[-1])[0] + "_plot1.xlsx"

    if 1:
        with pd.ExcelWriter(fileName, mode='w') as writer:  # 默认的mode为w，即代表覆盖写入。a代表不覆盖新增。
            newDf.to_excel(writer, sheet_name='ID%d_data' % (2), index=False)
    for i,idf in enumerate(newDf.groupby(['chip_id','Tset(C)'])):
        id = idf[0][0]
        Tset = idf[0][1]
        with pd.ExcelWriter(fileName, mode='a', engine="openpyxl") as writer:  # 默认的mode为w，即代表覆盖写入。a代表不覆盖新增。
            idf[1].to_excel(writer, sheet_name="ID%d,T%d" % (id, Tset), index=False)
    # bk = xw.Book(fileName)
    app = xw.App(visible=False, add_book=False)
    bk = app.books.open(fileName)
    for i,idf in enumerate(newDf.groupby(['chip_id','Tset(C)'])):
        id = idf[0][0]
        Tset = idf[0][1]
        sht = bk.sheets("ID%d,T%d" % (id, Tset))
        width = 600
        height = width//4*3
        for v,vdf in enumerate(idf[1].groupby(['Vset(mV)'])):
            shtRange = sht.range('%s%d' % ('I', 1+(v*round(height/14))))
            shtAngRange = sht.range('%s%d' % ('V', 1 + (v * round(height / 14))))
            Vset = vdf[0]
            figOne, axesOne = plt.subplots(2, 2, sharex=True, sharey=True, constrained_layout=True)
            figOne.suptitle(t='ID%d,T%d,V%.1f,Amplitude offset' % (id,Tset, Vset/1000))
            figOne.supxlabel('Freq(Hz)')
            figOne.supylabel('offset(%)')
            figAng, axesAng = plt.subplots(2, 2, sharex=True, sharey=True, constrained_layout=True)


            for j, gdf in enumerate(vdf[1].groupby(['Gain'])):
                gain=gdf[0]
                if gain == '1x':
                    yhline = 1.7
                    ylline = -1.7
                    yhAngLine = 0.4
                    ylAngLine = -0.4
                    xPos = 0
                    yPos = 0
                elif gain == '4x':
                    yhline = 1.7
                    ylline = -1.7
                    yhAngLine = 0.4
                    ylAngLine = -0.4
                    xPos = 1
                    yPos = 0
                else:
                    yhline = 1.7
                    ylline = -1.7
                    yhAngLine = 0.4
                    ylAngLine = -0.4
                    xPos = 0
                    yPos = 1
                ret = gdf[1].plot(x='Freq(Hz)', y='ampOffset', ax=axesOne[xPos][yPos], legend=None,ylim=(-10,10),#title='T%d,ID%d,Gain%s,vrStd' % (Tset, id, gain),
                                  logx=True,  fontsize=5, xticks=(0.01,0.1,1,10,100,1000,10000))
                ret = gdf[1].plot(x='Freq(Hz)', y='angMean', ax=axesAng[xPos][yPos], legend=None,ylim=(-1,1),#title='T%d,ID%d,Gain%s,viStd' % (Tset, id, gain),
                                  logx=True,  fontsize=5, xticks=(0.01,0.1,1,10,100,1000,10000))
                axesOne[xPos][yPos].text(0.45, 0.9, 'Gain%s'%gain, bbox=dict(facecolor='r', alpha=0.5), fontsize=10,
                          color='g', transform=axesOne[xPos][yPos].transAxes)
                axesOne[xPos][yPos].axhline(y=yhline, color='k', linestyle="-.", alpha=0.5)
                axesOne[xPos][yPos].axhline(y=ylline, color='k', linestyle="-.", alpha=0.5)
                # axesOne[xPos][yPos].legend(loc='upper right')
                axesOne[xPos][yPos].set_xlabel(xlabel=None)
                axesAng[xPos][yPos].text(0.45, 0.9, 'Gain%s' % gain, bbox=dict(facecolor='r', alpha=0.5), fontsize=10,
                                         color='g', transform=axesAng[xPos][yPos].transAxes)
                axesAng[xPos][yPos].axhline(y=yhAngLine, color='k', linestyle="-.", alpha=0.5)
                axesAng[xPos][yPos].axhline(y=ylAngLine, color='k', linestyle="-.", alpha=0.5)
                # axesAng[xPos][yPos].legend(loc='upper right')
                axesAng[xPos][yPos].set_xlabel(xlabel=None)
            figAng.suptitle(t='ID%d,T%d,V%.1f,Angle offset' % (id, Tset, Vset / 1000))
            figAng.supxlabel('Freq(Hz)')
            figAng.supylabel('offset(deg)')
            sht.pictures.add(figOne, left=shtRange.left,top=shtRange.top, width=width, height=height)
            sht.pictures.add(figAng, left=shtAngRange.left, top=shtAngRange.top, width=width, height=height)
    bk.save()
    bk.close()
    app.quit()

if __name__ == "__main__":
    zm_plot('ZM_Trueness_1168_ZMBoard_2v5_-40to125_LDO_NULL_20240328_101252.csv')
    exit()

