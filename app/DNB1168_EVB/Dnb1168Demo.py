'''
Created on May 21, 2024

@author: Jessie.Bian
'''
import sys, os, time, json
WORK_SPACE_PATH=os.path.dirname(os.path.abspath(__file__))+'\\..\\..'
sys.path.append(WORK_SPACE_PATH+'/modules/')
from DigitalMeter import DigitalMeter
from Chamber import Chamber
from Dnb1168Dev import ChainDev
from Dnb1168Dev import RREG
import LOG

class Config():
    def __init__(self, path):
        assert os.path.exists(path)
        fp = open(path, 'r')
        _json_str = fp.read()
        self._json = json.loads(_json_str)
        fp.close()

    def _get(self, item:str):
        return (self._json[item]["Port"], self._json[item]["Type"])

    def GetMeter(self):
        return self._get("Meter")
    
    def GetChamber(self):
        return self._get("Chamber")
    
    def GetTarget(self):
        return self._get("Target")
    
    def GetIcNum(self):
        return self._json["NumberOfIC"]
    
    def GetLogObject(self):
        level = LOG.LOG_LEVEL.get(self._json["LOG"]["Level"])
        path = self._json["LOG"]["Path"]
        if isinstance(path, str):
            if False == os.path.isdir(WORK_SPACE_PATH+"\\log"):
                os.makedirs(WORK_SPACE_PATH+"\\log")
            fname = WORK_SPACE_PATH+"\\log\\" + LOG.FMT_NOW().replace(':', '.') + ".log"
            return LOG.LOG(fname, level)
        else:
            return LOG.LOG(level=level)
    
    def GetCsvObject(self):
        fpath = self._json["CSV"]["Path"]
        if None == fpath: return LOG.LOG(level=LOG.LOG_LEVEL.ALL)
        return LOG.CSV(fpath + '/' + LOG.FMT_NOW().replace(':', '.') + '.csv')
    
def Evb():
    def __init__(self):
        pass

    def CreateTitle1(count):
        titile = "Time,"
        for i in range(0, dut.GetCount()):
            title += f" Tdm_{i}, Tdg_{i}, Tcm_{i}, Tcg_{i}, Vm_{i}, Vg_{i},"
        return title[:-1]
    

if __name__ == '__main__':
    config = Config(sys.path[0]+"/config.json")
    log = config.GetLogObject()

    # port, name = config.GetMeter()
    # log.INF(f'NAME:{name}, PORT:{port}')
    # meter = DigitalMeter(port=port)

    # port, name = config.GetChamber()
    # log.INF(f'NAME:{name}, PORT:{port}')
    # chamber = Chamber(port)

    port, name = config.GetTarget()
    log.INF(f'NAME:{name}, PORT:{port}')
    ic_num = config.GetIcNum()
    assert ic_num > 0
    log.INF(f'Expect {ic_num} ICs')
    dut = ChainDev(port=port,target_ic_num=ic_num)

    csv = config.GetCsvObject()

    log.SUC("开始测试")
    # log.INF("#1. 温箱设定25度")
    # chamber.SetTemperature(25.0, 60 * 60)
    # while chamber.IsRunning():
    #     time.sleep(1)

    # log.INF("#2. 等待温箱温度稳定在25度")
    # time.sleep(30 * 60)

    log.INF("#3. 使芯片保持通信状态15分钟")
    dut.KeepAlive()
    # time.sleep(15 * 60)

    log.INF("#4. 读取温度值（TDIE_M 和 TDIE_G），（Ctg 和Ctm），（Vm和 Vg）记录原始值")
    log.INF("    循环读10次，写入表格T1。")
    # csv.Append(Evb.CreateTitle())
    for i in range(0, 10):
        l = []
        d = dut.ReadRegister(RREG.TempDieMain); l.extend(d)
        d = dut.ReadRegister(RREG.TempDieGuard); l.extend(d)
        d = dut.ReadRegister(RREG.TempCellMain); l.extend(d)
        d = dut.ReadRegister(RREG.TempCellGuard); l.extend(d)
        d = dut.ReadRegister(RREG.VoltMain); l.extend(d)
        d = dut.ReadRegister(RREG.VoltGuard); l.extend(d)
        csv.Append(payload=d, timestamp=True)
    # d = meter.Read(0)
    l.extend(d)
    csv.Blank()

    log.INF("#5. 打开均衡18.3mA")
    dut.StartBalance()

    log.INF("#6. 反复读取温度值（TDIE_M 和 TDIE_G）直到平衡")
    log.INF("    写入表格T1。")
    csv.Append(Evb.CreateTitle1())
    l = []
    d = dut.ReadRegister(RREG.TempDieMain); l.extend(d)
    d = dut.ReadRegister(RREG.TempDieGuard); l.extend(d)
    d = dut.ReadRegister(RREG.TempCellMain); l.extend(d)
    d = dut.ReadRegister(RREG.TempCellGuard); l.extend(d)
    d = dut.ReadRegister(RREG.VoltMain); l.extend(d)
    d = dut.ReadRegister(RREG.VoltGuard); l.extend(d)
    csv.Append(payload=d, timestamp=True)
    csv.Blank()
    


