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
    freq_1k_list = []
    for i,idf in enumerate(df.groupby(['chip_id','Gain','Tset(C)','Vset(mV)'])):
        id=idf[0][0]
        gain=idf[0][1]
        Tset=idf[0][2]
        Vset=idf[0][3]
        for j, freqdf in enumerate(idf[1].groupby(['Freq(Hz)'])):
            freq = freqdf[0]
            if freq > 90 and freq < 110:
                continue
            vrStd = freqdf[1]['Vr(uV)'].std() * 3
            viStd = freqdf[1]['Vi(uV)'].std() * 3
            newlist.append({'chip_id':id,'Gain':gain,'Tset(C)':Tset,'Vset(mV)':Vset,'Freq(Hz)':freq,'Vr3Sigma':vrStd,'Vi3Sigma':viStd})
            if freq > 900 and freq < 1100:
                freq_1k_list.append({'chip_id':id,'Gain':gain,'Tset(C)':Tset,'Vset(mV)':Vset,'Freq(Hz)':freq,'Vr3Sigma':vrStd,'Vi3Sigma':viStd})
    newDf=pd.DataFrame(newlist)
    print(newDf)
    fileName=os.path.splitext(os.path.split(filepath)[-1])[0] + "_plot.xlsx"

    freq_1k_df = pd.DataFrame(freq_1k_list)
    print(freq_1k_df)
    file_1k_name = os.path.splitext(os.path.split(filepath)[-1])[0] + "_1k_plot.xlsx"

    newDf.hist(column='Vr3Sigma', bins=10)
    #newDf.plot(kind='hist',x='Vr3Sigma',bins=10)

    if 1:
        with pd.ExcelWriter(fileName, mode='w') as writer:  # 默认的mode为w，即代表覆盖写入。a代表不覆盖新增。
            newDf.to_excel(writer, sheet_name='ID%d_3Sigma' % (2), index=False)
        with pd.ExcelWriter(file_1k_name, mode='w') as writer:
            freq_1k_df.to_excel(writer, sheet_name='result', index=False)
    for i,idf in enumerate(newDf.groupby(['chip_id','Tset(C)'])):
        id = idf[0][0]
        Tset = idf[0][1]
        with pd.ExcelWriter(fileName,engine="openpyxl",  mode='a') as writer:  # 默认的mode为w，即代表覆盖写入。a代表不覆盖新增。
            idf[1].to_excel(writer, sheet_name="ID%d,T%d" % (id, Tset), index=False)
    # bk = xw.Book(fileName)
    app = xw.App(visible=False, add_book=False)
    if 1:
        bk = app.books.open(fileName)
        for i,idf in enumerate(newDf.groupby(['chip_id','Tset(C)'])):
            id = idf[0][0]
            Tset = idf[0][1]
            sht = bk.sheets("ID%d,T%d" % (id, Tset))
            width = 300
            height = width//4*3

            for v,vdf in enumerate(idf[1].groupby(['Vset(mV)'])):
                Vset = vdf[0]
                for j, gdf in enumerate(vdf[1].groupby(['Gain'])):
                    gain=gdf[0]
                    shtRange = sht.range('%s%d' % ('H', 1 + ((v*3+j) * round(height / 14))))
                    figOne, axesOne = plt.subplots(1, 1, sharex = True, sharey = True, constrained_layout=True)
                    figOne.suptitle(t='ID%d,Gain%s,T%d,V%.1f' % (id, gain, Tset, Vset / 1000))
                    figOne.supxlabel('Freq(Hz)')
                    figOne.supylabel('3sigma(uV)')
                    if gain == '1x':
                        yline = 7.2
                        ylim=(0,40)
                    elif gain == '4x':
                        yline = 1.8
                        ylim = (0, 15)
                    else:
                        yline = 0.45
                        ylim = (0, 10)
                    ret = gdf[1].plot(x='Freq(Hz)', y='Vr3Sigma', ax=axesOne, label='Vr',ylim=ylim,xticks=(0.01,0.1,1,10,100,1000,10000),#title='T%d,ID%d,Gain%s,vrStd' % (Tset, id, gain),
                                      xlabel='',logx=True, rot=30, fontsize=7)
                    ret = gdf[1].plot(x='Freq(Hz)', y='Vi3Sigma', ax=axesOne, label='Vi',ylim=ylim,xticks=(0.01,0.1,1,10,100,1000,10000),#title='T%d,ID%d,Gain%s,viStd' % (Tset, id, gain),
                                      xlabel='',logx=True, rot=30, fontsize=7)

                    # axesOne[xPos][yPos].text(0.45, 0.9, 'Gain%s'%gain, bbox=dict(facecolor='r', alpha=0.5), fontsize=10,
                    #           color='g', transform=axesOne[xPos][yPos].transAxes)
                    axesOne.axhline(y=yline, color='k', linestyle="-.", alpha=0.5)
                    axesOne.legend(loc='upper right')
                    sht.pictures.add(figOne, left=shtRange.left,top=shtRange.top, width=width, height=height)
        #plt.show()
        bk.save()
        bk.close()


    bk = app.books.open(file_1k_name)
    sht = bk.sheets('result')
    for i, idf in enumerate(freq_1k_df.groupby(['Vset(mV)','Gain'])):
        Vset = idf[0][0]
        #Tset = idf[0][1]
        gain = idf[0][1]
        width = 300
        height = width // 4 * 3
        print(Vset, gain)
        shtRange = sht.range('%s%d' % ('H', 1 + ((i * 3) * round(height / 42))))
        figOne, axesOne = plt.subplots(1, 1, sharex=True, sharey=True, constrained_layout=True)
        figOne.suptitle(t='Vr,Gain%s,V%.1f' % (gain, Vset / 1000))
        figOne.supxlabel('Tset(C)')
        figOne.supylabel('3sigma(uV)')

        shtRange2 = sht.range('%s%d' % ('O', 1 + ((i * 3) * round(height / 42))))
        figOne2, axesOne2 = plt.subplots(1, 1, sharex=True, sharey=True, constrained_layout=True)
        figOne2.suptitle(t='Vi,Gain%s,V%.1f' % (gain, Vset / 1000))
        figOne2.supxlabel('Tset(C)')
        figOne2.supylabel('3sigma(uV)')
        if gain == '1x':
            yline = 7.2
            ylim = (0, 40)
        elif gain == '4x':
            yline = 1.8
            ylim = (0, 15)
        else:
            yline = 0.45
            ylim = (0, 10)

        if 1:
            for j, gdf in enumerate(idf[1].groupby(['chip_id'])):
                id = gdf[0]

                ret = gdf[1].plot(x='Tset(C)', y='Vr3Sigma', ax=axesOne, label='id%d' % (id), ylim=ylim,
                                  #xticks=(0.01, 0.1, 1, 10, 100, 1000, 10000),
                                  # title='T%d,ID%d,Gain%s,vrStd' % (Tset, id, gain),
                                  xlabel='', logx=False, rot=30, fontsize=7)

                ret = gdf[1].plot(x='Tset(C)', y='Vi3Sigma', ax=axesOne2, label='id%d' % (id), ylim=ylim,
                                  #xticks=(0.01, 0.1, 1, 10, 100, 1000, 10000),
                                  # title='T%d,ID%d,Gain%s,viStd' % (Tset, id, gain),
                                  xlabel='', logx=False, rot=30, fontsize=7)

                # axesOne[xPos][yPos].text(0.45, 0.9, 'Gain%s'%gain, bbox=dict(facecolor='r', alpha=0.5), fontsize=10,
                #           color='g', transform=axesOne[xPos][yPos].transAxes)
                axesOne.axhline(y=yline, color='k', linestyle="-.", alpha=0.5)
                axesOne.legend(loc='upper right')
                axesOne2.axhline(y=yline, color='k', linestyle="-.", alpha=0.5)
                axesOne2.legend(loc='upper right')
        sht.pictures.add(figOne, left=shtRange.left, top=shtRange.top, width=width, height=height)
        sht.pictures.add(figOne2, left=shtRange2.left, top=shtRange2.top, width=width, height=height)
    plt.show()
    bk.save()
    bk.close()

    app.quit()

if __name__ == "__main__":
    zm_plot('ZM_Noise_1168_ZMBoard_2V5to5V5_-40to125_LDO_NULL_20240321_150316.csv')
    exit()

