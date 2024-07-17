
import sys, os, time
from enum import Enum
WORK_SPACE_PATH=os.path.split(os.path.realpath(__file__))[0]+r'/../..'
sys.path.append(WORK_SPACE_PATH+'/driver/')
sys.path.append(WORK_SPACE_PATH+'/equipment/')
sys.path.append(WORK_SPACE_PATH+'/equipment/power/')
sys.path.append(WORK_SPACE_PATH+'/equipment/oven')
sys.path.append(WORK_SPACE_PATH+'/equipment/mux')
sys.path.append(WORK_SPACE_PATH+'/equipment/multimeter')
sys.path.append(WORK_SPACE_PATH+'/equipment/tempref')
sys.path.append(WORK_SPACE_PATH+'/equipment/counter')
sys.path.append(WORK_SPACE_PATH+'/modules/')
import phy, api, reg
import LOG

class ReadRegTable(Enum):
    TempDieGuard  = 0xFFE2005
    TempDieMain   = 0xFFE2004
    TempCellGuard = 0xFFE2003
    TempCellMain  = 0xFFE2002
    VoltGuard     = 0xFFE2001
    VoltMain      = 0xFFE2000

class ChainDev:
    def __init__(self, name = "ChainDev", port = "COM1", target_ic_num = 1):
        self._name = name
        self._port = port
        self._phy = phy.ser(port)
        self._obj = api.chain(self._phy)
        self._is_open = False
        self._enum_ic_num = 0
        self._target_ic_num = target_ic_num

    def Open(self):
        self._obj.open()
        self._is_open = True
        self._enum_ic_num = 0
        self.Initialize()

    def GetCount(self):
        return self._enum_ic_num

    def Close(self):
        self._obj.close()
        self._is_open = False

    def Initialize(self):
        if self._is_open == False:
            LOG.ERR("%s not open" % self._name)
            return False
        self._phy.tx('cc 0\n',delay=0.1)
        self._phy.tx('slp 15000\n',delay=0.1)
        self._phy.tx('snp 15000\n',delay=0.1)
        self._phy.tx('ssp 15000\n',delay=0.1)
        self._phy.tx('stp 15000\n',delay=0.1)
        self._phy.tx('sdp 15000\n',delay=0.1)
        self._phy.tx('sdi 70\n',delay=0.1)
        self._phy.tx('mut 80\n',delay=0.1)
        self._phy.tx('sdd FFD0002\n',delay=0.1)
        self._phy.tx('sdc 0\n',delay=0.1)
        self._enum_ic_num = 0
        return True
    
    def Enumerate(self):
        self._enum_ic_num = 0
        retry_count = 5
        for retry_times in range(0, retry_count):
            LOG.INF("%s try enumerating... %d/%d" % (self._name, retry_times + 1, retry_count))
            self._obj.en()
            if self._obj.linx_num >= self._target_ic_num:
                self._enum_ic_num = self._obj.linx_num
                self._obj.Initialise()
                self._UID = self._obj.get_UniqueID()[0]
                assert len(self._UID) == self._enum_ic_num
                return True
        LOG.ERR("%s not enough enumerated IC %d/%d" % (self._name, self._obj.linx_num, self._target_ic_num))
        return False
    
    def GetUID(self):
        assert None != self._UID
        return self._UID
    
    def ReadRegister(self, reg:ReadRegTable, repeat = 1):
        assert reg in ReadRegTable
        fmt_reg = f'{reg.value:07X}'
        retry_count = 5
        for retry_times in range(0, retry_count):
            DTS = self._obj.cmd2(fmt_reg, repeat)
            if len(DTS) == repeat and len(DTS[0]) == self._enum_ic_num:
                return DTS[0] if repeat == 1 else DTS
        return None
    
    def KeepAlive(self, delay_sec = 15 * 60):
        self._phy.tx
    
    def StopBalance(self):
        code=0xFF80000
        self._phy.tx(f"RT {code:07X} 2\n")
    
    def StartBalance(self, current_ma:float, delay_sec:int = sys.maxsize):
        current_bias = 5.0 # mA
        current_lsb = 13.3 # mA
        current_max_raw = (1 << 4) - 1 # bit[11:8]
        current_shift = 8
        current_raw = int(round((current_ma - current_bias)/current_lsb))
        assert current_raw <= current_max_raw and current_raw > 0
        current_raw <<= current_shift

        delay_lsb = 134 # seconds
        delay_max_raw = (1 << 8) - 1 # bit[7:0]
        delay_shift = 0
        delay_raw = int(round(delay_sec/delay_lsb))
        # assert delay_raw <= delay_max_raw
        delay_raw = delay_max_raw if delay_raw > delay_max_raw else delay_raw
        delay_raw <<= delay_shift

        code = 0xFF81000 | current_raw | delay_raw
        self._phy.tx(f"RT {code:07X} 2\n")

        return True
    
    def WriteRth(self, ic_id, Rth_values):
        self._phy.tx("RT FF20000 2\n")
        time.sleep(0.5)
        self._phy.tx("RT FFF006E 2\n")
        time.sleep(0.5)
        Rth_values_w=0
        for ID in ic_id:
            if  int(ID)<16:
                ID = hex(int(ID))
                ID = str("0"+str(ID[2:3]))
            else:
                ID = hex(int(ID))
                ID = str(ID[2:4])
            command = "RT " + str(ID) + "800" + str(Rth_values[Rth_values_w]) + " 2\n"
            #print(command)
            self._phy.tx(command)
            Rth_values_w=Rth_values_w+1
            time.sleep(0.5)
        self._phy.tx("RT FFF0000 2\n")
        time.sleep(0.5)
        self._phy.tx("RT FF13300 2\n")
        time.sleep(0.5)
    
if __name__ == '__main__':
    cdev = ChainDev(port='COM27', target_ic_num=3)
    cdev.Open()
    if False == cdev.Enumerate():
        LOG.ERR("Fail to enumerate")
        sys.exit(1)
    LOG.INF("%d ICs enumerated" % cdev.GetCount())
    LOG.INF("UID:" + str(cdev.GetUID()))
    for r in ReadRegTable:
        d = cdev.ReadRegister(r)
        LOG.INF(f"{r}: {d}")
    cdev.StartBalance(current_ma=18, delay_sec=130)
    cdev.StopBalance()
    cdev.Close()
    LOG.SUC("Test Done")