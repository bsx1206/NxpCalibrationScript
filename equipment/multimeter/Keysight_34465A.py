'''
Created on Feb 14, 2018

@author: felix.yao
'''

import pyvisa, time

#rsc_Keysight_34465A = "GPIB0::26::INSTR"
#rsc_Keysight_34465A = "USB0::0x2A8D::0x0101::MY57502828::0::INSTR"
# rsc_Keysight_34465A = "TCPIP0::192.168.1.102::hislip0::INSTR"
rsc_Keysight_34465A = "USB0::0x2A8D::0x0101::MY59001765::0::INSTR"


class instr(object):
    def __init__(self, rsc=rsc_Keysight_34465A):
        self.rsc = rsc
        self.idn = "Keysight 34465A"

    def open(self):
        print("\nConnect to Keysight 34465A ......", end=' ')
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

    def DCV_conf(self):
        err_cnt = 0
        while True:
            try:
                self.inst.write("CONF:VOLT:DC")
                self.inst.write("VOLT:DC:RANG:AUTO ON")
                self.inst.query("MEAS:VOLT:DC?")
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False
    def DCV_read(self): #read = init+fetc
        err_cnt = 0
        while True:
            try:
                volt = float(self.inst.query("READ?"))                
                print("\nVolt = %s" %volt)
                return volt
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return
    def DCV_init(self):
        err_cnt = 0
        while True:
            try:
                self.inst.write("INIT")                
                return
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return
    def DCV_fetc(self):
        err_cnt = 0
        while True:
            try:
                volt = float(self.inst.query("FETC?"))                
                print("\nVolt = %s" %volt)
                return volt
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return
    def DCI_conf(self):
        err_cnt = 0
        while True:
            try:
                self.inst.write("CONF:CURR:DC")
                self.inst.write("CURR:DC:RANG:AUTO ON")
                self.inst.query("MEAS:CURR:DC?")
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False
    def DCI_read(self): #read = init+fetc
        err_cnt = 0
        while True:
            try:
                curr = float(self.inst.query("READ?"))                
                print("\nCurr = %s" %curr)
                return curr
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return
    def DCI_init(self):
        err_cnt = 0
        while True:
            try:
                self.inst.write("INIT")                
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return
    def DCI_fetc(self):
        err_cnt = 0
        while True:
            try:
                curr = float(self.inst.query("FETC?"))                
                print("\nCurr = %s" %curr)
                return curr
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return              
    def TEMP_conf(self):
        err_cnt = 0
        while True:
            try:
                self.inst.write("CONF:TEMP TC,K")
                self.inst.write("TEMP:NPLC 10")
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False
    def TEMP_meas(self):
        err_cnt = 0
        while True:
            try:
                temp = float(self.inst.query("MEAS:TEMP? TC, K"))
                print("\nTemp = %s" %temp)
                return temp
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return
    def Beeper(self):
        err_cnt = 0
        while True:
            try:
                self.inst.write("SYST:BEEP:IMM")
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    print("Failed!")
                    return False                
    def close(self):
        print("\nDisconnect Keysight 34465A ......", end=' ')
        err_cnt = 0
        while True:
            try:
                self.inst.write("*CLS")
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
    meter = instr()
    if not meter.open(): return 
    meter.DCV_conf()
    for i in range(10):
        meter.DCV_read()
    meter.close()
    return

if __name__ == "__main__":
    test()
    exit()

