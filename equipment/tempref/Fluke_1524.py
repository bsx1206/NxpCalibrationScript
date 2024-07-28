'''
Created on May 12, 2020

@author: luke.pan
'''

import time
import phy

BAUDRATE = 9600
TIMEOUT  = 0.5

class instr(phy.ser):
    def __init__(self, COM=None):
        phy.ser.__init__(self, COM)
        self.ser.baudrate = BAUDRATE
        self.ser.timeout = TIMEOUT

    def instr_open(self):
        print("\nConnect to Fluke 1524 ......", end=' ')
        err_cnt = 0
        while True:
            try:
                self.open()
                self.tx("*RST\n")
                self.tx("*CLS\n")
                print("Successful!")
                self.tx("*IDN?\n")
                time.sleep(0.5)
                self.idn = self.rx()
                print(self.idn)
                return True
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    print("Failed!")
                    return False

    def read_data(self, ch=1):
        err_cnt = 0
        while True:
            try:
                self.tx("MEAS? %s\n" %ch)
                temp = float(self.rx())
                return temp
            except:
                if err_cnt < 3:
                    err_cnt += 1
                    time.sleep(3)
                else:
                    return False
              
    def instr_close(self):
        print("\nDisconnect Fluke 1524 ......", end=' ')
        err_cnt = 0
        while True:
            try:
                self.tx("*RST\n")
                self.tx("*CLS\n")
                self.close()
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
    meter = instr("COM17")
    if not meter.instr_open(): return 
    print(meter.read_data(1))
    print(meter.read_data(2))
    meter.instr_close()
    return

if __name__ == "__main__":
    test()
    exit()

