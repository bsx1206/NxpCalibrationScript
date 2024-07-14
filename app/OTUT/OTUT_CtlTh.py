'''
Created on May 21, 2022

@author: Mark.Kan
'''
import sys
sys.path.append(r'../')
sys.path.append(r'../../driver/')
sys.path.append(r'../../equipment/')
sys.path.append(r'../../equipment/power/')
sys.path.append(r'../../equipment/oven')
sys.path.append(r'../../equipment/mux')
sys.path.append(r'../../equipment/multimeter')
sys.path.append(r'../../equipment/tempref')
import time, math
import numpy as np
import os
import platform
import testsInit

if 0:
    base_dir=os.path.dirname(os.path.abspath(__file__))
else:
    base_dir=os.path.dirname(os.path.realpath(sys.executable))

def DTS_ACCURACY():
    test = testsInit.TEST(os.path.join(base_dir, 'setting.conf'))
    powerChannel = test.powerChannel
    LinxNumber = test.LinxNumber
    print(test.reportName)
    if test.init() == False:
        return
    reportTitle=   ['Type','Command','ChipID','UID','Vset(mV)','Tset(C)','Tref(C)','Tm(C)','RawData','Time']
    reportDataType=['%s',  '%s',      '%d',    '%s', '%.4f',    '%.4f',   '%.4f',   '%.4f', '%s',   '%s']
    reportDict=dict(zip(reportTitle,reportDataType))
    # print(reportDict)
    reportPath = "Report\\" + test.reportName + "_%s.csv" %(time.strftime("%Y%m%d_%H%M%S", time.localtime()))
    fobj = test.CreateReportFile(reportPath,reportTitle)
    test.pcSer.tx('cc 0\n')
    test.pcSer.tx('sdc 1\n')
    test.pcSer.tx('slp 10000\n')
    test.pcSer.tx('snp 10000\n')
    test.pcSer.tx('ssp 10000\n')
    test.pcSer.tx('stp 10000\n')
    test.pcSer.tx('sdc 0\n')

    test.ps.config(ch=powerChannel, voltage=3300, current=3000, voltlimit=32000, currlimit=3000)
    test.ps.on(ch=powerChannel)
    time.sleep(5)
    count=0
    while test.pc.linx_num<LinxNumber:
        test.pc.en()
        count += 1
        if count > 5:
            return False
    test.pc.Initialise()
    UID = test.pc.get_UniqueID()
    test.ps.off(ch=powerChannel)
    # test.pc.set_Mode(operatingMode="Standby")
    test.oven.start()
    for tempIDX,Tset in enumerate(test.ovenTempPoint if test.ovenTempInputMode==0 else range(test.ovenTempPoint[0],test.ovenTempPoint[1],test.ovenTempPoint[2])):
        test.oven.setTemp(temp=Tset, delay=test.ovenDelayFirst if tempIDX==0 else test.ovenDelayEach)
        for voltIDX,Vset in enumerate(test.psVoltPoint if test.psVoltInputMode==0 else range(test.psVoltPoint[0],test.psVoltPoint[1],test.psVoltPoint[2])):
            test.ps.config(ch=powerChannel, voltage=Vset, current=2000, voltlimit=32000, currlimit=3000)
            dts_type_name=['Tdm','Tdg']#,'Tcm','Tcg'
            dts_types=["FFE2004", "FFE2005"]#, "FFE2002", "FFE2003"
            tempMeasList = [0.0] * (LinxNumber)
            tempMeasRawData=[0]* (LinxNumber)
            for dtsIdx,dts_type in enumerate(dts_types):
                test.ps.off(ch=powerChannel)
                # test.pc.set_Mode(operatingMode="Standby")
                time.sleep(600)
                # time.sleep(1)
                Tref=(test.tr.getData(1)+test.tr.getData(2))/2
                test.ps.on(ch=powerChannel)
                test.pcSer.tx('sdc 1\n')
                if Vset<=2200:
                    test.ps.config(ch=powerChannel, voltage=3300, current=2000, voltlimit=32000, currlimit=3000)
                    time.sleep(0.1)
                    DTS = test.pc.cmd2(dts_type, 1)
                    test.ps.config(ch=powerChannel, voltage=Vset, current=2000, voltlimit=32000, currlimit=3000)
                time.sleep(0.1)
                while True:
                    DTS = test.pc.cmd2(dts_type, 5)
                    if len(DTS) != 5: continue
                    if len(DTS[4]) != LinxNumber: continue
                    break
                test.ps.off(ch=powerChannel)
                test.pcSer.tx('sdc 0\n')
                # test.pc.set_Mode(operatingMode="Standby")
                for i in range(0, 5, 1):
                    for j in range(1, LinxNumber, 1):
                        data = DTS[i][j]
                        dts_cal = test.pc.cal_temp(frame_str=data)
                        if (dts_cal != 0) and (abs(dts_cal) != 0.0625) and (dts_cal != 127.9375) and tempMeasList[j]== 0.0 :  # abs(dts_cal-temp)<10
                            tempMeasList[j]=dts_cal
                            tempMeasRawData[j]=data
                Test_time = time.strftime("%H:%M:%S", time.localtime())
                for li in range(1,LinxNumber):
                    test.RecordData(fobj, reportDataType, [dts_type_name[dtsIdx],dts_type,li,UID[0][li],Vset,Tset,Tref,tempMeasList[li],tempMeasRawData[li],Test_time])
    fobj.close()
    test.deinit()
def DTS_Rth():
    print('DTS_Rth')

def DTS_OTUT():
    print('DTS_OTUT')

    test = testsInit.TEST(os.path.join(base_dir, 'setting.conf'))
    powerChannel = test.powerChannel
    LinxNumber = test.LinxNumber
    OverTemp = test.overTemp
    UnderTemp = test.underTemp

    print(test.reportName)
    if test.init() == False:
        return
    reportTitle = [   'ChipID', 'UID', 'Vset(mV)', 'Tset(C)',  'OT(C)',   'UT(C)', 'Tref(C)', 'DTSm(C)', 'DTSg(C)', 'CTSm(C)', 'CTSg(C)', 'DTSm(RD)', 'DTSg(RD)', 'CTSm(RD)', 'CTSg(RD)', 'Rth', 'SR(12)', 'TD(14)', 'TMshc','TGshc', 'OTUTResult','RthResult','Time']
    reportDataType = ['%d',     '%s',  '%.4f',      '%.4f',    '%.4f',    '%.4f',    '%.4f',    '%.4f',    '%.4f',    '%.4f',    '%.4f',   '%s',       '%s',       '%s',       '%s',       '%d',  '%s',    '%s',     '%.4f',  '%.4f',    '%s',         '%s',      '%s']
    reportDict = dict(zip(reportTitle, reportDataType))
    # print(reportDict)
    reportPath = "Report\\" + 'OTUT_' + test.reportName + "_%s.csv" % (time.strftime("%Y%m%d_%H%M%S", time.localtime()))
    fobj = test.CreateReportFile(reportPath, reportTitle)
    test.pcSer.tx('cc 0\n')
    test.pcSer.tx('sdc 1\n')
    test.pcSer.tx('slp 10000\n')
    test.pcSer.tx('snp 10000\n')
    test.pcSer.tx('ssp 10000\n')
    test.pcSer.tx('stp 10000\n')

    test.ps.config(ch=powerChannel, voltage=3300, current=3000, voltlimit=32000, currlimit=3000)
    test.ps.on(ch=powerChannel)
    time.sleep(5)
    count = 0
    while test.pc.linx_num < LinxNumber:
        test.pc.en()
        count += 1
        if count > 5:
            print('enumeration error')
            return False
    RthList=[30 for i in range(test.pc.linx_num)]
    test.pc.Initialise()
    test.pc.set_TempTh(OverTemp = OverTemp if OverTemp>=0 else OverTemp+256, UnderTemp = UnderTemp if UnderTemp>=0 else UnderTemp+256)
    UID = test.pc.get_UniqueID()

    test.pcSer.tx('sdc 1\n')
    test.pcSer.tx('RT FFF007D 2\n')
    test.pcSer.tx('RT FF2FFFF 2\n')
    test.pcSer.tx('RT FFF0000 2\n')
    test.pcSer.tx('RT FFD0012\n')
    test.pcSer.tx('RT FFAFFFF 2\n')
    test.pcSer.tx('RT FFB0004 2\n')
    # time.sleep(5 * 60)
    dts_type_name = ['Tdm', 'Tdg', 'Tcm', 'Tcg', 'SR(12)', 'TD(14)']
    dts_types = ["FFE0004", "FFE0005", "FFE0002", "FFE0003", "FFD0012", "FFD0014"]
    testConditionDict = {'normal': 0, 'overTemp': 1, 'underTemp': 2}
    Tset = 25
    Tref = 25
    for voltIDX, Vset in enumerate(test.psVoltPoint if test.psVoltInputMode == 0 else range(test.psVoltPoint[0], test.psVoltPoint[1],test.psVoltPoint[2])):
        test.ps.config(ch=powerChannel, voltage=Vset, current=2000, voltlimit=32000, currlimit=3000)
        testCondition=testConditionDict['normal']
        while 1:
            if testCondition == testConditionDict['normal']:
                OverTemp=60
                UnderTemp=10
            elif testCondition == testConditionDict['overTemp']:
                OverTemp=10
                UnderTemp=0
            elif testCondition == testConditionDict['underTemp']:
                OverTemp=60
                UnderTemp=50
            test.pc.set_TempTh(OverTemp=OverTemp if OverTemp >= 0 else OverTemp + 256,
                               UnderTemp=UnderTemp if UnderTemp >= 0 else UnderTemp + 256)
            test.pcSer.tx('RT FFD0012\n')
            test.pcSer.tx('RT FFAFFFF 2\n')
            time.sleep(1)
            tempMeasList = [[0.0] * (LinxNumber) for i in dts_types]
            tempMeasRawData = [[0] * (LinxNumber) for i in dts_types]

            for dtsIdx, dts_type in enumerate(dts_types):
                getDataTimes=5
                while True:
                    DTS = test.pc.cmd2(dts_type, getDataTimes)
                    if len(DTS) != getDataTimes: continue
                    if len(DTS[getDataTimes-1]) != LinxNumber: continue
                    break
                for j in range(1, LinxNumber, 1):
                    for i in range(0, getDataTimes, 1):
                        data = DTS[i][j]
                        if dts_type != "FFD0012" and dts_type != "FFD0014":
                            dts_cal = test.pc.cal_temp(frame_str=data)
                            tmpData = int(data, 16)
                            if (tmpData & (1 << 23) != 0) and tempMeasList[dtsIdx][j] == 0.0:
                                tempMeasList[dtsIdx][j] = dts_cal
                                tempMeasRawData[dtsIdx][j] = data
                            else:
                                continue
                        else:
                            tempMeasRawData[dtsIdx][j] = data
            Test_time = time.strftime("%H:%M:%S", time.localtime())
            tempMeasDict = dict(zip(dts_type_name, tempMeasList))
            tempMeasRawDataDict = dict(zip(dts_type_name, tempMeasRawData))
            for li in range(1, LinxNumber):
                td=tempMeasRawDataDict['TD(14)'][li]
                tdTmp=int(td[-5:-1],16)
                if testCondition == testConditionDict['normal']:
                    OTUTResult= 'Pass' if (tdTmp&0x0F)==0x0 else 'Fail'
                elif testCondition == testConditionDict['overTemp']:
                    OTUTResult = 'Pass' if (tdTmp&0x0F)==0x05 else 'Fail'
                elif testCondition == testConditionDict['underTemp']:
                    OTUTResult = 'Pass' if (tdTmp&0x0F)==0x0A else 'Fail'
                TMshc=tempMeasDict['Tdm'][li]-(0.017*Vset/1000)*RthList[li]
                TGshc=tempMeasDict['Tdg'][li]-(0.017*Vset/1000)*RthList[li]
                RthResult= 'Pass' if abs(TMshc-tempMeasDict['Tcm'][li])<1 and abs(TGshc-tempMeasDict['Tcg'][li])<1 else 'Fail'
                test.RecordData(fobj, reportDataType,[li, UID[0][li], Vset, Tset, OverTemp,UnderTemp,Tref,tempMeasDict['Tdm'][li],tempMeasDict['Tdg'][li],tempMeasDict['Tcm'][li],tempMeasDict['Tcg'][li],tempMeasRawDataDict['Tdm'][li],tempMeasRawDataDict['Tdg'][li],tempMeasRawDataDict['Tcm'][li],tempMeasRawDataDict['Tcg'][li], RthList[li],tempMeasRawDataDict['SR(12)'][li],tempMeasRawDataDict['TD(14)'][li],TMshc,TGshc,OTUTResult, RthResult,Test_time])
            testCondition+=1
            if testCondition>testConditionDict['underTemp']:
                break

    fobj.close()
    test.deinit()
if __name__ == "__main__":
    DTS_OTUT()
