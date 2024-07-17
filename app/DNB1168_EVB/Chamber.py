'''
Created on May 21, 2024

@author: Jessie.Bian
'''
import sys, os, time
import threading

WORK_SPACE_PATH=os.path.split(os.path.realpath(__file__))[0]+r'/../..'
sys.path.append(WORK_SPACE_PATH+'/modules/')
import LOG
from sampler import Sampler

# ${WORK_SPACE_PATH}/equipment/oven/Boy_B_TH_48C.py:chamber
class Chamber(Sampler):
    def __init__(self, obj, name = "Chamber"):
        assert obj != None
        self._obj = obj
        self._timeout = sys.maxsize
        self._temp_diff_threshold = 0.05 # Celcius
        self._extra_delay = 30 * 60 # wait half hour if temperature meet target
        Sampler.__init__(self, name, interval=60)
        
        self._locker.acquire()
        self._obj.set_Status(0)
        self._locker.release()
    
    # TurnOff the Chamber. if running, wait thread.join()
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