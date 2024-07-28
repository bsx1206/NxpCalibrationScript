'''
Created on Feb 14, 2018

@author: felix.yao
'''

import pyvisa, time

#rsc_Keithley_2280S = "GPIB0::5::INSTR"
rsc_Keithley_2280S = "USB0::0x05E6::0x2280::4062995::0::INSTR"


class instr(object):
    def __init__(self, rsc=rsc_Keithley_2280S):
        self.rsc = rsc
        self.idn = "Keithley 2280S"

    def open(self):
        print("\nConnect to Keithley 2280S ......", end=' ')
        err_cnt = 0
        while True:
            try:
                self.inst = pyvisa.ResourceManager().open_resource(self.rsc)
                self.inst.write("*RST")
                self.inst.write("*CLS")
                print("Successful!")
                self.idn = self.inst.query("*IDN?")
                print(self.idn)
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    print("Failed!")
                    return False

    def source_conf(self, ch=1, volt=3.3, curr=0.5, volt_prot=6.5, curr_prot=1):
        err_cnt = 0
        while True:
            try:
                self.inst.write(":VOLT %s" %volt)
                self.inst.write(":CURR %s" %curr)                
                self.inst.write(":VOLT:PROT %s" %volt_prot)
                self.inst.write(":CURR:PROT %s" %curr_prot)
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    print("Failed!")
                    return False

##    def meas_conf(self, volt_range=32, curr_range=0.1, volt_res=6, curr_res=6, nplc=10):
##        err_cnt = 0
##        while True:
##            try:
##                self.inst.write(":SENS:VOLT:RANG %s" %volt_range)
##                self.inst.write(":SENS:CURR:RANG %s" %curr_range)                
##                self.inst.write(":SENS:VOLT:DIG %s" %curr_res)
##                self.inst.write(":SENS:CURR:DIG %s" %curr_res)
##                self.inst.write(":SENS:VOLT:NPLC %s" %nplc)
##                self.inst.write(":SENS:CURR:NPLC %s" %nplc)
##                return True
##            except:
##                if err_cnt < 3:
##                    err_cnt += 1
##                    time.sleep(3)
##                else:
##                    print "Failed!"
##                    return False

    def meas_read(self, m_type="CURR", m_range=0.01, m_res=6):  #Type:VOLT=V, CURR=I
        err_cnt = 0
        while True:
            try:
                meas_str = self.inst.query(":MEAS:%s? %s,%s" %(m_type,m_range,m_res))
                if m_type == "CURR":
                    meas_mant = meas_str[0:meas_str.find("E")]
                    meas_exp = meas_str[meas_str.find("E")+1:meas_str.find("A")]
                    return float(meas_mant)*(10**(float(meas_exp)))
                elif m_type == "VOLT":
                    meas_str = meas_str[meas_str.find("A,")+2:meas_str.find("V")+1]
                    meas_mant = meas_str[0:meas_str.find("E")]
                    meas_exp = meas_str[meas_str.find("E")+1:meas_str.find("V")]
                    return float(meas_mant)*(10**(float(meas_exp)))
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    print("Failed!")
                    return False

    def output(self,state = "ON"):
        err_cnt = 0
        while True:
            try:
                self.inst.write(":OUTP %s" %state)
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    print("Failed!")
                    return False
        return


    def close(self):
        print("\nDisconnect Keithley 2280S ......", end=' ')
        err_cnt = 0
        while True:
            try:
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
    PS = instr()
    if not PS.open(): return
    if not PS.source_conf():return
    if not PS.output("ON"): return
    for v in range(55,19,-10):
       if not PS.source_conf(volt=v/10.0, curr=0.1):return
       time.sleep(0.5)
       print(PS.meas_read(m_type="CURR", m_range=0.01)) 
    if not PS.output("OFF"): return
    PS.close()
    return
def test1():

    inst = pyvisa.ResourceManager().open_resource(rsc_Keithley_2280S)
    inst.write("*RST")
    inst.write("*CLS")
    idn = inst.query("*IDN?")
    print(idn)
    inst.write(":VOLT %s" % 3.3)
    inst.write(":CURR %s" %0.1)
    inst.write(":VOLT:PROT %s" %6.5)
    inst.write(":CURR:PROT %s" %1)
    inst.write(":OUTP %s" % "ON")
if __name__ == "__main__":
    test()
    exit()

