'''
Created on Dec 2, 2019

@author: luke.pan
'''

import pyvisa, time

rsc_Keysight_34970  = "GPIB4::3::INSTR"


class instr(object):
    def __init__(self, rsc=rsc_Keysight_34970):
        self.rsc = rsc
        self.idn = "Keysight 34970"

    def open(self):
        print("\nConnect to Keysight 34970 ......")
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

    def volt_conf(self, Type="DC", Range="AUTO", Resolution="1E-6", Integrate = "10",
                  Channels="(@101, 102, 103, 104, 105, 106, 107, 108)"):
        err_cnt = 0
        while True:
            try:
                self.inst.write("CONF:VOLT:" + Type + " " + Range + "," + Resolution + "," + Channels)
                self.inst.write("SENS:VOLT:" + Type + ":NPLC "+ Integrate + ","+ Channels)
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False

    def temp_conf(self, Sensor="TC", Type="J", Unit="C",
                  Channels="(@101, 102, 103, 104, 105, 106, 107, 108)"):
        err_cnt = 0
        while True:
            try:
                print("CONF:TEMP " + Sensor + "," + Type + "," + Channels)
                self.inst.write("CONF:TEMP " + Sensor + "," + Type + "," + Channels)
                print("UNIT:TEMP " + Unit + "," + Channels)
                self.inst.write("UNIT:TEMP " + Unit + "," + Channels)

                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False
                
    def data_read(self,Delay = None):
        err_cnt = 0
        data = []
        while True:
            try:
                tmp = self.inst.query(message="READ?", delay=Delay)
                while "," in tmp:
                    data.append(float(tmp[0:tmp.find(",")]))
                    tmp = tmp[tmp.find(",")+1:]
                data.append(float(tmp))                                  
                return data
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False
                
    def close(self):
        print("\nDisconnect Keysight 34970 ......")
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
    meter.temp_conf(Channels="(@101, 102, 103, 104)")
##    for dly in range(0,20):
    data = meter.data_read(1)
    print(data)
    meter.close()
    return

def test1():
    meter = instr()
    if not meter.open():
        print("error open meter")
        return
    # meter.temp_conf()
    meter.temp_conf(Channels="(@301, 302, 303, 304, 305, 306, 307, 308)")
    count=10
    while count>0:
        count -= 1
        Test_time = time.strftime("%H:%M:%S", time.localtime())
        data = meter.data_read(1)
        print(data,Test_time)
        # time.sleep(1)
def test2():
    inst = pyvisa.ResourceManager().open_resource(rsc_Keysight_34970)
    print(inst.query("*IDN?"))
if __name__ == "__main__":
    test1()
    exit()

