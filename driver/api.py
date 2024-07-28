'''
Created on Feb 14, 2017
Update on Dec 11, 2020

@author: felix.yao
@update: luke.pan
'''

import trx

class chain(trx.trx):
    def __init__(self, phy):
        trx.trx.__init__(self, phy)
        self.Ack = None
        self.Exe = None
        self.VmainRSCpre = None
        self.VmainRSCcur = None
        self.Vmain = None
        self.Vm_code = None
        self.VguardRSCpre = None
        self.VguardRSCcur = None
        self.Vguard = None
        self.Vg_code = None
        self.MainCellTempRSCpre = None
        self.MainCellTempRSCcur = None
        self.MainCellTemp = None
        self.GuardCellTempRSCpre = None
        self.GuardCellTempRSCcur = None
        self.GuardCellTemp = None
        self.MainDTSRSCpre = None
        self.MainDTSRSCcur = None
        self.MainDTS = None
        self.GuardDTSRSCpre = None
        self.GuardDTSRSCcur = None
        self.GuardDTS = None
        self.VZMRSCpre = None
        self.VZMRSCcur = None
        self.VZM = None
        self.VZM_code = None
        self.ZrealRSCpre = None
        self.ZrealRSCcur = None
        self.Zreal = None
        self.ZrealCode = None
        self.ZimagRSCpre = None
        self.ZimagRSCcur = None
        self.Zimag = None
        self.ZimagCode = None
        self.ZM = None
        self.BatchID = None
        self.WaferD = None
        self.IDX = None
        self.IDY = None
    
    def open(self):
        return self.phy.open()
    
    def close(self):
        return self.phy.close()
    
    def _tx(self, *args):
        return self.phy.tx(*args)
# -----------------------------------------------------------------------------
    def set_Bank(self, bank):
        frame_list = self.SetRegBank(BankAddr = bank)
        if frame_list == None: return False
        self.Exe = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
        return True

    def set_VoltTh(self, OverVolt = 255, UnderVolt = 0):
        frame_list = self.SetThVolt(ThOver = OverVolt, ThUnder = UnderVolt)
        if frame_list == None: return False
        self.Exe = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
        return True

    def set_TempTh(self, OverTemp = 255, UnderTemp = 0):
        frame_list = self.SetThTemp(ThOver = OverTemp, ThUnder = UnderTemp)
        if frame_list == None: return False
        self.Exe = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
        return True

    def set_ZMCurr(self, ID=0xFF, enZM="Stop", enXCS="Internal", hiPass="1x", timeOut=255):
        frame_list = self.SetZMCurr(LinxID=ID, EnZM=enZM, EnXCS=enXCS, HiPass=hiPass, TimeOut=timeOut)
        if frame_list == None: return False
        self.Exe = []
        # self.ZrealRSCcur = []
        # self.ZimagRSCcur = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
#             self.ZrealRSCcur.append(map(set_zero, frame))
        return True

    def set_ZMFreq(self, ID=0xFF, Freq_spread="Disable", winEn="Disable", Exponent=0, Mantissa=0 ):
        frame_list = self.SetZMFreq(LinxID=ID, Freq_spread=Freq_spread, WinEn=winEn, Fexponent=Exponent, Fmantissa=Mantissa)
        if frame_list == None: return False
        self.Exe = []
        #mark
        self.ZrealRSCpre = None
        self.ZimagRSCpre = None
        self.ZrealRSCcur = None
        self.ZimagRSCpre = None
        #mark
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
        return True

    def set_BalCurr(self, ID=0xFF, enBalCurr = "Stop", current = 0, timeOut = 0):
        frame_list = self.SetBalCurr(LinxID=ID, EnBal = enBalCurr, Current = current, TimeOut = timeOut)
        if frame_list == None: return False
        self.Exe = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
        return True

    def set_BalVolt(self, ID=0xFF, balMode = "Disable", balVolt = 0):
        frame_list = self.SetBalVolt(LinxID=ID, BalMode = balMode, BalVolt = balVolt,repeat=1)
        if frame_list == None: return False
        self.Exe = []
        # print(frame_list)
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
        return True

    
    def set_SRMask(self, ID=0xFF, cmdErr="NoMask", clockErr="NoMask", intErr="NoMask",
                  gpioErr="NoMask", invalidLockKey="NoMask", openWire="NoMask", zmADCErr="NoMask",
                  balZMDone="NoMask", currErr="NoMask", ldoOoR="NoMask",
                  tempADCErr="NoMask", cellTempErr="NoMask", vmADCErr="NoMask", cellVoltErr="NoMask",
                  brownOut="NoMask"):
        frame_list = self.SetSRMask(LinxID=ID, CmdErr=cmdErr, ClockErr=clockErr, IntErr=intErr,
                  GPIOErr=gpioErr, InvalidLockKey=invalidLockKey, OpenWire=openWire, ZMADCErr=zmADCErr,
                  BalZMDone=balZMDone, CurrErr=currErr, LDOOoR=ldoOoR,
                  TempADCErr=tempADCErr, CellTempErr=cellTempErr, VMADCErr=vmADCErr, CellVoltErr=cellVoltErr,
                  BrownOut=brownOut)
        if frame_list == None: return False
        self.Exe = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
        return True

    
    def set_Mode(self, ID=0xFF, operatingMode="Normal"):
        frame_list = self.SetMode(LinxID=ID, OperatingMode=operatingMode)
        if frame_list == None: return False
        self.Exe = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
        return True


    def set_ForceErr(self, ID=0xFF, vdrcomp="Disable", openWire="Disable", utot="Disable", dtscomp="Disable",
                    uvov="Disable", vmcomp="Disable", gLDODio="Disable", gLDOAna="Disable", gLDODig="Disable",
                    gLDOPll="Disable", mLDOAna="Disable", mLDOBal="Disable"):
        frame_list = self.SetForceErr(self, LinxID=ID, VDRcomp=vdrcomp, OpenWire=openWire, UTOT=utot, DTScomp=dtscomp,
                    UVOV=uvov, VMcomp=vmcomp, GLDODio=gLDODio, GLDOAna=gLDOAna, GLDODig=gLDODig,
                    GLDOPll=gLDOPll, MLDOAna=mLDOAna, MLDOBal=mLDOBal)
        if frame_list == None: return False
        self.Exe = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return False
            self.Exe.append(list(map(check_Exe, frame)))
        return True

# -----------------------------------------------------------------------------
    def get_Status(self, ID=0xFF, statusType="FSMStatus"):
        frame_list = self.GetStatus(LinxID=ID, StatusType=statusType)
        if frame_list == None: return
        self.Ack = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Ack.append(list(map(check_Ack, frame)))
        return frame_list
        
    def get_Vmain(self, ID=0xFF, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction", sampleRate=0, 
                dataType="MainVolt"):
        frame_list = self.GetData(LinxID=ID, ClrExeCnt=clrExeCnt, Equidist=equidist, ResetRSC=resetRSC, SampleRate=sampleRate, 
                DataType=dataType)
        if frame_list == None: return
        self.Ack = []
        self.VmainRSCpre = self.VmainRSCcur
        self.VmainRSCcur = []
        self.Vm_code = []
        self.Vmain = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Vm_code.append([x for x in frame])
            self.Ack.append(list(map(check_Ack, frame)))
            self.VmainRSCcur.append(list(map(check_RSC, frame)))
            self.Vmain.append(list(map(cal_voltage, frame)))
        if self.VmainRSCpre == None: self.VmainRSCpre = self.VmainRSCcur
        return self.Vmain

    def get_Vguard(self, ID=0xFF, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction", sampleRate=0, 
                dataType="GuardVolt"):
        frame_list = self.GetData(LinxID=ID, ClrExeCnt=clrExeCnt, Equidist=equidist, ResetRSC=resetRSC, SampleRate=sampleRate, 
                DataType=dataType)
        if frame_list == None: return
        self.Ack = []
        self.VguardRSCpre = self.VguardRSCcur
        self.VguardRSCcur = []
        self.Vguard = []
        self.Vg_code = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Vg_code.append([x for x in frame])
            self.Ack.append(list(map(check_Ack, frame)))
            self.VguardRSCcur.append(list(map(check_RSC, frame)))
            self.Vguard.append(list(map(cal_voltage, frame)))
        if self.VguardRSCpre == None: self.VguardRSCpre = self.VguardRSCcur
        return self.Vguard

    def get_MainCellTemp(self, ID=0xFF, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction", dataType="MainCellTemp"):
        frame_list = self.GetData(LinxID=ID, ClrExeCnt=clrExeCnt, Equidist=equidist, ResetRSC=resetRSC, DataType=dataType)
        if frame_list == None: return
        self.Ack = []
        self.MainCellTempRSCpre = self.MainCellTempRSCcur
        self.MainCellTempRSCcur = []
        self.MainCellTemp = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Ack.append(list(map(check_Ack, frame)))
            self.MainCellTempRSCcur.append(list(map(check_RSC, frame)))
            self.MainCellTemp.append(list(map(cal_temperature, frame)))
        if self.MainCellTempRSCpre == None: self.MainCellTempRSCpre = self.MainCellTempRSCcur
        return self.MainCellTemp

    def get_GuardCellTemp(self, ID=0xFF, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction", dataType="GuardCellTemp"):
        frame_list = self.GetData(LinxID=ID, ClrExeCnt=clrExeCnt, Equidist=equidist, ResetRSC=resetRSC, DataType=dataType)
        if frame_list == None: return
        self.Ack = []
        self.GuardCellTempRSCpre = self.GuardCellTempRSCcur
        self.GuardCellTempRSCcur = []
        self.GuardCellTemp = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Ack.append(list(map(check_Ack, frame)))
            self.GuardCellTempRSCcur.append(list(map(check_RSC, frame)))
            self.GuardCellTemp.append(list(map(cal_temperature, frame)))
        if self.GuardCellTempRSCpre == None: self.GuardCellTempRSCpre = self.GuardCellTempRSCcur
        return self.GuardCellTemp

    def get_MainDTS(self, ID=0xFF, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction", dataType="MainDieTemp"):
        frame_list = self.GetData(LinxID=ID, ClrExeCnt=clrExeCnt, Equidist=equidist, ResetRSC=resetRSC, DataType=dataType)
        if frame_list == None: return
        self.Ack = []
        self.MainDTSRSCpre = self.MainDTSRSCcur
        self.MainDTSRSCcur = []
        self.MainDTS = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Ack.append(list(map(check_Ack, frame)))
            self.MainDTSRSCcur.append(list(map(check_RSC, frame)))
            self.MainDTS.append(list(map(cal_temperature, frame)))
        if self.MainDTSRSCpre == None: self.MainDTSRSCpre = self.MainDTSRSCcur
        return self.MainDTS

    def get_GuardDTS(self, ID=0xFF, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction", dataType="GuardDieTemp"):
        frame_list = self.GetData(LinxID=ID, ClrExeCnt=clrExeCnt, Equidist=equidist, ResetRSC=resetRSC, DataType=dataType)
        if frame_list == None: return
        self.Ack = []
        self.GuardDTSRSCpre = self.GuardDTSRSCcur
        self.GuardDTSRSCcur = []
        self.GuardDTS = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Ack.append(list(map(check_Ack, frame)))
            self.GuardDTSRSCcur.append(list(map(check_RSC, frame)))
            self.GuardDTS.append(list(map(cal_temperature, frame)))
        if self.GuardDTSRSCpre == None: self.GuardDTSRSCpre = self.GuardDTSRSCcur
        return self.GuardDTS

    def get_VZM(self, ID=0xFF, clrExeCnt="NoReset", equidist="Reset", resetRSC="NoAction", dataType="VZM"):
        frame_list = self.GetData(LinxID=ID, ClrExeCnt=clrExeCnt, Equidist=equidist, ResetRSC=resetRSC, DataType=dataType)
        if frame_list == None: return
        self.Ack = []
        self.VZMRSCpre = self.VZMRSCcur
        self.VZMRSCcur = []
        self.VZM = []
        self.VZM_code = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.VZM_code.append([x for x in frame])
            self.Ack.append(list(map(check_Ack, frame)))
            self.VZMRSCcur.append(list(map(check_RSC, frame)))
            self.VZM.append(list(map(cal_voltage, frame)))
        if self.VZMRSCpre == None: self.VZMRSCpre = self.VZMRSCcur
        return self.VZM
    
    def get_ZM(self, ID=0xFF, rstZMPh="NoReset", clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction"):
        frame_list = self.GetData(LinxID=ID, RstZMPh=rstZMPh, ClrExeCnt=clrExeCnt, Equidist=equidist, ResetRSC=resetRSC, DataType="Zreal")
        if frame_list == None: return
        self.Ack = []
        self.ZrealRSCpre = self.ZrealRSCcur
        # print(frame_list)
        self.ZrealRSCcur = []
        self.ZrealCode = []
        self.Zreal = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Ack.append(list(map(check_Ack, frame)))
            self.ZrealRSCcur.append(list(map(check_RSC, frame)))
            self.Zreal.append(list(map(cal_ZM, frame)))            
            self.ZrealCode.append([x for x in frame])
        if self.ZrealRSCpre == None: self.ZrealRSCpre = self.ZrealRSCcur
        #----------------------------------------------------------
        frame_list = self.GetData(LinxID=ID, ClrExeCnt=clrExeCnt, Equidist=equidist, ResetRSC=resetRSC, DataType="Zimag")
        if frame_list == None: return
        self.Ack = []
        self.ZimagRSCpre = self.ZimagRSCcur
        self.ZimagRSCcur = []
        self.ZimagCode = []
        self.Zimag = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Ack.append(list(map(check_Ack, frame)))
            self.ZimagRSCcur.append(list(map(check_RSC, frame)))
            self.Zimag.append(list(map(cal_ZM, frame)))
            self.ZimagCode.append([x for x in frame])
        if self.ZimagRSCpre == None: self.ZimagRSCpre = self.ZimagRSCcur
        return self.Zreal, self.Zimag

    def get_Corrosion(self):
        return

    def get_UniqueID(self):
        frame_list = self.GetData(DataType="UniqueID1")
        if frame_list == None: return
        tmp1 = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            tmp1.append(list(map((lambda x: x[-5: -1]), frame)))
        frame_list = self.GetData(DataType="UniqueID2")
        if frame_list == None: return
        tmp2 = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            tmp2.append(list(map((lambda x: x[-5: -1]), frame)))
        frame_list = self.GetData(DataType = "UniqueID3")
        if frame_list == None: return
        tmp3 = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            tmp3.append(list(map((lambda x: x[-5 : -1]), frame)))
        frame_list = self.GetData(DataType = "UniqueID4")
        if frame_list == None: return
        tmp4 = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            tmp4.append(list(map((lambda x: x[-5 : -1]), frame)))
        self.UniqueID = []
        for i in range(len(tmp1)):
            self.UniqueID.append(list(map((lambda x, y, m, n: "0x" + x + y+ m +n ), tmp1[i], tmp2[i], tmp3[i], tmp4[i])))
        return self.UniqueID

    def get_IDXY(self):
        frame_list = self.GetData(DataType = "UniqueID4")
        if frame_list == None: return
        tmp1 = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            tmp1.append(list(map((lambda x: x[-5 : -1]), frame)))
        self.IDXY = []
        for i in range(len(tmp1)):
            self.IDXY.append(list(map((lambda x: "0x" + x), tmp1[i])))
        return self.IDXY

    def get_ATEID(self):
        frame_list = self.SetRegBank(BankAddr = 0x7B, RW = "Read")
        if frame_list == None: return
        frame_list = self.cmd("FFE0000", 1)
        if frame_list == None: return
        self.ATEID = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.ATEID.append(list(map((lambda x: "0x" + x[-5 : -1]), frame)))
        return self.ATEID

    def get_PXIID(self):
        frame_list = self.SetRegBank(BankAddr = 0x7E, RW = "Read")
        if frame_list == None: return
        frame_list = self.cmd("FFA0000", 1)
        if frame_list == None: return
        self.PXIID = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.PXIID.append(list(map((lambda x: "0x" + x[-5 : -1]), frame)))     
        frame_list = self.SetRegBank(BankAddr = 0x00)
        if frame_list == None: return
        return self.PXIID

    def get_Version(self):
        frame_list = self.GetData(DataType = "Version")
        if frame_list == None: return
        self.Version = []
        for frame in frame_list:
            if len(frame) != self.linx_num: return
            self.Version.append(list(map((lambda x: "0x" + x[-5 : -1]), frame)))
        return self.Version

##    def get_IDXY(self):
##        frame_list = self.SetRegBank(BankAddr = 0x7F, RW = "Read")
##        if frame_list == None: return
##        frame_list = self.cmd("FF00000", 1)
##        if frame_list == None: return
##        self.IDX = []
##        for frame in frame_list:
##            if len(frame) <> self.linx_num: return
##            self.IDX.append(map((lambda x: "0x" + x[-5 : -1]), frame))  
##        frame_list = self.cmd("FF10000", 1)
##        if frame_list == None: return
##        self.IDY = []
##        for frame in frame_list:
##            if len(frame) <> self.linx_num: return
##            self.IDY.append(map((lambda x: "0x" + x[-5 : -1]), frame))    
##        frame_list = self.SetRegBank(BankAddr = 0x00)
##        if frame_list == None: return
##        return self.IDX, self.IDY

    def get_MTPCRC(self):
        return

    def get_SetCRC(self):
        return

    def get_MTP(self):
        mtp_addr = 0
        print(" Bank  Address  MTP_Address     Data")
        for bank in [0x7B, 0x7C, 0x7D, 0x7E, 0x7F]:
            frame_list = self.SetRegBank(RW="Read", BankAddr=bank)
            if frame_list == None: return
            for addr in range(15):
                command = "FF" + hex(addr)[2:3] + "0000"
                frame_list = self.cmd(command, 1)
                print(" 0x%X\t0x%X\t0x%02X\t%s" %(bank, addr, mtp_addr, ", ".join(map((lambda x : "%s" %x), frame_list[0]))))
                mtp_addr += 1
                if mtp_addr > 63: break
        self.SetRegBank(RW="Write", BankAddr=0)
        return

    def cal_temp(self,frame_str = "0X00000000"):
        tmp = int(frame_str[-4 : -1], 16)
        if tmp < 0X800:
            dts = tmp/16.0
        else:
            dts = -((~(tmp & 0XFFF) & 0X7FF) + 1)/16.0       
        return dts    

# -------------------------------------------------------------------------------------------------
def check_Ack(frame_str):
    tmp = int(frame_str, 16)
    if (tmp & (1 << 23) != 0) and (tmp & (1 << 22) == 0): return 8 #GET confirmation, no pending SR
    if (tmp & (1 << 23) != 0): return 12                           #GET confirmation, pending SR
    if tmp & (1 << 22) != 0: return "CRC fails"
    if tmp & (1 << 21) != 0: return "Linx is Not Addressed"
    if tmp & (1 << 20) != 0: return "Service Request present"
    return

def check_Exe(frame_str):
    tmp = int(frame_str, 16)
    if (tmp & (1 << 23) != 0) and (tmp & (1 << 22) == 0) and (tmp & (1 << 20) != 0): return 9 #SET confirmation (cmd sent twice), no pending SR
    if (tmp & (1 << 23) != 0) and (tmp & (1 << 22) == 0): return 8                            #SET confirmation (cmd sent once), no pending SR
    if (tmp & (1 << 23) != 0) and (tmp & (1 << 20) != 0): return 13                           #SET confirmation (cmd sent twice), pending SR
    if (tmp & (1 << 23) != 0): return 12                                                      #SET confirmation (cmd sent once), pending SR
    if tmp & (1 << 22) != 0: return "CRC fails"
    if tmp & (1 << 21) != 0: return "Linx is Not Addressed"
    if tmp & (1 << 20) != 0: return "Service Request present"
    return

def check_RSC(frame_str):
    rsc = int(bin(int(frame_str, 16) & (0b11 << 20) | (0b1 << 32))[-22 : -20], 2)
    return rsc
   
def cal_voltage(frame_str):
    volt = 1.2 + 4.8 * int(frame_str[-5 : -1], 16) / (2**14 - 1)
    return volt

def cal_temperature(frame_str):
    tmp = int(frame_str[-4 : -1], 16)
    if tmp < 0X800:
        dts = tmp/16.0
    else:
        dts = -((~(tmp & 0XFFF) & 0X7FF) + 1)/16.0       
    return dts

def cal_ZM(frame_str):
    tmp = int(frame_str[-5 : -1], 16)
    if (tmp & 0XFFF) < 0X800:
        zm = 1000*1.2*(tmp & 0XFFF) * 2**((tmp >> 12) - 28) / 1.41421
    else:
        tmp_mant = (~(tmp & 0XFFF) & 0XFFF) + 1
        zm = - 1000*1.2*tmp_mant* 2**((tmp >> 12) - 28) / 1.41421
    return zm

# def ZM_code(frame_str):
#     code = frame_str[-5 : -1]
#     return code

# def set_zero(frame_str):
#     return 0

# -------------------------------------------------------------------------------------------------
import phy, time
def test():
    print("\n%s\n*%sWelcome to the program for LINX operating!%s*\n%s" %("* "*40, " "*17, " "*18, "* "*40))
    ser = phy.ser("COM62")
    chain1 = chain(ser)
    if not chain1.open(): return False
    chain1.en()
    ids=chain1.get_UniqueID()
    print(ids)
    chain1.close()
    return

if __name__ == "__main__":
    #test()
    ser = phy.ser("COM62")
    chain1 = chain(ser)
    if not chain1.open(): exit()
    print(chain1.en())
    # print chain1.get_MainDTS(ID=0xff, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction", dataType="MainDieTemp")
    # print chain1.get_GuardDTS(ID=0xff, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction",dataType="GuardDieTemp")
    # print chain1.get_Vmain(ID=0xFF, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction", sampleRate=0, dataType="MainVolt")
    # print chain1.get_Vguard(ID=0xFF, clrExeCnt="NoReset", equidist="NoReset", resetRSC="NoAction", sampleRate=0, dataType="GuardVolt")
    # print chain1.get_UniqueID()
    # print chain1.get_VZM()
    # print chain1.get_ZM()


    exit()

