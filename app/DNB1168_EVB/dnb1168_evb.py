'''
Created on May 21, 2024

@author: Jessie.Bian
'''
import sys, os, time
import threading
from enum import Enum

#register table: F:\Thomas.Zhu\交接\BBM1839_MemoryMap_MRA4_V0.49_20230620.xlsx

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
sys.path.append(WORK_SPACE_PATH+'/modules/')
import phy, api, reg
import LOG
from sampler import Sampler

# ${WORK_SPACE_PATH}/equipment/oven/Boy_B_TH_48C.py:chamber
class Oven(Sampler):
    def __init__(self, obj, name = "Oven"):
        assert obj != None
        self._obj = obj
        self._timeout = sys.maxsize
        self._temp_diff_threshold = 0.05 # Celcius
        self._extra_delay = 30 * 60 # wait half hour if temperature meet target
        Sampler.__init__(self, name, interval=60)
        
        self._locker.acquire()
        self._obj.set_Status(0)
        self._locker.release()
    
    # TurnOff the Oven. if running, wait thread.join()
    def Stop(self):
        r = Sampler.Stop(self)
        self._locker.acquire()
        self._obj.set_Status(0)
        self._locker.release()
        return r

    # Get current temperature
    def GetTemperature(self) -> float:
        self._locker.acquire()
        self._data = self._obj.get_T() #tzhu: confirm if physical value
        self._locker.release()
        return self._data
    
    # Set target temperture and turn on the oven
    # selcius: target temperature
    # timeout: seconds
    # return(bool): True: success, False: failure
    def SetTemperature(self, celcius: float, timeout: int=sys.maxsize) -> bool:
        assert timeout > self._extra_delay
        if self.IsSampling() == True:
            LOG.ERR("%s is running" % self._name)
            return False
        self._target = celcius
        self._locker.acquire()
        ret = self._obj.set_TargetT(celcius)
        self._locker.release()
        if False == ret:
            LOG.ERR("%s lost connection" % self._name)
            return False
        self._locker.acquire()
        self._obj.set_Status(1)
        self._locker.release()
        self._timeout = timeout
        assert self.Start() == True
        return True
    
    # Get is oven running
    def IsRunning(self) -> bool:
        return self.IsSampling()
    
    def _SampleOnce(self) -> Sampler.Status:
        t = self.GetTemperature()

        # judge whether timeout
        tm = time.time() - self._time_start
        if tm >= self._timeout - self._extra_delay:
            LOG.ERR("%s Timeout!" % self._name)
            return Sampler.Status.TIMEOUT
        
        # judge the temperature meet the target
        if abs(self.GetTemperature() - self._target) > self._temp_diff_threshold:
            return Sampler.Status.SAMPLING
        
        # delay _extra_delay
        for i in range(0, self._extra_delay, self._sample_interval):
            self.Sleep()
            if self._status != Sampler.Status.SAMPLING:
                return self._status
        return self._status
    
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


class DNS1168_EVB:
    def __init__(self, oven = Oven, target_dev = None, temp_meter = None, recorder = None):
        self._oven = oven
        self._target_dev = target_dev
        self._temp_meter = temp_meter
        self._recorder = recorder
    def Enumerate(self):
        assert self._chain != None

    

if __name__ == '__main__':
    chain = 
    obj = api.chain(phy.ser("COM27"))
    obj.open()
    print('done')
