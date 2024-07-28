import time
import phy

BAUDRATE = 115200
TIMEOUT  = 0.5

class TF930(phy.ser):
    def __init__(self, COM=None):
        phy.ser.__init__(self, COM)
        self.ser.baudrate = BAUDRATE
        self.ser.timeout = TIMEOUT
    def open(self):
        try:
            phy.ser.open(self)
            self.tx("*IDN?\r\n")
            print(self.rx())
            self.tx("*RST?\r\n")
            return True
        except:
            print("<Error!>: COM port open failed!\n")
            return False
    #F2 - A frequency; F1 - A Period; F7 - A Count; F9 - A duty cycle; F8 Ratio H:L
    def config(self, mode='frequency'):
        if mode=='frequency':
            modeStr='F2'
        elif mode=='dutyCycle':
            modeStr='F9'
        elif mode=='count':
            modeStr='F7'
        self.tx("%s\r\n"%(modeStr))
        self.tx("DC\r\n")
        self.tx("Z1\r\n")
        self.tx("A1\r\n")
        self.tx("FI\r\n")
        self.tx("M1\r\n")
    def readData(self):
        self.tx('?\r\n')
        rxStr = self.rx()
        if rxStr != '':
            return float(rxStr[:-4])
        else:
            return 0.0
    def close(self):
        self.tx('STOP\r\n')
        phy.ser.close(self)


# -------------------------------------------------------------------------------------------------
def test():
    te = TF930("COM6")
    if not te.open():
        print("error open")
        return
    te.config(mode='frequency')
    count=5
    while count!=0:
        count-=1
        print(te.readData())
        time.sleep(0.1)
    te.close()
if __name__ == "__main__":
    test()

    exit()
