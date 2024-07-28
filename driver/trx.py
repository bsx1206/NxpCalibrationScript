'''
Created on Feb 14, 2017
Update on Dec 11, 2020
Update on Feb 28, 2022

@author: felix.yao
@update: luke.pan
@update: Mark.Kan -- update to fit the requirement of  MRA4 samples

'''

import reg, phy
import time

en_ErrMsg = [   "Error : command not recognized.",
                "Error: can't",
                "Error: incorrect",
                "000 Linxs found"
                ]

cmd_ErrMsg = [  "Error : command not recognized.",
                "ERROR: NO DEVICE ENUMERATED.",
                "Error: can't",
                "Error: incorrect",
                "000 Linxs found",
                "No response",
                "Zero response",
                "CRC error",
                "Discover new linx"
                ]
#"Sequence error"

class trx(object):
    def __init__(self, phy):
        self.phy = phy
        self.linx_num = 0
#         self.linx_list = []
#         self.linx_config = []
#         self.linx_VM_Guard = []
#         self.linx_VM_Main = []
#         self.linx_CS_Guard = []
#         self.linx_CS_Main = []
#         self.linx_ZM = []
#         self.linx_TM = []
#         self.linx_BAL = []


    def en(self):
        print("\n >>> Enumerate ...", end=' ')
        err_cnt = 0
        while True:
            self.phy.tx("en 3\n" )
            time.sleep(10)
            rx_buf = self.phy.rx()
            # if "Waiting for 100ms to switch to bottom SPI interface" in rx_buf:
            #     time.sleep(1)
            #     rx_buf=self.phy.rx()
            err = list(map((lambda x : x in rx_buf), en_ErrMsg))
            if True in err:
                err_cnt += 1
                if err_cnt >= 3:
                    print("Failed")
                    # print(rx_buf)
                    return False
            else:
                try:
                    # print (rx_buf)
                    self.linx_num = int(rx_buf.split(", ")[-1].split(" ")[0])
                    #self.linx_num-=1
                    if self.linx_num <= 0:
                        print("Failed\n No LINX found!")
                        return False
                    print("Successful\n%s LINX found.\n" %self.linx_num)
                    return True
                except:
                    return False

    def cmd(self, command, repeat):
        cmd_str = "RT %s %s" %(command, repeat) if repeat > 1 else "RT %s" %(command)
##        print cmd_str
        miss_cnt = 0
        self.phy.tx(cmd_str + "\n")
        while True:
            rx_buf = self.phy.rx()
            # print rx_buf
            if "--- End of transaction ---" not in rx_buf:
                miss_cnt +=1
                if miss_cnt > 10:
                    #print(rx_buf)
                    return
                else: continue
            else: break
        err = list(map((lambda x : x in rx_buf), cmd_ErrMsg))
        if True in err:
            # print(rx_buf)
            return
        else:
            if rx_buf.count("<==") != repeat:
                #print(rx_buf)
                #print(rx_buf.count("<=="))
                return
            conf_buf = []
            while rx_buf.count("<==") >0:
                rx_tmp = rx_buf[rx_buf.find("<==")+3 : rx_buf.find("--- End of transaction ---")]
                rx_tmp = rx_tmp.replace("\t", "").replace("\r\n", ", ")
                rx_frame = []
                while "0x" in rx_tmp:
                    rx_frame.append(rx_tmp[rx_tmp.find("0x"): rx_tmp.find("0x")+10])
                    rx_tmp = rx_tmp.replace("0x", "", 1)
                if rx_frame != []: conf_buf.append(rx_frame)
                rx_buf = rx_buf.replace("<==", "", 1)
                rx_buf = rx_buf.replace("--- End of transaction ---", "", 1)
            return conf_buf if conf_buf != [] else None

#---No error detection
    def cmd2(self, command, repeat):
        cmd_str = "RT %s %s" %(command, repeat) if repeat > 1 else "RT %s" %(command)
        miss_cnt = 0
        self.phy.tx(cmd_str + "\n")
        time.sleep(0.5)
        while True:
            rx_buf = self.phy.rx()
            if (rx_buf.count(">>>") != repeat):
                miss_cnt +=1
                if miss_cnt > 10:
                    # print(rx_buf)
                    return
                else: continue
            else: break
        conf_buf = []
        while rx_buf.count("<==") >0:
            rx_tmp = rx_buf[rx_buf.find("<==")+3 : rx_buf.find("--- End of transaction ---")]
            rx_tmp = rx_tmp.replace("\t", "").replace("\r\n", ", ")
            rx_frame = []
            while "0x" in rx_tmp:
                rx_frame.append(rx_tmp[rx_tmp.find("0x"): rx_tmp.find("0x")+10])
                rx_tmp = rx_tmp.replace("0x", "", 1)
            if rx_frame != []: conf_buf.append(rx_frame)
            rx_buf = rx_buf.replace("<==", "", 1)
            rx_buf = rx_buf.replace("--- End of transaction ---", "", 1)
        return conf_buf if conf_buf != [] else None                  
# -----------------------------------------------------------------------------
    def Enumerate(self, LinxID=0x00, WriteMTP="NoWrite",ContClk="Enable", SplitBus="Disable", IgnoreBcast="Listen",
                  SetID = None, repeat=2):
        if SetID == None: SetID = self.linx_num + 1
        cmd_type = reg.register["Enumerate"]
        cmd_data = reg.Enumerate["WriteMTP"][WriteMTP] + \
                   reg.Enumerate["ContClk"][ContClk] + \
                   reg.Enumerate["SplitBus"][SplitBus] + \
                   reg.Enumerate["IgnoreBcast"][IgnoreBcast] + \
                   reg.Enumerate["SetID"](SetID)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def Initialise(self, LinxID=0xFF, WriteMTP="NoWrite", Time2Mute="Disable",ReloadMTP="NoReload", EnSrvReq="Disable",
                   ResetID="NoReset", AutoStb="NoAutoStb", NrOfLinxes = None, repeat=2):
        if NrOfLinxes == None: NrOfLinxes = self.linx_num
        cmd_type =  reg.register["Initialise"]
        cmd_data =  reg.Initialise["WriteMTP"][WriteMTP] + \
                    reg.Initialise["Time2Mute"][Time2Mute] + \
                    reg.Initialise["ReloadMTP"][ReloadMTP] + \
                    reg.Initialise["EnSrvReq"][EnSrvReq] + \
                    reg.Initialise["ResetID"][ResetID] + \
                    reg.Initialise["AutoStb"][AutoStb] + \
                    reg.Initialise["NrOfLinxes"](NrOfLinxes)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)
    
    def SetMTPLockKey(self, LinxID=0xFF, MTPLockKey = 0x0035, repeat=2):
        cmd_type = reg.register["SetMTPLockKey"]
        cmd_data = reg.SetMTPLockKey["MTPLockKey"](MTPLockKey)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)
    
    def SetThVolt(self, LinxID=0xFF, ThOver=255, ThUnder=0, repeat=2):
        cmd_type = reg.register["SetThVolt"]
        cmd_data = reg.SetThVolt["ThOver"](ThOver) + \
                   reg.SetThVolt["ThUnder"](ThUnder)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)
    
    def SetThTemp(self, LinxID=0xFF, ThOver=255, ThUnder=0, repeat=2):
        cmd_type = reg.register["SetThTemp"]
        cmd_data = reg.SetThTemp["ThOver"](ThOver) + \
                   reg.SetThTemp["ThUnder"](ThUnder)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)
    def SetGPIO_ConfDly(self, LinxID=0xFF, GPIO2_modeSPI="Input", GPIO1_modeSPI="Input", GPIO2_mode="Input",
                        GPIO1_mode="Input",NrOfLinxesInBottomChain=None,repeat=2):
        cmd_type = reg.register["SetGPIO_ConfDly"]
        cmd_data = reg.SetGPIO_ConfDly["GPIO2_modeSPI"][GPIO2_modeSPI] + \
                   reg.SetGPIO_ConfDly["GPIO1_modeSPI"][GPIO1_modeSPI] + \
                   reg.SetGPIO_ConfDly["GPIO2_mode"][GPIO2_mode] + \
                   reg.SetGPIO_ConfDly["GPIO1_mode"][GPIO1_mode] + \
                   reg.SetGPIO_ConfDly["NrOfLinxesInBottomChain"](NrOfLinxesInBottomChain)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)
    def SetZMCurr(self, LinxID=0xFF, EnZM="Stop", EnXCS="Internal", HiPass="1x",
                  TimeOut=255, repeat=2):
        cmd_type = reg.register["SetZMCurr"]
        cmd_data = reg.SetZMCurr["EnZM"][EnZM] + \
                   reg.SetZMCurr["EnXCS"][EnXCS] + \
                   reg.SetZMCurr["HiPass"][HiPass] + \
                   reg.SetZMCurr["TimeOut"](TimeOut)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def SetZMFreq(self, LinxID=0xFF, Freq_spread="Disable",WinEn="Disable", Fexponent=0, Fmantissa=0, repeat=2):
        cmd_type = reg.register["SetZMFreq"]
        cmd_data = reg.SetZMFreq["Freq_spread"][Freq_spread] + \
                   reg.SetZMFreq["WinEn"][WinEn] + \
                   reg.SetZMFreq["Fexponent"](Fexponent) + \
                   reg.SetZMFreq["Fmantissa"](Fmantissa)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def SetBalCurr(self, LinxID=0xFF, EnBal="Stop", Current=0, TimeOut=0, repeat=2):
        cmd_type = reg.register["SetBalCurr"]
        cmd_data = reg.SetBalCurr["EnBal"][EnBal] + \
                   reg.SetBalCurr["Current"](Current) + \
                   reg.SetBalCurr["TimeOut"](TimeOut)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def SetBalVolt(self, LinxID=0xFF, BalMode="Disable", BalVolt=0, repeat=2):
        cmd_type = reg.register["SetBalVolt"]
        cmd_data = reg.SetBalVolt["BalMode"][BalMode] + \
                   reg.SetBalVolt["BalVolt"](BalVolt)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def SetSRMask(self, LinxID=0xFF, CmdErr="NoMask", ClockErr="NoMask", IntErr="NoMask",
                  GPIOErr="NoMask", InvalidLockKey="NoMask", OpenWire="NoMask", ZMADCErr="NoMask",
                  BalZMDone="NoMask", CurrErr="NoMask", LDOOoR="NoMask",
                  TempADCErr="NoMask", CellTempErr="NoMask", VMADCErr="NoMask", CellVoltErr="NoMask",
                  BrownOut="NoMask", repeat = 2):
        cmd_type = reg.register["SetSRMask"]
        cmd_data = reg.SetSRMask["CmdErr"][CmdErr] + \
                   reg.SetSRMask["ClockErr"][ClockErr] + \
                   reg.SetSRMask["IntErr"][IntErr] + \
                   reg.SetSRMask["GPIOErr"][GPIOErr] + \
                   reg.SetSRMask["InvalidLockKey"][InvalidLockKey] + \
                   reg.SetSRMask["OpenWire"][OpenWire] + \
                   reg.SetSRMask["ZMADCErr"][ZMADCErr] + \
                   reg.SetSRMask["BalZMDone"][BalZMDone] + \
                   reg.SetSRMask["CurrErr"][CurrErr] + \
                   reg.SetSRMask["LDOOoR"][LDOOoR] + \
                   reg.SetSRMask["TempADCErr"][TempADCErr] + \
                   reg.SetSRMask["CellTempErr"][CellTempErr] + \
                   reg.SetSRMask["VMADCErr"][VMADCErr] + \
                   reg.SetSRMask["CellVoltErr"][CellVoltErr] + \
                   reg.SetSRMask["BrownOut"][BrownOut]
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def SetMode(self, LinxID=0xFF, OperatingMode="Normal", repeat=2):
        cmd_type = reg.register["SetMode"]
        cmd_data = reg.SetMode["OperatingMode"][OperatingMode]
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def SetForceErr(self, LinxID=0xFF, GPIO="Disable",VDRcomp="Disable", OpenWire="Disable", UTOT="Disable", DTScomp="Disable",
                    UVOV="Disable", VMcomp="Disable",LDOfsm="Disable", GLDOAna="Disable", GLDODig="Disable",
                    GLDOPll="Disable", MLDOAna="Disable", MLDOBal="Disable", repeat=2):
        cmd_type = reg.register["SetForceErr"]
        cmd_data = reg.SetForceErr["GPIO"][GPIO] + \
                   reg.SetForceErr["VDRcomp"][VDRcomp] + \
                   reg.SetForceErr["OpenWire"][OpenWire] + \
                   reg.SetForceErr["UTOT"][UTOT] + \
                   reg.SetForceErr["DTScomp"][DTScomp] + \
                   reg.SetForceErr["UVOV"][UVOV] + \
                   reg.SetForceErr["VMcomp"][VMcomp] + \
                   reg.SetForceErr["LDOfsm"][LDOfsm] + \
                   reg.SetForceErr["GLDOAna"][GLDOAna] + \
                   reg.SetForceErr["GLDODig"][GLDODig] + \
                   reg.SetForceErr["GLDOPll"][GLDOPll] + \
                   reg.SetForceErr["MLDOAna"][MLDOAna] + \
                   reg.SetForceErr["MLDOBal"][MLDOBal]
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def GetStatus(self, LinxID=0xFF, StatusType="GeneralStatus", repeat=1):
        cmd_type = reg.register["GetStatus"]
        cmd_data = reg.GetStatus["StatusType"][StatusType]
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def GetData(self, LinxID=0xFF, RstZMPh="NoReset", ClrExeCnt="NoReset", Equidist="Reset", ResetRSC="NoAction", SampleRate=0, 
                DataType="MainVolt", repeat=1):
        cmd_type = reg.register["GetData"]
        cmd_data = reg.GetData["RstZMPh"][RstZMPh] + \
                   reg.GetData["ClrExeCnt"][ClrExeCnt] + \
                   reg.GetData["Equidist"][Equidist] + \
                   reg.GetData["ResetRSC"][ResetRSC] + \
                   reg.GetData["SampleRate"](SampleRate) + \
                   reg.GetData["DataType"][DataType]
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

    def SetRegBank(self, LinxID=0xFF, RW="Write", BankAddr=0x00, repeat=2):
        cmd_type = reg.register["SetRegBank"]
        cmd_data = reg.SetRegBank["RW"][RW] +\
                    reg.SetRegBank["BankAddr"](BankAddr)
        command = "%02X%X%04X" %(LinxID, cmd_type, cmd_data)
        return self.cmd(command, repeat)

# -------------------------------------------------------------------------------------------------
def test():
    import phy
    ser = phy.ser("COM26")
    if not ser.open(): return
    linx = trx(ser)
    print(linx.en())
    print("\n Enumerate(00h)")
    print(linx.Enumerate())
    print("\n Initialise(01h)")
    print(linx.Initialise())
    print("\n SetTheVolt(03h)")
    print(linx.SetThVolt())
    print("\n SetTheTemp(04h)")
    print(linx.SetThTemp())
    print("\n SetZMCurr(06h)")
    print(linx.SetZMCurr())
    print("\n SetZMFreq(07h)")
    print(linx.SetZMFreq())
    print("\n SetBalCurr(08h)")
    print(linx.SetBalCurr())
    print("\n SetBalVolt(09h)")
    print(linx.SetBalVolt())
    print("\n SetSRMask(0Ah)")
    print(linx.SetSRMask())
    print("\n SetMode(0Bh)")
    print(linx.SetMode())
    print("\n SetForceErr(0Ch)")
    print(linx.SetForceErr())
    print("\n GetStatus(0Dh)")
    print(linx.GetStatus())
    print("\n GetData(0Eh)")
    print(linx.GetData())

    print("\n")
    for i in range(50):
        print("GetData LoopTest")
        print("%s: %s" %(i, linx.GetData()))
    return


def mytest():
    ser = phy.ser("COM26")
    if not ser.open(): return
    linx = trx(ser)
    if not linx.en() : return

    linx.Enumerate(LinxID=0x00, WriteMTP="NoWrite", SplitBus="Enable", IgnoreBcast="Listen",
                  SetID = None, repeat=2)
    #linx.Initialise(LinxID=0xFF, WriteMTP="NoWrite", ReloadMTP="NoReload", EnSrvReq="Disable", GenPOR="Generate",ResetID="NoReset", AutoStb="NoAutoStb", NrOfLinxes = None, repeat=2)
    for i in range(0,1,1):
        time.sleep(1)
        testid=0xff
        #print linx.SetMode(LinxID=testid, GPIO2="ActLow", GPIO1="ActLow", OperatingMode="Normal", repeat=2)

        linx.SetThTemp(LinxID=testid, ThOver=0x7f, ThUnder=0x80, repeat=2)
        linx.SetThVolt(LinxID=testid, ThOver=0xff, ThUnder=0x00, repeat=2)
        print(linx.GetData(LinxID=testid, RstZMPh="NoReset", ClrExeCnt="NoReset", Equidist="Reset", ResetRSC="NoAction",
                         SampleRate=0, DataType="MainVolt", repeat=1))

        print(linx.GetStatus(LinxID=testid, StatusType="GeneralStatus",repeat=1))
        testgetstatus=0
        if testgetstatus:
            for i in list(reg.GetStatus["StatusType"].keys()):
                print(i, reg.GetStatus["StatusType"][i])
                print(linx.GetStatus(LinxID=testid, StatusType=i,repeat=1))
        testsetmode=0
        if testsetmode:
            print(linx.SetMode(LinxID=0xff, GPIO2="ActLow", GPIO1="ActLow", OperatingMode="Standby", repeat=2))
            time.sleep(1)
            print(linx.GetStatus(LinxID=0xff, StatusType="GeneralStatus", repeat=1))

            time.sleep(1)
            print(linx.GetStatus(LinxID=0xff, StatusType="GeneralStatus", repeat=1))
            print(linx.GetStatus(LinxID=0xff, StatusType="GeneralStatus", repeat=1))

        print("\n")
if __name__ == "__main__":
    test()
    # mytest()
    exit()

