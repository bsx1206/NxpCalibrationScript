'''
Created on Jul 15th, 2024

@author: Thomas.Zhu
'''

import sys, os, time
import threading
from enum import Enum
from abc import ABC, abstractmethod

import LOG

# a object for sampling and judging the condition.
class Sampler(ABC):
    class Status(Enum):
        STOPPED = 0
        PRESAMPLING = 1 # shouldn't be get
        SAMPLING = 2
        REACH = 3
        TIMEOUT = 4
        ALERT = 5 # over-threshold, under-threshold or other issue
    def __init__(self, name : str = "Sampler", interval : float = 1.0):
        self._name = name
        self._time_start = None
        self._time_end = None
        self._tid = None
        self._locker = threading.RLock()
        self._sample_interval = interval # seconds
        self._delay_resolution = 0.5
        self._status = Sampler.Status.STOPPED

    # sleep a _sample_interval
    def Sleep(self):
        if self._sample_interval == 0: return
        for i in range(0, self._sample_interval, self._delay_resolution):
            time.sleep(self._delay_resolution)
            if self._status == Sampler.Status.STOPPED:
                break

    def _Sampling(self) -> None:
        self._time_start = time.time()
        self._status = Sampler.Status.SAMPLING
        while self._status == Sampler.Status.SAMPLING:
            self._status == self._SampleOnce()
            if self._status != Sampler.Status.SAMPLING:
                break
            self.Sleep()
        self._time_end = time.time()
        LOG.INF("%s exit Sampling. %d" % (self._name, self._status))
            
    
    # stop the sampler
    def Stop(self) -> bool:
        if self._status == Sampler.Status.SAMPLING:
            self._status = Sampler.Status.STOPPED
            self._time_end = None
            self.tid.join()
        else:
            LOG.WRN("%s not SAMPLING" % self._name)
        return True
        

    # start the sampler
    def _Start(self) -> bool:
        if self._status == Sampler.Status.SAMPLING:
            LOG.WRN("%s is SAMPLING!" % self._name)
            return False
        self._time_start = None
        self._time_end = None
        self._status = Sampler.Status.PRESAMPLING
        self._tid = threading.Thread(target=self._Sampling, name=self._name)
        self._tid.start()
        while self._status == Sampler.Status.PRESAMPLING:
            time.sleep(self._delay_resolution)
        return True
    
    def IsSampling(self) -> bool:
        return True if self._status == Sampler.Status.SAMPLING else False
    
    def GetStatus(self) -> Status:
        return self._status
    
    def GetSecondsTake(self):
        if None == self._time_start:
            LOG.WRN("%s not start yet" % self._name)
            return 0
        if None == self._time_end:
            LOG.WRN("%s not reach target" % self._name)
            return time.time() - self._time_start
        return self._time_end - self._time_start

    # trigger once sampling, for override
    @abstractmethod
    def _SampleOnce(self) -> Status:
        return Sampler.Status.ALERT

    