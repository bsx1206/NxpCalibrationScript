'''
@since: 06/01/2022
@version: V1.0
@author: Mark.Kan
@change:
        06/01/2022 Mark.Kan
        1.    Created
'''
import sys
sys.path.append('power')
import configparser
import os
import time
import Keithley_2280S
import Rigol_DP832A


base_dir=os.path.dirname(os.path.abspath(__file__))
config=configparser.ConfigParser()
config.sections()

if config.read(os.path.join(base_dir,'setting.conf')):
    ps_enable_g = int(config.get('power setting', 'enable'))
    ps_type_g = config.get('power setting', 'type')
    ps_addr_g = config.get('power setting', 'addr')
else:
    ps_enable_g=1
    ps_type_g='Rigol_DP832A'
    ps_addr_g='USB0::0x1AB1::0x0E11::DP8B173900754::INSTR'

ps_types_g=['Keithley_2280S','Rigol_DP832A']
ps_voltage_g = 3.3
ps_current_g = 0.5
ps_voltlimit_g = 6.5
ps_currlimit_g = 1.0
ps_state_g = 0
class PS():
    def __init__(self,type=ps_type_g, addr=ps_addr_g):
        self.type = type
        self.addr = addr
        self.types = ps_types_g
        self.inlist = True
        self.enableLogPrint = True
        self.channelNum = 0
        if self.type == self.types[0]:
            self.ps = Keithley_2280S.instr(self.addr)
            self.channelNum=1
        elif self.type == self.types[1]:

            self.ps = Rigol_DP832A.instr(self.addr)
            self.channelNum=3
        else:
            self.inlist=False
            self.logprint('device not in list %s'% self.types)
            return
        self.voltage = [ps_voltage_g for i in range(self.channelNum + 1)]
        self.voltLimit = [ps_voltlimit_g for i in range(self.channelNum + 1)]
        self.current = [ps_current_g for i in range(self.channelNum + 1)]
        self.currLimit = [ps_currlimit_g for i in range(self.channelNum + 1)]
        self.state = [ps_state_g for i in range(self.channelNum + 1)]
    def open(self):
        if self.inlist:
            self.logprint('open %s'%self.type)
            return self.ps.open()
        else:
            return False
    def close(self):
        if self.inlist:
            self.logprint('close %s'%self.type)
            return self.ps.close()
        else:
            return False
    def on(self,ch=0):# 0 all output switch on
        self.logprint('power on')
        if self.type == self.types[0]:
            self.ps.output(state = "ON")
        elif self.type == self.types[1]:
            for i in range(1,self.channelNum+1) if ch==0 else range(ch,ch+1):
                self.ps.output_on(ch=i, volt=self.voltage[i], curr=self.current[i])
        else:
            return False
    def off(self,ch=0):# 0 all output switch off
        self.logprint('power off')
        if self.type == self.types[0]:
            self.ps.output(state = "OFF")
        elif self.type == self.types[1]:
            for i in range(1,self.channelNum+1) if ch == 0 else range(ch,ch+1):
                self.ps.output_off(ch=i)

        else:
            return False
    def config(self,ch=0,voltage=None,current=None,voltlimit=None,currlimit=None):
        self.logprint('power config %dmV'%(voltage))
        if self.type == self.types[0]:
            ch=1
            self.voltage[ch] = self.voltage[ch] if voltage == None else voltage/1000
            self.current[ch] = self.current[ch] if current == None else current/1000
            self.voltLimit[ch] = self.voltLimit[ch] if voltlimit == None else voltlimit/1000
            self.currLimit[ch] = self.currLimit[ch] if currlimit == None else currlimit/1000
            self.ps.source_conf(ch=ch, volt=self.voltage[ch], curr=self.current[ch], volt_prot=self.voltLimit[ch],
                                curr_prot=self.currLimit[ch])
        elif self.type == self.types[1]:
            for i in range(1,self.channelNum+1) if ch==0 else range(ch,ch+1):
                self.voltage[i] = self.voltage[i] if voltage == None else voltage/1000
                self.current[i] = self.current[i] if current == None else current/1000
                self.voltLimit[i] = self.voltLimit[i] if voltlimit == None else voltlimit/1000
                self.currLimit[i] = self.currLimit[i] if currlimit == None else currlimit/1000
                self.ps.conf(ch=i, volt=self.voltage[i], curr=self.current[i], volt_prot=self.voltLimit[i],
                             curr_prot=self.currLimit[i])
        else:
            return False
    def get_current(self,ch=1):
        self.logprint('get_current')
        if self.type == self.types[0]:
            return self.ps.meas_read(m_type="CURR", m_range=round(self.currLimit[ch]))
        elif self.type == self.types[1]:
            return self.ps.query_CURR(ch)
        else:
            return False
    def logprint(self,str):
        if self.enableLogPrint:
            print(str)

def test():
    myps = PS()
    if not myps.open():
        return
    for i in range(1,4):
        myps.config(0,i+1,3,i+2,4)
        myps.on(i)
        myps.get_current()
        time.sleep(5)
        myps.off(i)
        time.sleep(5)
    myps.config(0, 3.5, 1,5,2)
    myps.on(0)
    time.sleep(5)
    myps.off(0)
    myps.close()
if __name__ == "__main__":
    test()
