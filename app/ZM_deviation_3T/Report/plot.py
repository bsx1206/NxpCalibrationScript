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
    for i,idf in enumerate(df.groupby(['chip_id','Gain','Tset(C)','Vset(mV)'])):
        id=idf[0][0]
        gain=idf[0][1]
        Tset=idf[0][2]
        Vset=idf[0][3]
        for j,freqdf in enumerate(idf[1].groupby(['Freq(Hz)'])):
            freq=freqdf[0]
            dev=max(freqdf[1]['FreqM(Hz)'].max()-freq,freqdf[1]['FreqM(Hz)'].min()-freq)/freq*100
            result='Pass' if dev<=1 else 'Fail'
            newlist.append({'chip_id':id,'Gain':gain,'Tset(C)':Tset,'Vset(mV)':Vset,'Freq(Hz)':freq,'deviation(%)':dev,'result':result})
    newDf=pd.DataFrame(newlist)
    newDf1=newDf.style.applymap(func=lambda x:'background-color:red' if x!='Pass' else 'background-color:green',subset=['result'])
    # print(newDf)

    fileName=os.path.splitext(os.path.split(filepath)[-1])[0] + "_plot1.xlsx"
    if 1:
        with pd.ExcelWriter(fileName, mode='w') as writer:  # 默认的mode为w，即代表覆盖写入。a代表不覆盖新增。
            newDf1.to_excel(writer, sheet_name='ID%d_deviation' % (2), index=False)
    app = xw.App(visible=False, add_book=False)
    for i,idf in enumerate(newDf.groupby(['chip_id','Tset(C)'])):
        id = idf[0][0]
        Tset = idf[0][1]
        newidf=idf[1].style.applymap(func=lambda x:'background-color:red' if x!='Pass' else 'background-color:green',subset=['result'])
        with pd.ExcelWriter(fileName, mode='a') as writer:  # 默认的mode为w，即代表覆盖写入。a代表不覆盖新增。
            newidf.to_excel(writer, sheet_name="ID%d,T%d" % (id, Tset), index=False)
        bk = app.books.open(fileName)
        figOne, axesOne = plt.subplots(1, 1, sharex=True, sharey=True, constrained_layout=True)
        figOne.suptitle(t='ZM deviation under %d degC'%Tset)
        figOne.supxlabel('Freq(Hz)')
        figOne.supylabel('deviation [%]')
        sht = bk.sheets("ID%d,T%d" % (id, Tset))
        width = 600
        height = width // 4 * 3
        shtRange=sht.range('%s%d' % ('I', 1+(0*round(height/14))))
        for j,jdf in enumerate(idf[1].groupby(['Gain','Vset(mV)'])):
            print(jdf)
            gain=jdf[0][0]
            Vset=jdf[0][1]
            jdf[1].plot(x='Freq(Hz)', y='deviation(%)', ax=axesOne, label='Gain%s,%.1fV'%(gain,Vset/1000),xlabel='',ylim=(0,1),#ylim=(-10,10),#title='T%d,ID%d,Gain%s,vrStd' % (Tset, id, gain),
                                      logx=True,  fontsize=5, xticks=(0.01,0.1,1,10,100,1000,10000))
            axesOne.legend(loc='upper right')
        sht.pictures.add(figOne, left=shtRange.left, top=shtRange.top, width=width, height=height)
        bk.save()
        bk.close()
    app.quit()
    plt.show()


if __name__ == "__main__":

    zm_plot('ZM_Deviation_1168_ZMBoard_2v5To5v5_-40to125_PowerSupply_NULL_20220822_181024.csv')

    exit()

