'''
@since: 06/01/2022
@version: V1.0
@author: Mark.Kan
@change:
        06/01/2022 Mark.Kan
        1.    Created
'''

import configparser
import os
import platform
import time
import sys
sys.path.append(r'./oven')
base_dir=os.path.dirname(os.path.abspath(__file__))
config=configparser.ConfigParser()
config.sections()
oven_types_g=['boyi', 'boyi48C', 'boyi504C']
if config.read(os.path.join(base_dir,'setting','setting.conf')):
    oven_enable_g=int(config.get('oven setting','enable'))
    oven_type_g=config.get('oven setting','type')
    oven_addr_g=config.get('oven setting','addr')
else:
    oven_enable_g=1
    oven_type_g='boyi504C'
    oven_addr_g='COM94'

class OVEN():
    def __init__(self,addr=oven_addr_g,type=oven_type_g,enable=oven_enable_g,temp=25.0,status=0):
        self.oven = None
        self.addr = addr
        self.type = type
        self.enable = enable
        self.types = oven_types_g
        self.temp = temp
        self.status = status
        self.inlist = True
        self.enableLogPrint = True
        if self.enable == False:
            return
        if self.type == 'boyi':
            import Boyi
            self.oven =Boyi.chamber(self.addr)
            self.typestr=''
        elif self.type == 'boyi48C' or self.type == 'boyi504C':
            import Boyi_B_TH_48C
            self.oven = Boyi_B_TH_48C.chamber(self.addr)
        else:
            self.inlist=False
            self.logprint('device not in list %s'% self.types)
    def open(self):
        if self.inlist:
            self.logprint('open %s'%self.type)
            return self.oven.open()
        else:
            return False
    def close(self):
        if self.inlist:
            self.logprint('close %s'%self.type)
            return self.oven.close()
        else:
            return False
    def start(self):
        self.logprint('start')
        self.status=1
        if self.type in oven_types_g:
            self.oven.set_Status(self.status)
        else:
            return False
        return True
    def stop(self):
        self.logprint('stop')
        self.status=0
        if self.type in oven_types_g:
            self.oven.set_Status(self.status)
        else:
            return False
        return True
    def setTemp(self,temp=25.0):
        self.logprint('set temp to %f' % temp)
        if self.type == 'boyi':
            self.oven.set_Mode(1)
        if self.type in oven_types_g:
            self.oven.set_TargetT(temp)
        return True
    def setTemp(self, temp=25.0, delay=0):
        self.logprint('set temp to %f' % temp)
        if self.type == 'boyi':
            self.oven.set_Mode(1)
        if self.type in oven_types_g:
            self.oven.set_TargetT(temp)
        cnt = 0
        if delay:
            while True:
                if temp == 200: break
                Toven = self.getTemp()
                if not Toven: continue
                Test_time = time.strftime("%H:%M:%S", time.localtime())
                cnt += 1
                self.logprint("%s,%.3f,%s\n" % (cnt, Toven, Test_time))
                time.sleep(15)
                if abs(Toven - temp) > 1: continue
                break
            if temp != 200:
                time.sleep(delay)
        return True
    def getTemp(self):
        self.logprint('get temp')
        if self.type in oven_types_g:
            return self.oven.get_T()
        else:
            return 0

    def logprint(self,str):
        if self.enableLogPrint:
            print(str)

def test():
    import time
    myoven = OVEN()
    print(myoven.open())
    print(myoven.start())
    print(myoven.setTemp(20))
    for i in range(1):
        print(myoven.getTemp())
        time.sleep(1)
    print(myoven.stop())
if __name__ == "__main__":
    test()
