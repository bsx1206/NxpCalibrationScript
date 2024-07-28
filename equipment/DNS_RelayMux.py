'''
@since: 10/02/2022
@version: V1.0
@author: Mark.Kan
@change:
        10/02/2022 Mark.Kan
        1.    Created
'''
import sys
sys.path.append(r'./mux')
import configparser
import os
import platform
import time

base_dir=os.path.dirname(os.path.abspath(__file__))
config=configparser.ConfigParser()
config.sections()

if config.read(os.path.join(base_dir,'setting','setting.conf')):
    mux_enable_g = int(config.get('mux setting', 'enable'))
    mux_type_g = config.get('mux setting', 'type')
    mux_addr_g = config.get('mux setting', 'addr')
else:
    mux_enable_g=1
    mux_type_g='MUX_V10'
    mux_addr_g='COM3'

mux_types_g=['MUX_V10']

class MUX():
    def __init__(self, addr=mux_addr_g, type=mux_type_g):
        self.addr = addr
        self.type = type
        self.types = mux_types_g
        self.inlist = True
        self.enableLogPrint = True
        self.channelNum = 0
        if self.type == self.types[0]:
            import MUX_V10
            self.mux = MUX_V10.ser(self.addr)
        else:
            self.inlist=False
            self.logprint('device not in list %s'% self.types)
            return
    def open(self):
        if self.inlist:
            self.logprint('open %s'%self.type)
            return self.mux.open()
        else:
            return False
    def close(self):
        if self.inlist:
            self.logprint('close %s'%self.type)
            return self.mux.close()
        else:
            return False
    def sw(self,ch=1):
        self.logprint('switch to channel %d'%ch)
        if self.type in self.types[0:1]:
            self.mux.Relay_Switch(ch)
        else:
            return False
    def set_SwDelay(self,ms=100):# 0 all output switch off
        self.logprint('Set switch delay %d'%ms)
        if self.type in self.types[0:1]:
            self.mux.Relay_Delay(ms)
        else:
            return False
    def logprint(self,str):
        if self.enableLogPrint:
            print(str)

def test():
    MUX_Board = MUX(addr="COM3")
    if not MUX_Board.open(): return
    MUX_Board.set_SwDelay(1000)
    #for i in range(1, 17):
        #MUX_Board.sw(i)
        #time.sleep(2)
    MUX_Board.sw(3)
    MUX_Board.close()
if __name__ == "__main__":
    test()
