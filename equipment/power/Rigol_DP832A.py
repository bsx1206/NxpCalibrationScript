#coding=utf-8
'''
Created on Feb 14, 2018

@author: felix.yao
'''
#:APPL? CH1

import time
import pyvisa as visa
#rsc_Rigol_DP832A   = "USB0::0x1AB1::0x0E11::DP8B173900805::INSTR"
#rsc_Rigol_DP832A   = "USB0::0x1AB1::0x0E11::DP8B173900785::INSTR"
rsc_Rigol_DP832A   = "USB0::0x1AB1::0x0E11::DP8B173900754::INSTR"
#rsc_Rigol_DP832A   = "USB0::0x1AB1::0x0E11::DP8B173900784::INSTR"
#rsc_Rigol_DP832A   = "USB0::0x1AB1::0x0E11::DP8B161750221::INSTR"

class instr(object):
    def __init__(self, rsc=rsc_Rigol_DP832A):
        self.rsc = rsc
        self.idn = "Rigol DP832A"

    def open(self):
        print("\nConnect to Rigol DP832A ......", end=' ')
        err_cnt = 0
        while True:
            try:
                self.inst = visa.ResourceManager().open_resource(self.rsc)
                self.inst.write("*RST")
                self.inst.write("*CLS")
                self.inst.write("SYST:BEEP:IMM")###???
                print("Successful!")
                # self.idn = self.inst.query("*IDN?")##identification query 
                # print self.idn
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    print("Failed!")
                    return False
                    
    def query_CURR(self,ch=1):
        ch_query = self.inst.query(":MEAS:CURR? CH%s"%ch)
        unicode_ch = ch_query[:-1]
        # print('unicode_ch',type(unicode_ch))
        # str_ch = unicode_ch.encode('unicode-escape').decode('string_escape')
        float_ch = float(unicode_ch)*1000
        return float_ch

    def query_VOL(self,ch=1):
        ch_query = self.inst.query(":MEAS? CH%s"%ch)
        unicode_ch = ch_query[:-1]
        # str_ch = unicode_ch.encode('unicode-escape').decode('string_escape')
        float_ch = float(unicode_ch)*1000
        return float_ch


    def conf(self, ch=1, volt=3.3, curr=0.5, volt_prot=6.5, curr_prot=1):
        err_cnt = 0
        while True:
            try:
                self.inst.write("INST CH%s" %ch)
                self.inst.write("VOLT %s" %volt)
                self.inst.write("VOLT:PROT %s" %volt_prot)
                self.inst.write("VOLT:PROT:STAT ON")
                self.inst.write("CURR %s" %curr)
                self.inst.write("CURR:PROT %s" %curr_prot)
                self.inst.write("CURR:PROT:STAT ON")
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False

    def output_on(self, ch=1, volt=3.3, curr=0.5):##channel voltage current
        err_cnt = 0
        while True:
            try:
                self.inst.write("INST CH%s" %ch)
                self.inst.write("VOLT %s" %volt)
                self.inst.write("CURR %s" %curr)
                self.inst.write("OUTP CH%s, ON" %ch)
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False

    def output_off(self, ch=1):
        err_cnt = 0
        while True:
            try:
                self.inst.write("OUTP CH%s, OFF" %ch)
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False

    def close(self):
        print("\nDisconnect Rigol DP832A ......", end=' ')
        err_cnt = 0
        while True:
            try:
                self.inst.write("OUTP CH1, OFF")
                self.inst.write("OUTP CH2, OFF")
                self.inst.write("OUTP CH3, OFF")
                self.inst.write("SYST:BEEP:IMM")
                self.inst.write("*CLS")
                self.inst.write("SYST:LOC")
                self.inst.close()
                print("Successful!")
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    print("Failed!")
                    return False
# -------------------------------------------------------------------------------------------------
def test():
    list=[]
    PS = instr()
    if not PS.open(): return
    curr = PS.query_CURR(1)
    print(curr)
    #vol = PS.query_VOL(1)
    #list.append(vol)
    for ch in [1, 2, 3]:
        print("Set channel %s" %ch)
        PS.conf(ch=ch, volt_prot=5, curr_prot=1)
        ''
        for volt in range(1, 6):
            print("    Output voltage(V): %s" %volt)
            PS.output_on(ch, volt)
            time.sleep(1)
        PS.output_off(ch)
    PS.close()
    return

if __name__ == "__main__":
    test()
    exit()

