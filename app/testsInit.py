'''
Created on May 21, 2022

@author: Mark.Kan
'''
import sys
import configparser
from csv import reader
sys.path.append(r'../driver/')
sys.path.append(r'../equipment/')
sys.path.append(r'../equipment/power/')
sys.path.append(r'../equipment/oven')
sys.path.append(r'../equipment/mux')
sys.path.append(r'../equipment/multimeter')
sys.path.append(r'../equipment/tempref')
sys.path.append(r'../equipment/counter')
import phy, api, reg

class TEST():
    def __init__(self,filepath):
        self.configFile = filepath
        self.ReportName = ''
        self.mm = None
        self.mux = None
        self.ps = None
        self.oven = None
        self.tr = None
        self.pcSer = None
        self.pc = None
        self.config=configparser.ConfigParser()
        self.config.sections()
        self.config.read(self.configFile)
        self.readConfig()
    def getConfig(self,section,val):
        return self.config.get(section,val)
    def readConfig(self):
        # get multimeter configure
        self.mmEnable = bool(int(self.config.get('multimeter setting', 'enable')))
        self.mmType = self.config.get('multimeter setting', 'type')
        self.mmAddr = self.config.get('multimeter setting', 'addr')

        # get mux configure
        self.muxEnable = bool(int(self.config.get('mux setting', 'enable')))
        self.muxType = self.config.get('mux setting', 'type')
        self.muxAddr = self.config.get('mux setting', 'addr')

        # get power supply configure
        self.psEnable=bool(int(self.config.get('power setting', 'enable')))
        self.psType=self.config.get('power setting', 'type')
        self.psAddr = self.config.get('power setting', 'addr')
        self.psVoltInputMode=int(self.config.get('power setting' , 'inputMode'))
        self.psVoltPoint = self.config.get('power setting', 'points').split(',')
        self.psVoltPoint = list(map(int, self.psVoltPoint))

        # get oven configure
        self.ovenEnable = bool(int(self.config.get('oven setting', 'enable')))
        self.ovenType = self.config.get('oven setting', 'type')
        self.ovenAddr = self.config.get('oven setting', 'addr')
        self.ovenTempInputMode = int(self.config.get('oven setting', 'inputMode'))
        self.ovenTempPoint = self.config.get('oven setting', 'points').split(',')
        self.ovenTempPoint = list(map(int, self.ovenTempPoint))
        self.ovenDelayFirst=int(self.config.get('oven setting','delayFirst'))
        self.ovenDelayEach=int(self.config.get('oven setting','delayEach'))

        # get tempRef configure
        self.trEnable=bool(int(self.config.get('tempRef setting', 'enable')))
        self.trType=self.config.get('tempRef setting', 'type')
        self.trAddr = self.config.get('tempRef setting', 'addr')

        # get pack controller configure
        self.pcAddr = self.config.get('pack controller setting', 'addr')

        # get counter configure
        self.cntEnable=bool(int(self.config.get('counter setting', 'enable')))
        self.cntType=self.config.get('counter setting', 'type')
        self.cntAddr = self.config.get('counter setting', 'addr')

        # define report file name
        TestCase = self.config.get('report name', 'TestCase')
        Setup = self.config.get('report name', 'Setup')
        VolCon = self.config.get('report name', 'VolCon')
        TempCon = self.config.get('report name', 'TempCon')
        PowSup = self.config.get('report name', 'PowSup')
        OtherCon = self.config.get('report name', 'OtherCon')
        self.reportName = TestCase + "_" + Setup + "_" + VolCon + "_" + TempCon + "_" + PowSup + "_" + OtherCon
    def init(self):
        if self.mmEnable:
            import DNS_MultiMeter
            self.mm=DNS_MultiMeter.MM(type=self.mmType,addr=self.mmAddr,enable=self.mmEnable)
            if self.mm.open()==False:
                return False
        if self.muxEnable:
            import DNS_RelayMux 
            self.mux=DNS_RelayMux.MUX(type=self.muxType,addr=self.muxAddr)
            if self.mux.open()==False:
                return False
        if self.psEnable:
            
            import DNS_Power
            self.ps=DNS_Power.PS(type=self.psType,addr=self.psAddr)
            if self.ps.open()==False:
                return False
        if self.ovenEnable:
            import DNS_Oven
            self.oven=DNS_Oven.OVEN(type=self.ovenType,addr=self.ovenAddr)
            if self.oven.open()==False:
                return False
        if self.trEnable:
            import DNS_TempRef
            self.tr=DNS_TempRef.TR(type=self.trType,addr=self.trAddr)
            if self.tr.open()==False:
                return False
        if self.cntEnable:
            import DNS_Counter
            self.cnt=DNS_Counter.CNT(type=self.cntType,addr=self.cntAddr)
            if self.cnt.open()==False:
                return False
        self.pcSer= phy.ser(self.pcAddr)
        self.pc=api.chain(self.pcSer)
        if self.pc.open()==False:
            return False
    def deinit(self):
        if self.mmEnable:
            self.mm.close()
        if self.muxEnable:
            self.mux.close()
        if self.psEnable:
            self.ps.off(ch=0)
            self.ps.close()
        if self.ovenEnable:
            self.oven.stop()
            self.oven.close()
        if self.trEnable:
            self.tr.close()
        if self.cntEnable:
            self.cnt.close()
        self.pc.close()

    def CreateReportFile(self, filename, reportTitle):
        fobj = open(filename, 'a')
        for title in reportTitle:
            fobj.write(title)
            fobj.write(',')
        fobj.write('\n')
        fobj.flush()
        return fobj

    def RecordData(self, fobj, dataType, dataList):
        for i, type in enumerate(dataType):
            fobj.write(type % (dataList[i]))
            fobj.write(',')
        fobj.write('\n')
        fobj.flush()
