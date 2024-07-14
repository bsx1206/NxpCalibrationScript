'''
@since: 10/02/2022
@version: V1.0
@author: Mark.Kan
@change:
        10/02/2022 Mark.Kan
        1.    Created
'''
import sys
sys.path.append('counter')
import configparser
import os


base_dir=os.path.dirname(os.path.abspath(__file__))
config=configparser.ConfigParser()
config.sections()

if config.read(os.path.join(base_dir,'setting','setting.conf')):
    cnt_enable_g = int(config.get('counter setting', 'enable'))
    cnt_type_g = config.get('counter setting', 'type')
    cnt_addr_g = config.get('counter setting', 'addr')
else:
    cnt_enable_g=1
    cnt_type_g='TF930'
    cnt_addr_g='COM?'

cnt_types_g=['TF930']

class CNT():
    def __init__(self, addr=cnt_addr_g, type=cnt_type_g):
        self.addr = addr
        self.type = type
        self.types = cnt_types_g
        self.inlist = True
        self.enableLogPrint = True
        self.channelNum = 0
        if self.type == self.types[0]:
            import TF930
            self.cnt = TF930.TF930(self.addr)
            self.chNum=2
        else:
            self.inlist=False
            self.logprint('device not in list %s'% self.types)
            return
    def open(self):
        self.logprint('open %s' % self.type)
        if self.type == self.types[0]:
            return self.cnt.open()
        else:
            return False
    def close(self):
        self.logprint('close %s' % self.type)
        if self.type == self.types[0]:
            return self.cnt.close()
        else:
            return False
    def config(self,mode='frequency'):
        if self.type == self.types[0]:  # Fluke_1524
            self.cnt.config(mode=mode)
            return True
        else:
            return False
    def readData(self, ch=1):
        self.logprint('getData %s' % self.type)
        if self.type == self.types[0]:
            return self.cnt.readData()
        else:
            return False
    def logprint(self,str):
        if self.enableLogPrint:
            print(str)

def test():
    print("1")
if __name__ == "__main__":
    test()
