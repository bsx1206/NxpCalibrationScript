'''
Created on May 21, 2024

@author: Jessie.Bian
'''
import sys, os, time, json
WORK_SPACE_PATH=os.path.dirname(os.path.abspath(__file__))+'\\..\\..'
sys.path.append(WORK_SPACE_PATH+'/modules/')
from DigitalMeter import DigitalMeter
from DigitalMeter import FlukeMeter
from DigitalMeter import CurrentMeter
from DigitalMeter import PowerSupport
from Chamber import Chamber
from Dnb1168Dev import ChainDev
from Dnb1168Dev import RREG
# from Fluke_1524 import instr
import phy
import LOG
from AutoDigitalMeter import AutoDigitalMeter


        
class Config():
    def __init__(self, path):
        assert os.path.exists(path)
        fp = open(path, 'r')
        _json_str = fp.read()
        self._json = json.loads(_json_str)
        fp.close()

    def _get1(self, item:str):
        return (self._json[item]["Port"], self._json[item]["Type"])

    def _get2(self, item:str, secondary_item:str):
        return (self._json[item][secondary_item]["Port"], self._json[item][secondary_item]["Type"])
#~~~~~~~~~~~~~~~~~~~~~~keysight_34970a~~~~~~~~~~~~~~~~~~~~~~
    def GetMeter(self, name:str):
       return self._get2("Meter", name)

    
    def GetChamber(self):
        return self._get1("Chamber")
    
    def GetTarget(self):
        return self._get1("Target")
    
    def GetIcNum(self):
        return self._json["NumberOfIC"]
    
    def GetBalanceDiff(self):
        return self._json["SETTING"]["BALANCE_DIFF_VALUE"], self._json["SETTING"]["BALANCE_KEEP_SEC"],self._json["SETTING"]["BALANCE_Off_Time"],self._json["SETTING"]["BALANCE_CURRENT"],self._json["SETTING"]["Voltagelist"],self._json["SETTING"]["Templist"],self._json["SETTING"]["BALANCE_IClist"],self._json["SETTING"]["Chamber_Wtime"]
    
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
    
    def GetCsvObject(self, posfix:str=""):
        fpath = self._json["CSV"]["Path"]
        if None == fpath: return LOG.LOG(level=LOG.LOG_LEVEL.ALL)
        return LOG.CSV(fpath + '/' + LOG.FMT_NOW().replace(':', '.') + posfix + '.csv')
    
class Evb:
    def __init__(self):
        pass

    @staticmethod
    def CreateTitle1(count:int):
        title = "Time, I, Tref1,Tref2,Balance_Value(mA),Voltage,State,"
        for i in range(1, count + 1):
            title += f" Tdm_{i}, Tdg_{i}, Tcm_{i}, Tcg_{i}, Vm_{i}, Vg_{i}, "
        return title[:-1]
    


def list_number_smaller_than(list_of_numbers,smaller_data):
    return all(num < smaller_data for num in list_of_numbers)   
 
        

    
'''
def ChamberContorl(temperature,Chamber_Wtime):
    #~~~~~~~~~~~~~~~~~~~设定x℃温箱，到达后静置5H,静置过程芯片通讯状态~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    log.INF(f"#1. 温箱设定{temperature}度")
    chamber.SetTemperature(float(temperature),30)
    while True:
        tem = chamber.GetTemperature()
        if abs(tem) >= abs(temperature):
            print(f"温度达到设定值：{tem}度")
            break
        else:
            print(f"当前温度：{tem}度")
            time.sleep(5)
    #while chamber.IsRunning():
        #   time.sleep(1)
        #if chamber.GetStatus() != "REACH": # comment for speedup test
            #log.ERR(f"chamber错误: {chamber.GetStatus()} ")
            #sys.exit(1)    
    log.INF("#2. 在温箱静置使使芯片保持通信状态分钟")
    dut.KeepAlive()
    log.INF(f"#3. 等待温箱温度稳定在{temperature}度--到达温度后静置2h")
    time.sleep(Chamber_Wtime) # comment for speedup test  
        
def ValtageContorl(Voltage):
        PowerOut.VoutOn(ch=3,Volt=Voltage,Curr=3)
        time.sleep(1)
        dut.KeepAlive()  
        #csv.Append("#4. 模组静置1H",timestamp=True)
        log.INF("#4. 模组静置1H")'''

        
def DataRecord(balance_off_time,Balancevalue,Valtage):
    csv.Append(Evb.CreateTitle1(dut.GetCount() - 1))
    tdg_before=[0,0,0]
    counter = 0
    t_start = time.time()
    c_time = time.time()
    while time.time() - t_start < balance_off_time:
    #while time.time() - t_start < 1 * 600:
        tdm = dut.ReadRegister(RREG.TempDieMain)[1:]     
        tdg = dut.ReadRegister(RREG.TempDieGuard)[1:]
        tcm = dut.ReadRegister(RREG.TempCellMain)[1:]
        tcg = dut.ReadRegister(RREG.TempCellGuard)[1:]
        vm = dut.ReadRegister(RREG.VoltMain)[1:]
        vg = dut.ReadRegister(RREG.VoltGuard)[1:]
        '''m1 = meter.Read(1)
        m2 = meter.Read(2)
        meter_current.DCImeas()
        I = meter_current.ReadAll_DCI()'''
        diff_Tdg_map =list(map(lambda x,y:x-y,tdg,tdg_before))
        
        if time.time() - c_time > 60:
            c_time = time.time()
            diff_Tdg_map =list(map(lambda x,y:x-y,tdg,tdg_before))
            result = list_number_smaller_than(diff_Tdg_map,0.15)
            tdg_before = tdg
            print(result)
            if result == True:
                counter = counter + 1
        tdg_before = tdg
                  
        
        print(diff_Tdg_map)
        
        


        m1 = 1
        m2 = 2
        I = 1
        
        csv.Append(payload=[I, m1,m2,Balancevalue,Valtage,"Balance_OFF"] + [x for y in zip(tdm,tdg,tcm,tcg,vm,vg) for x in y], timestamp=True)
        print(tdm)            

           
def BlanceContorl(ID,Balancevalue):
    log.INF(f"#5. 打开均衡{Balancevalue}mA")
    dut.StartBalanceOne(ID,Balancevalue)


def BalanceonDataRecord(Balancelist,Balance_IDlist,BALANCE_KEEP_SEC,Voltage):
    log.INF(f"设定均衡电流列表： {Balancelist} mA")
    log.INF(f"当前开启均衡IC：IC {Balance_IDlist}")
    log.INF(f"均衡保持时间：{BALANCE_KEEP_SEC}s")
    time.sleep(1)
    for Balancevalue in Balancelist:                        
        for ID in Balance_IDlist:
            log.INF(f"当前均衡电流： {Balancevalue} mA") 
            log.INF(f"当前均衡IC：IC {ID} ")                          
            log.INF(f"#5. 打开均衡{Balancevalue}mA")
            log.INF(f"均衡保持时间：{BALANCE_KEEP_SEC}s")
            dut.Normal_work()
            dut.StartBalanceOne(ID,Balancevalue)     #One_IC Blance_ON
            SR_DATA= dut.ReadRegister(RREG.SrvReqData)[1:]
            print(SR_DATA)
            DataRecord(BALANCE_KEEP_SEC,Balancevalue,Voltage)
            dut.StopBalance()

            
    
               
if __name__ == '__main__':
    
    config = Config(sys.path[0]+"/config.json")
    log = config.GetLogObject()
    
#~~~~~~~~~~~~~~~~~~~~控制板初始化~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    port, name = config.GetTarget()
    log.INF(f'NAME:{name}, PORT:{port}')
    ic_num = config.GetIcNum()
    assert ic_num > 0
    log.INF(f'Expect {ic_num} ICs')
    dut = ChainDev(port=port,target_ic_num=ic_num)  
    if dut.Enumerate() == False:
        sys.exit(1)
    '''   
#~~~~~~~~~~~~~~~~~~~~Fluke_1524初始化~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    port, name = config.GetMeter("Fluke_1524")
    log.INF(f'NAME:{name}, PORT:{port}')
    # meter = DigitalMeter(port=port)
    meter = FlukeMeter(port=port)
    
#~~~~~~~~~~~~~~~~~~~~Keysight_34465a初始化~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    port, name = config.GetMeter("Keysight_34465A")
    log.INF(f'NAME:{name}, PORT:{port}')
    # meter = DigitalMeter(port=port)
    meter_current = CurrentMeter (port=port)
    meter_current.DCIconf()
    meter_current.DCImeas()
    
#~~~~~~~~~~~~~~~~~~~~Rigol_DP832A初始化~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    port, name = config.GetMeter("Rigol_DP832A")
    log.INF(f'NAME:{name}, PORT:{port}')
    # meter = DigitalMeter(port=port)
    PowerOut = PowerSupport(port=port)
    PowerOut.Voutconf(ch=3,Volt=3.8,Curr=3,volt_prot=5, curr_prot=3)
    #PowerOut.Voutconf(ch=2,Volt=3.8,Curr=3,volt_prot=5, curr_prot=3)
    PowerOut.VoutOn(ch=3,Volt=3.8,Curr=3)
    #PowerOut.VoutOn(ch=2,Volt=3.8,Curr=3)
    port, name = config.GetChamber()
    log.INF(f'NAME:{name}, PORT:{port}')
    chamber = Chamber(port)'''   
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Blance_Parameter = config.GetBalanceDiff()
    diff_Voltage = Blance_Parameter[0]
    BALANCE_on_time = Blance_Parameter[1]
    Waittingtime = Blance_Parameter[2]
    Balance_list = Blance_Parameter[3]
    Valtage_list = Blance_Parameter[4]
    Temperature_list = Blance_Parameter[5]
    Balance_IDlist = Blance_Parameter[6]
    Chamber_Wtime = Blance_Parameter[7]


    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    log.SUC("开始测试")
    Balanceoff =0
    #dut.KeepAlive()
    #SR_DATA= dut.ReadRegister(RREG.SrvReqData)[1:]
    #print(SR_DATA)
    for temperature in Temperature_list:
        csv = config.GetCsvObject(f"({temperature}C)")
        log.INF(f"设定温度:{temperature} C")
        #ChamberContorl(temperature,Chamber_Wtime) 
        for Voltage in Valtage_list:
            log.INF(f"设定温度：{Voltage} V")  
            #ValtageContorl(Voltage)
            log.INF(f"温度静置：{Waittingtime} s")
            DataRecord(Waittingtime,Balanceoff,Voltage)
            log.INF(f"开启均衡：{BALANCE_on_time} s")
            BalanceonDataRecord(Balance_list,Balance_IDlist,BALANCE_on_time,Voltage)
            print(Voltage)
        print("V_STOP")
    print("STOP")
    log.SUC("DONE")
        
   
                 
  
                
            
    
    
     
    