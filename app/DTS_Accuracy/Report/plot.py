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

def plot(filepath):
    df = pd.read_csv(filepath, skiprows=0)
    print(df)
    df['Err']=df['Tm(C)']-df['Tref(C)']
    df['HL'] = df['Tset(C)'].apply(lambda x: 3 if (x > 85 or x < -10) else 2.5)
    df['LL'] = df['Tset(C)'].apply(lambda x: -3 if (x > 85 or x < -10) else -2.5)
    df['Result'] = df.apply(lambda x: True if (x['LL'] < x['Err'] < x['HL']) else False , axis = 1)
    plotList=[]
    for tempIdx, tempdf in enumerate(df.groupby(['Tset(C)'])):
        temp=tempdf[0]
        xlim=[1500,6000]
        ylim=[-7,7]
        tempFigSp, tempAxesSp = plt.subplots(4, 4, sharex=True, sharey=True, constrained_layout=True,figsize=(17.78,10))
        legend_elements = [Line2D([0], [0], color='green', lw=1, label='Main DTS', linestyle="-"),
                           Line2D([0], [0], color='blue', lw=1, label='Guard DTS', linestyle="-"),
                           Line2D([0], [0], color='red', lw=1, label='High Limit', linestyle="-"),
                           Line2D([0], [0], color='purple', lw=1, label='Low Limit', linestyle="-"), ]
        tempFigSp.legend(handles=legend_elements, framealpha=0.3)
        tempFigSp.suptitle("%ddegC DTS Result" % (temp))
        plotList.append({'temp':temp,'plot':tempFigSp})
        for idIdx, idDf in enumerate(tempdf[1].groupby(['ChipID'])):
            id=idDf[0]
            axes=tempAxesSp[idIdx // 4, idIdx % 4]
            ret = idDf[1].plot(x='Vset(mV)', y='HL', ax=axes, legend=None,color='red',
                                 xlabel='Vset(mV)', ylabel='Err', xlim= xlim,ylim=ylim,  fontsize=7)
            ret = idDf[1].plot(x='Vset(mV)', y='LL', ax=axes, legend=None,color='purple',
                               xlabel='Vset(mV)', ylabel='Err', xlim= xlim, ylim=ylim, rot=30, fontsize=7)
            axes.text(0.9, 0.1, "ID%02d" % id, bbox=dict(facecolor='yellow', alpha=0.5), fontsize=6,
                      color='g', transform=axes.transAxes)
            # resultList=[False if result == False else True for result in idDf[1]['Result']]
            if False in idDf[1]['Result'].unique():
            # if False in resultList:
                axes.axvspan(xlim[0], xlim[1], facecolor='red', alpha=0.3)
                axes.text(0.45, 0.9, 'Fail', bbox=dict(facecolor='r', alpha=0.5), fontsize=10,
                          color='black', transform=axes.transAxes)
            else:
                axes.text(0.45, 0.9, 'Pass', bbox=dict(facecolor='g', alpha=0.5), fontsize=10,
                          color='black', transform=axes.transAxes)
                axes.axvspan(xlim[0], xlim[1], facecolor='green', alpha=0.3)
            for typeIdx, typeDf in enumerate(idDf[1].groupby(['Type'])):
                ret=typeDf[1].plot(x='Vset(mV)', y='Err', ax=axes, legend=None,color='green' if typeDf[0] == 'Tdm' else 'blue',marker='o',ms=3,
                                 xlabel='Vset(mV)', ylabel='Err', xlim= xlim, ylim=ylim, rot=30, fontsize=7)
    plt.show()

    app = xw.App(visible=False)
    bk = app.books.add()
    pltheight = 500
    pltwidth = 890

    # poltlist.reverse()
    for tmpDict in plotList:
        sht = bk.sheets.add('%dDegC'%tmpDict['temp'])
        sht.pictures.add(tmpDict['plot'], left=sht.range('%s%d' % ('B', 1)).left,
                         top=sht.range('%s%d' % ('B', 1)).top, width=pltwidth, height=pltheight)
    bk.save(os.path.splitext(os.path.split(filepath)[-1])[0]+"_plot.xlsx")
    bk.close()
    app.quit()
    return
def plot_liner(filepath):
    df = pd.read_csv(filepath, skiprows=0)
    print(df)
    df['Err'] = df['Tm(C)'] - df['Tref(C)']
    df['HL'] = df['Tset(C)'].apply(lambda x: 3 if (x > 85 or x < -10) else 2.5)
    df['LL'] = df['Tset(C)'].apply(lambda x: -3 if (x > 85 or x < -10) else -2.5)
    df['Result'] = df.apply(lambda x: True if (x['LL'] < x['Err'] < x['HL']) else False, axis=1)
    plotList = []
    for voltIdx, voltdf in enumerate(df.groupby(['Vset(mV)'])):
        volt = voltdf[0]
        # xlim = [1500, 6000]
        ylim = [-7, 7]
        voltFigSp, voltAxesSp = plt.subplots(4, 4, sharex=True, sharey=True, constrained_layout=True,
                                             figsize=(17.78, 10))
        legend_elements = [Line2D([0], [0], color='green', lw=1, label='Main DTS', linestyle="-"),
                           Line2D([0], [0], color='blue', lw=1, label='Guard DTS', linestyle="-"),
                           Line2D([0], [0], color='red', lw=1, label='High Limit', linestyle="-"),
                           Line2D([0], [0], color='purple', lw=1, label='Low Limit', linestyle="-"), ]
        voltFigSp.legend(handles=legend_elements, framealpha=0.3)
        voltFigSp.suptitle("%.2fV DTS Result" % (volt/1000))
        plotList.append({'volt': volt, 'plot': voltFigSp})
        for idIdx, idDf in enumerate(voltdf[1].groupby(['ChipID'])):
            id = idDf[0]+1
            # idIdx+=1
            axes = voltAxesSp[idIdx // 4, idIdx % 4]
            ret = idDf[1].plot(x='Tset(C)', y='HL', ax=axes, legend=None, color='red',
                               xlabel='Tset(C)', ylabel='Err', ylim=ylim, fontsize=7)
            ret = idDf[1].plot(x='Tset(C)', y='LL', ax=axes, legend=None, color='purple',
                               xlabel='Tset(C)', ylabel='Err',  ylim=ylim, rot=30, fontsize=7)
            axes.text(0.9, 0.1, "ID%02d" % id, bbox=dict(facecolor='yellow', alpha=0.5), fontsize=6,
                      color='g', transform=axes.transAxes)
            # resultList=[False if result == False else True for result in idDf[1]['Result']]
            # if False in idDf[1]['Result'].unique():
            #     # if False in resultList:
            #     axes.axvspan(xlim[0], xlim[1], facecolor='red', alpha=0.3)
            #     axes.text(0.45, 0.9, 'Fail', bbox=dict(facecolor='r', alpha=0.5), fontsize=10,
            #               color='black', transform=axes.transAxes)
            # else:
            #     axes.text(0.45, 0.9, 'Pass', bbox=dict(facecolor='g', alpha=0.5), fontsize=10,
            #               color='black', transform=axes.transAxes)
            #     axes.axvspan(xlim[0], xlim[1], facecolor='green', alpha=0.3)
            for typeIdx, typeDf in enumerate(idDf[1].groupby(['Type'])):
                ret = typeDf[1].plot(x='Tset(C)', y='Err', ax=axes, legend=None,
                                     color='green' if typeDf[0] == 'Tdm' else 'blue', marker='o', ms=3,
                                     xlabel='Tset(C)', ylabel='Err',  ylim=ylim, rot=30, fontsize=7)
    plt.show()
    app = xw.App(visible=False)
    bk = app.books.add()
    pltheight = 500
    pltwidth = 890

    # poltlist.reverse()
    for tmpDict in plotList:
        sht = bk.sheets.add('%.2fV' % (tmpDict['volt']/1000))
        sht.pictures.add(tmpDict['plot'], left=sht.range('%s%d' % ('B', 1)).left,
                         top=sht.range('%s%d' % ('B', 1)).top, width=pltwidth, height=pltheight)
    bk.save(os.path.splitext(os.path.split(filepath)[-1])[0] + "_plot.xlsx")
    bk.close()
    app.quit()

if __name__ == "__main__":
    plot_liner('#1.csv')

    exit()

