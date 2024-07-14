'''
@since: 10/02/2022
@version: V1.0
@author: Mark.Kan
@change:
        10/02/2022 Mark.Kan
        1.    Created
'''
import sys
sys.path.append('tempref')
import configparser
import os


base_dir=os.path.dirname(os.path.abspath(__file__))
config=configparser.ConfigParser()
config.sections()

if config.read(os.path.join(base_dir,'setting','setting.conf')):
    tr_enable_g = int(config.get('tempRef setting', 'enable'))
    tr_type_g = config.get('tempRef setting', 'type')
    tr_addr_g = config.get('tempRef setting', 'addr')
else:
    tr_enable_g=1
    tr_type_g='Fluke_1524'
    tr_addr_g='COM?'

tr_types_g=['Fluke_1524','Keysight_34970A']

class TR():
    def __init__(self, addr=tr_addr_g, type=tr_type_g):
        self.addr = addr
        self.type = type
        self.types = tr_types_g
        self.inlist = True
        self.enableLogPrint = True
        self.channelNum = 0
        if self.type == self.types[0]:
            import Fluke_1524
            self.tr = Fluke_1524.instr(self.addr)
            self.chNum=2
        elif self.type == self.types[1]:
            import Keysight_34970A
            self.tr = Keysight_34970A.instr(self.addr)
            self.chNum=8
        else:
            self.inlist=False
            self.logprint('device not in list %s'% self.types)
            return
    def open(self):
        self.logprint('open %s' % self.type)
        if self.type == self.types[0]:
            return self.tr.instr_open()
        elif self.type == self.types[1]:
            return self.tr.open()
        else:
            return False
    def close(self):
        self.logprint('close %s' % self.type)
        if self.type == self.types[0]:
            return self.tr.instr_close()
        elif self.type == self.types[1]:
            return self.tr.close()
        else:
            return False
    def config(self):
        if self.type == self.types[0]:  # Fluke_1524
            return True
        elif self.type == self.types[1]:  # Keysight_34970A
            self.tr.temp_conf()
            return True
        else:
            return False
    def getData(self, ch=1):
        self.logprint('getData %s' % self.type)
        if self.type == self.types[0]: # Fluke_1524
            if ch==0:
                return [self.tr.read_data(1),self.tr.read_data(2)]
            elif ch<=self.chNum:
                return self.tr.read_data(ch)
            else:
                return False
        elif self.type == self.types[1]: # Keysight_34970A
            if ch==0:
                return self.tr.data_read()
            elif ch <= self.chNum:
                return self.tr.data_read()[ch-1]
            else:
                return False
        else:
            return False
    def logprint(self,str):
        if self.enableLogPrint:
            print(str)

def test():
    tr = TR(tr_addr="COM15")
    if not tr.open(): return
    if not tr.config(): return
    print(tr.getData(1))
    tr.close()
if __name__ == "__main__":
    test()
