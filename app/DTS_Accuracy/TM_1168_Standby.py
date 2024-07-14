'''
Created on May 21, 2022

@author: Mark.Kan
'''
import sys
import time, math
import configparser
from csv import reader
import numpy as np
import os
import platform
sys.path.append(r'../')
sys.path.append(r'../../driver/')
sys.path.append(r'../../equipment/')
sys.path.append(r'../../equipment/power/')
sys.path.append(r'../../equipment/oven')
sys.path.append(r'../../equipment/mux')
sys.path.append(r'../../equipment/multimeter')
sys.path.append(r'../../equipment/tempref')
import phy, api, reg
import DNS_Power
import DNS_Oven
import DNS_RelayMux
import DNS_MultiMeter
import DNS_TempRef
import testsInit
base_dir=os.path.dirname(os.path.abspath(__file__))

#base_dir=os.path.dirname(os.path.realpath(sys.executable))

def DTS_ACCURACY():
    test = testsInit.TEST(os.path.join(base_dir, 'setting.conf'))
    powerChannel = int(test.getConfig("test case setting", "powerChannel"))
    LinxNumber = int(test.getConfig("test case setting", "LinxNumber"))
    delayBetEach = int(test.getConfig("test case setting", "delayBetEach"))
    print(test.reportName)
    if test.init() == False:
        return
    reportTitle=   ['Type','Command','ChipID','UID','Vset(mV)','Tset(C)','Tref(C)','Tm(C)','RawData','Time']
    reportDataType=['%s',  '%s',      '%d',    '%s', '%.4f',    '%.4f',   '%.4f',   '%.4f', '%s',   '%s']
    reportDict=dict(zip(reportTitle,reportDataType))

    reportPath = "Report\\" + test.reportName + "_%s.csv" %(time.strftime("%Y%m%d_%H%M%S", time.localtime()))
    fobj = test.CreateReportFile(reportPath,reportTitle)
    test.pcSer.tx('cc 0\n')
    test.pcSer.tx('slp 15000\n')
    test.pcSer.tx('snp 15000\n')
    test.pcSer.tx('ssp 15000\n')
    test.pcSer.tx('stp 15000\n')
    test.pcSer.tx('sdp 15000\n')
    test.pcSer.tx('sdi 70\n')
    test.pcSer.tx('sdd FFD0002\n')
    test.pcSer.tx('sdc 0\n')

    test.ps.config(ch=powerChannel, voltage=3300, current=3000, voltlimit=32000, currlimit=3000) if test.ps!=None else None
    test.ps.on(ch=powerChannel) if test.ps!=None else None
    time.sleep(1)
    count=0
    while test.pc.linx_num < LinxNumber:
        test.pc.en()
        count += 1
        if count > 5:
            return False
    test.pc.Initialise()
    UID = test.pc.get_UniqueID()
    test.pc.set_Mode(operatingMode="Standby")
    test.oven.start() if test.oven!=None else None
    for tempIDX, Tset in enumerate(test.ovenTempPoint if test.ovenTempInputMode==0 else range(test.ovenTempPoint[0],test.ovenTempPoint[1],test.ovenTempPoint[2])):
        test.oven.setTemp(temp=Tset, delay=test.ovenDelayFirst if tempIDX==0 else test.ovenDelayEach) if test.oven!=None else None
        for voltIDX, Vset in enumerate(test.psVoltPoint if test.psVoltInputMode==0 else range(test.psVoltPoint[0],test.psVoltPoint[1],test.psVoltPoint[2])):
            test.ps.config(ch=powerChannel, voltage=Vset, current=2000, voltlimit=32000, currlimit=3000) if test.ps!=None else None
            test.ps.get_current(ch=powerChannel) if test.ps!=None else None
            dts_type_name = ['Tdg','Tdm']#,'Tcm','Tcg'
            dts_types = ["FFE2005", "FFE2004"]#, "FFE2002", "FFE2003"
            for dtsIdx, dts_type in enumerate(dts_types):
                tempMeasList = [0.0] * (LinxNumber)
                tempMeasRawData = [0] * (LinxNumber)
                test.ps.off(ch=powerChannel) if test.ps!=None else None
                time.sleep(delayBetEach)
                Tref = (test.tr.getData(1) + test.tr.getData(2)) / 2
                test.pcSer.tx('sdc 1\n')
                if Vset <= 2200:
                    test.ps.config(ch=powerChannel, voltage=3300, current=2000, voltlimit=32000, currlimit=3000) if test.ps!=None else None
                    print(test.ps.get_current(ch=powerChannel)) if test.ps!=None else None
                    time.sleep(0.2)
                    DTS = test.pc.cmd2(dts_type, 10)
                    print(DTS)
                    test.ps.config(ch=powerChannel, voltage=Vset, current=2000, voltlimit=32000, currlimit=3000) if test.ps!=None else None
                    print(test.ps.get_current(ch=powerChannel)) if test.ps!=None else None
                time.sleep(0.2)
                while True:
                    dataCount=10
                    DTS = test.pc.cmd2(dts_type, dataCount)
                    print(DTS)
                    if DTS == None: continue
                    if len(DTS) != dataCount: continue
                    if len(DTS[4]) != LinxNumber: continue
                    break
                test.pcSer.tx('sdc 0\n')
                test.pc.set_Mode(operatingMode="Standby")
                for i in range(0, dataCount, 1):
                    for j in range(1, LinxNumber, 1):
                        data = DTS[i][j]
                        dts_cal = test.pc.cal_temp(frame_str=data)
                        tmpData = int(data, 16)
                        if abs(dts_cal-Tset)>10:
                            continue
                        if ((tmpData & (1 << 23)) != 0) and tempMeasList[j] == 0.0 :  # abs(dts_cal-temp)<10
                            tempMeasList[j]=dts_cal
                            tempMeasRawData[j]=data
                Test_time = time.strftime("%H:%M:%S", time.localtime())
                
                for li in range(1,LinxNumber):
                    test.RecordData(fobj, reportDataType, [dts_type_name[dtsIdx],dts_type,li,UID[0][li],Vset,Tset,Tref,tempMeasList[li],tempMeasRawData[li],Test_time])
    fobj.close()
    test.deinit()
if __name__ == "__main__":
    DTS_ACCURACY()

