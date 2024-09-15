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
import numpy as np

        
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
        title = "Time,"
        for i in range(1, count + 1):
            title += f" Tdg_{i},Vm_{i}, Vg_{i}, "
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
    t_start = time.time()
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
        m1 = 1
        m2 = 2
        I = 1
        csv.Append(payload=[I, m1,m2,Balancevalue,Valtage,"Balance_OFF"] + [x for y in zip(tdm,tdg,tcm,tcg,vm,vg) for x in y], timestamp=True)
        print(tdm)    
        
def Data_Analysis(Balancevalue,Valtage):
    csv.Append(Evb.CreateTitle1(dut.GetCount() - 1))
    VCC_G = []
    TDS_G = []

    flge =0
    i = 0
    TDS_G0=[]
    TDS_G1=[]
    TDS_G2=[]
    Average_tape_1=[]
    Average_tape_2=[]
    Average_tape_3=[]
    t_start = time.time()
    while flge < 2:
    #while time.time() - t_start < balance_off_time:
        t_start = time.time()
        #while time.time() - t_start < 600:
        #while time.time() - t_start < 1 * 600:   
            #tdg = dut.ReadRegister(RREG.TempDieGuard)[1:]
        vg = dut.ReadRegister(RREG.VoltGuard)[1:]

        tdg = dut.ReadRegister(RREG.TempDieGuard)[1:]
        time.sleep(5)              #两个采样点间隔时间
            
        TDS_G = distribute_items_over_lists(tdg,len(tdg))
        #print(TDS_G)
        TDS_G0.append(TDS_G[0])
        TDS_G1.append(TDS_G[1])
        TDS_G2.append(TDS_G[2])
        if len(TDS_G0) >= 10:      
            window_size = 5
            # 计算移动平均
            moving_averages1 = [np.mean(TDS_G0[i:i+window_size]) for i in range(len(TDS_G0) - window_size + 1)]
            moving_averages2 = [np.mean(TDS_G1[i:i+window_size]) for i in range(len(TDS_G1) - window_size + 1)]
            moving_averages3 = [np.mean(TDS_G2[i:i+window_size]) for i in range(len(TDS_G2) - window_size + 1)]
            log.INF(f"IC1温度: {moving_averages1} ℃")
            log.INF(f"IC2温度: {moving_averages2} ℃")
            log.INF(f"IC3温度: {moving_averages3} ℃")
 

            # 计算相邻移动平均值之间的差值
            differences1 = [moving_averages1[i] - moving_averages1[i-1] for i in range(1, len(moving_averages1))]
            differences2 = [moving_averages2[i] - moving_averages2[i-1] for i in range(1, len(moving_averages2))]
            differences3 = [moving_averages3[i] - moving_averages3[i-1] for i in range(1, len(moving_averages3))]
            log.INF(f"IC1温度差: {differences1} ℃")
            log.INF(f"IC2温度差: {differences2} ℃")
            log.INF(f"IC3温度差: {differences3} ℃")
       

            # 检查差值是否小于0.1，并记录满足条件的最后一项
            recorded_values1 = [moving_averages1[i-1] for i, diff in enumerate(differences1) if diff < 0.15]
            last_recorded_value1 = recorded_values1[-1] if recorded_values1 else None
            recorded_values2 = [moving_averages2[i-1] for i, diff in enumerate(differences2) if diff < 0.15]
            last_recorded_value2 = recorded_values2[-1] if recorded_values2 else None
            recorded_values3 = [moving_averages3[i-1] for i, diff in enumerate(differences3) if diff < 0.15]
            last_recorded_value3 = recorded_values3[-1] if recorded_values3 else None

            # 如果有满足条件的记录，取最后一项，否则为None
            
            
            
            Average_tape_1.append(last_recorded_value1)
            Average_tape_2.append(last_recorded_value2)
            Average_tape_3.append(last_recorded_value3)
            log.INF(f"IC1平均温度: {Average_tape_1} ℃")
            log.INF(f"IC2平均温度: {Average_tape_2} ℃")
            log.INF(f"IC3平均温度: {Average_tape_3} ℃")
            flge = flge +1
            log.INF(f"等待时间30s,{flge}")
            time.sleep(30)

  
        

def distribute_items_over_lists(data_list, n):
    """
    将一个列表中的n项数据分别追加保存到n个列表里。
    
    :param data_list: 原始数据列表
    :param n: 每个新列表中应包含的数据项数
    :return: 一个包含n个列表的列表，每个列表包含原始列表中的n项数据
    """
    # 初始化n个空列表
    lists = [[] for _ in range(n)]
    
    # 迭代原始数据列表，并将数据追加到对应的新列表中
    for i, item in enumerate(data_list):
        lists[i % n].append(item)
        
    return lists
        
                
def add_data(new_data, data_list, max_length=50):
    # 向列表追加新数据
    data_list.append(new_data)
    
    # 如果数据超过最大长度，丢弃第一个数据
    if len(data_list) > max_length:
        data_list.pop(0)
           
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
            Data_Analysis(Balanceoff,Voltage)
            log.INF(f"开启均衡：{BALANCE_on_time} s")
            BalanceonDataRecord(Balance_list,Balance_IDlist,BALANCE_on_time,Voltage)
            print(Voltage)
        print("V_STOP")
    print("STOP")
    log.SUC("DONE")
        
   
                 
  
                
            
    
    
     
    