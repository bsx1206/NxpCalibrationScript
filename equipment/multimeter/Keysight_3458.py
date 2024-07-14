'''
Created on Dec 2, 2019

@author: luke.pan
'''

import time
import pyvisa as visa
rsc_Keysight_3458A  = "GPIB4::22::INSTR"


class instr(object):
    def __init__(self, rsc=rsc_Keysight_3458A):
        self.rsc = rsc
        self.idn = "Keysight 3458A"

    def open(self):
        print("\nConnect to Keysight 3458A ......", end=' ')
        err_cnt = 0
        while True:
            # try:
            if 1:
                self.inst = visa.ResourceManager().open_resource(self.rsc)
                self.inst.write("RESET")
                self.inst.write("CSB")
                self.inst.write("END")
                print("Successful!")
                self.idn = self.inst.query("ID?")
                print(self.idn)
                return True
            # except:
            #     if err_cnt < 10:
            #         err_cnt += 1
            #         time.sleep(3)
            #     else:
            #         print "Failed!"
            #         return False

    def conf(self, Type="DCV", Range="AUTO", Resolution="", Integrate = "10", NDIG = "8"):
        err_cnt = 0
        while True:
            try:
                self.inst.write("FUNC " + Type + "," + Range + "," + Resolution)
                self.inst.write("NPLC " + Integrate)
                self.inst.write("NDIG " + NDIG)
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False
                
    def data_read(self,Delay = None):
        err_cnt = 0
        while True:
            try:
                data = float(self.inst.query(message="MEM", delay=Delay))                        
                return data
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(2)
                else:
                    return False
                
    def close(self):
        print("\nDisconnect Keysight 3458A ......", end=' ')
        err_cnt = 0
        while True:
            try:
                self.inst.write("CSB")
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
    meter.conf(Type="DCV",Integrate="50")
    for i in range(0,20):
        data = meter.data_read()
        time.sleep(0.2)
        print(data)
    return

if __name__ == "__main__":
    test()
    exit()

