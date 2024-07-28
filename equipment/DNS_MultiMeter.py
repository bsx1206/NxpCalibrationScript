'''
@since: 06/01/2022
@version: V1.0
@author: Mark.Kan
@change:
        06/01/2022 Mark.Kan
        1.    Created
'''
import sys
sys.path.append(r'multimeter')
import configparser
import os
import time
import Keysight_3458
import Keysight_34465A
base_dir=os.path.dirname(os.path.abspath(__file__))
config=configparser.ConfigParser()
config.sections()

if config.read(os.path.join(base_dir,'setting.conf')):
    mm_enable_g = bool(int(config.get('multimeter setting', 'enable')))
    mm_type_g = config.get('multimeter setting', 'type')
    mm_addr_g = config.get('multimeter setting', 'addr')
else:
    mm_enable_g = False
    mm_type_g = 'Keysight_34465A'
    mm_addr_g = 'USB0::0x2A8D::0x0101::MY59001765::0::INSTR'

mm_types_g=['Keysight_3458','Keysight_34465A']

class MM():
    def __init__(self,type=mm_type_g, addr=mm_addr_g,enable=mm_enable_g):
        self.mm = None
        self.type = type
        self.addr = addr
        self.enable = enable
        self.types = mm_types_g
        self.inlist = True
        self.enableLogPrint = True
        if self.enable == False:
            return
        if self.type == self.types[0]:
            self.mm = Keysight_3458.instr(self.addr)
        elif self.type == self.types[1]:
            self.mm = Keysight_34465A.instr(self.addr)
        else:
            self.inlist=False
            self.logprint('device not in list %s'% self.types)
            return
    def open(self):
        if self.inlist:
            self.logprint('open %s'%self.type)
            return self.mm.open()
        else:
            return False
    def close(self):
        if self.inlist:
            self.logprint('close %s'%self.type)
            return self.mm.close()
        else:
            return False
    def config(self,Type='DCV', Range="AUTO"):
        self.logprint('config')
        if self.type == self.types[0]:
            self.mm.config(Type,Range)
        elif self.type == self.types[1]:
            if Type=='DCV':
                self.mm.DCV_conf()
            elif Type=='DCI':
                self.mm.DCI_conf()
            else:
                return False
        else:
            return False
    def get_data(self,Type='DCV'):
        self.logprint('get_data')
        if self.type == self.types[0]:
            return self.mm.data_read()
        elif self.type == self.types[1]:
            if Type=='DCV':
                return self.mm.DCV_read()
            elif Type=='DCI':
                return self.mm.DCI_read()
            else:
                return False
        else:
            return False
    def logprint(self,str):
        if self.enableLogPrint:
            print(str)

def test():
    meter = MM('Keysight_34465A','USB0::0x2A8D::0x0101::MY59001765::0::INSTR')
    if not meter.open(): return
    meter.config(Type='DCV')
    for i in range(10):
        meter.get_data(Type='DCV')
    meter.close()
if __name__ == "__main__":
    # test()
    print(bool(int('2')))
