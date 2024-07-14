'''
Created on May 21, 2024

@author: Jessie.Bian
'''
import sys, os, time
import threading
from enum import Enum

import configparser
from csv import reader
WORK_SPACE_PATH=os.path.split(os.path.realpath(__file__))[0]+r'/../..'
sys.path.append(WORK_SPACE_PATH+'/driver/')
sys.path.append(WORK_SPACE_PATH+'/equipment/')
sys.path.append(WORK_SPACE_PATH+'/equipment/power/')
sys.path.append(WORK_SPACE_PATH+'/equipment/oven')
sys.path.append(WORK_SPACE_PATH+'/equipment/mux')
sys.path.append(WORK_SPACE_PATH+'/equipment/multimeter')
sys.path.append(WORK_SPACE_PATH+'/equipment/tempref')
sys.path.append(WORK_SPACE_PATH+'/equipment/counter')
import phy, api, reg

# Formating UnitTIme to string
def FMT_UNIX_TIME(t) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

# Get formated current time
def FMT_NOW() -> str:
    return FMT_UNIX_TIME(time.time())

# Print Debug Leveled log
def LOG_DBG(s:str) -> None:
    print("\033[0;34;40m[%s]:DBG: %s\033[0m" % (FMT_NOW(), s))

# Print Information Leveled log
def LOG_INF(s:str) -> None:
    print("\033[0;37;40m[%s]:INF: %s\033[0m" % (FMT_NOW(), s))

# Print Warning Leveled log
def LOG_WRN(s:str) -> None:
    print("\033[0;33;40m[%s]:WRN: %s\033[0m" % (FMT_NOW(), s))

# Print Error Leveled log
def LOG_ERR(s:str) -> None:
    print("\033[0;31;40m[%s]:ERR: %s\033[0m" % (FMT_NOW(), s))

# Print GOOD Leveled log
def LOG_GOD(s:str) -> None:
    print("\033[0;32;40m[%s]:GOD: %s\033[0m" % (FMT_NOW(), s))

# a object for sampling and judging the condition.
class Sampler():
    class Status(Enum):
        TERMINATED = 0
        SAMPLING = 1
        REACH = 2
        TIMEOUT = 3
    def __init__(self, name, target, threshold, repeat_limit, timeout, delay_f, sample_f, sample_args = None):
        self._name = name
        self._target = target
        self._threshold = threshold
        self._repeat_limit = repeat_limit
        self._timeout = timeout
        self._delay_f = delay_f
        self._sample_f = sample_f
        self._sample_args = sample_args
        self._time_start = None
        self._time_end = None
        self._repeat_n = 0
        self._repeat_total = 0
        self._status = Sampler.Status.TERMINATED

    # restart the sampler
    def Restart(self):
        self._time_start = None
        self._time_end = None
        self._repeat_n = 0
        self._repeat_total = 0
        self._status = Sampler.Status.SAMPLING

    # trigger once sampling
    def DoOnce(self):
        if self._status != Sampler.Status.SAMPLING:
            return self._status
        if None == self._time_start:
            self._time_start = time.time()
        # True means terminated
        if True == self._delay_f():
            LOG_WRN("%s to %s is terminated" % (self._name, self._target))
            self._status = Sampler.Status.TERMINATED
            return self._status
        fv = self._sample_f(self._sample_args)
        if abs(fv, self._target) <= self._threshold:
            self._repeat_total += 1
            self._repeat_n += 1
            if self._repeat_n >= self._repeat_limit:
                self._time_end = time.time()
                self._status = Sampler.Status.REACH
                return self._status
        else:
            self._repeat_n = 0
        if self._timeout > time.time() - self.time_start:
            self._status = Sampler.Status.TIMEOUT
        return self._status
    
    # stop the sampler
    def Terminate(self):
        self._time_end = None
        self._status = Sampler.Status.TERMINATED
    
    def GetStatus(self):
        return self._status
    
    def GetSecondsTake(self):
        if None == self._time_start:
            LOG_WRN("%s not start yet" % self._name)
            return 0
        if None == self._time_end:
            LOG_WRN("%s not reach target" % self._name)
            return time.time() - self._time_start
        return self._time_end - self._time_start
        


# ${WORK_SPACE_PATH}/equipment/oven/Boy_B_TH_48C.py:chamber
class Oven():
    def __init__(self, obj, name = "Oven"):
        assert obj != None
        self._name = name
        self._obj = obj

        # control relevant
        self._sampler = None

        # thread relevant
        self._is_running = False
        self._locker = threading.RLock()
        self._tid = None

    def _DelayOneDuration(self) -> bool:
            for i in range(0, self._read_duration):
                time.sleep(1)
                if self._is_running == False:
                    return True
            return False

    def _ThreadMonitoring(self):
        while True:
            # read
            status = self._sampler.DoOnce()
            if status == Sampler.Status.TERMINATED:
                break
            elif status == Sampler.Status.REACH:
                self._locker.acquire()
                self._obj.set_Status(0)
                self._locker.release()
                break
            elif status == Sampler.Status.TIMEOUT:
                LOG_ERR("%s timeout" % self._name)
                break
            elif status != Sampler.Status.SAMPLING:
                assert False

        self._is_running = False
        return 0

    # TurnOff the Oven. if running, wait thread.join()
    def TurnOff(self) -> None:
        self._locker.acquire()
        self._obj.set_Status(0)
        self._locker.release()
        if self._is_running == False: return
        self._is_running = False
        self._tid.join()

    # Get current temperature
    def GetTemperature(self) -> float:
        self._locker.acquire()
        t = self._obj.get_T() #tzhu: confirm if physical value
        self._locker.release()
        return t
    
    # Set target temperture and turn on the oven
    # selcius: target temperature
    # timeout: seconds
    # return(bool): True: success, False: failure
    def SetTemperature(self, celcius: float, timeout: int=0) -> bool:
        if self._is_running == True:
            LOG_ERR("%s is running" % self._name)
            return False
        self._sampler = Sampler(name="Oven::sampler", target=celcius, threshold=0.1, repeat_limit=100, 
                                timeout=sys.maxsize if timeout == 0 else timeout,
                                delay_f=self._DelayOneDuration, sample_f=self.GetTemperature)
        self._locker.acquire()
        ret = self._obj.set_TargetT(celcius)
        self._locker.release()
        if False == ret:
            LOG_ERR("%s lost connection" % self._name)
            return False
        self._locker.acquire()
        self._obj.set_Status(1)
        self._locker.release()
        self._timeout = sys.maxsize if timeout == 0 else timeout
        self._is_running = True
        self._tid = threading.Thread(target=self._ThreadMonitoring, name=self._name)
        self._tid.start()

        return True
    
    # Get is oven running
    def IsRunning(self) -> bool:
        return self._is_running
    
    # Get target temperature
    def GetTarget(self):
        return self._target
    
class DevData():
    def __init__(self, name, reg, phy2count, count2phy):
        self._name = name
        self._reg = reg
        self._phy2count = phy2count
        self._count2phy = count2phy
    def GetCount(self, phy: float) -> int:
        return self._phy2count(phy)
    def GetPhysical(self, count: int) -> float:
        return self._count2phy(count)
    def volt2count(volt: float) -> int:
        return int(volt / 2.5 * 4096.0) #tzhu: need confirm the formula
    def count2volt(count: int) -> float:
        return float(count)/4096.0 * 2.5
    def temp2count(temp: float) -> int:
        return int(temp / 100.0 * 1024.0)
    def count2temp(count: int) -> float:
        return float(count)/1024.0 * 2.5

# ${WORK_SPACE_PATH}/driver/api.py:chain
class TargetDev():
    def __init__(self, obj):
        assert obj != None
        self._obj = obj
        self._num_ics = 0
        self._data_dict = {
            "MainVolt" : DevData("MainVolt", 1, DevData.volt2count, DevData.count2volt),
            "GuardVolt" : DevData("GuardVolt", 2, DevData.volt2count, DevData.count2volt),
            "MainCellTemp" : DevData("MainCellTemp", 3, DevData.temp2count, DevData.count2temp),
            "GuardCellTemp" : DevData("GuardCellTemp", 4, DevData.temp2count, DevData.count2temp),
            "MainDieTemp" : DevData("MainDieTemp", 5, DevData.temp2count, DevData.count2temp),
            "GuardDieTemp" : DevData("GuardDieTemp", 6, DevData.temp2count, DevData.count2temp)
        }

    def Enumerate(self) -> bool:
        self._num_ics = 0
        self._obj.open()
        if self._obj.en() == False:
            return False
        self._num_ics = self._obj.linx_num #tzhu: need confirm the data layout
        return True
    
    def GetDevNum(self) -> int:
        return self._num_ics
    
    def ListDatas(self) -> None:
        for key in self._data_dict:
            print(key)
        return
    
    def ReadData(self, item: str):
        if self._data_dict.has_key(item) == False: return None
        dev_data = self._data_dict[item]
        data = self._obj.GetData(item)
        print(data) #tzhu: need confirm the data layout
        #tzhu: may need call dev_data.GetPhysical(data)
        return


class DNS1168_EVB:
    def __init__(self, oven = Oven, target_dev = None, temp_meter = None, recorder = None):
        self._oven = oven
        self._target_dev = target_dev
        self._temp_meter = temp_meter
        self._recorder = recorder
    def Enumerate(self):
        assert self._chain != None
