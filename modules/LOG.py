'''
Created on Jul 15th, 2024

@author: Thomas.Zhu
'''

import sys, os, time, datetime
from enum import Enum

# Formating UnitTIme to string
def FMT_UNIX_TIME(t) -> str:
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")

def FMT_UNIX_TIME_MS(t) -> str:
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def FMT_UNIX_TIME_US(t) -> str:
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S.%f")

# Formating UnitTIme to string
def FMT_UNIX_TIME_FOR_CSV(t) -> str:
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S-%f")[:-3]

# Get formated current time
def FMT_NOW() -> str:
    return FMT_UNIX_TIME(time.time())

def FMT_NOW_MS() -> str:
    return FMT_UNIX_TIME_MS(time.time())

def FMT_NOW_US() -> str:
    return FMT_UNIX_TIME_US(time.time())

class LOG_LEVEL(Enum):
    ALL = 0x0
    DEBUG = 0x1
    INFO = 0x2
    WARNING = 0x3
    ERROR = 0x4
    NONE = 0
    def get(str):
        try:
            return LOG_LEVEL[str]
        except KeyError:
            raise ValueError(f"Invalid LOG_LEVEL: {str}")

class LOG():
    def __init__(self, target=None, level=LOG_LEVEL.ALL):
        self._target = target
        self._level = level
        if isinstance(self._target, str):
            self._fp = open(self._target, 'a+')
            assert self._fp != None
        else:
            self._fp = None

    def __del__(self):
        if self._fp:
            self._fp.close()

    # Print Debug Leveled log
    def DBG(self, s:str) -> None:
        if self._level.value <= LOG_LEVEL.DEBUG.value:
            if self._fp != None:
                self._fp.write(f"[%s]:DBG: %s\n" % (FMT_NOW_US(), s)); self._fp.flush()
            else:
                print("\033[0;34;40m[%s]:DBG: %s\033[0m" % (FMT_NOW_US(), s))

    # Print Information Leveled log
    def INF(self, s:str) -> None:
        if self._level.value <= LOG_LEVEL.INFO.value:
            if self._fp != None:
                self._fp.write(f"[%s]:INF: %s\n" % (FMT_NOW_US(), s)); self._fp.flush()
            else:
                print("\033[0;37;40m[%s]:INF: %s\033[0m" % (FMT_NOW_US(), s))

    # Print Warning Leveled log
    def WRN(self, s:str) -> None:
        if self._level.value <= LOG_LEVEL.WARNING.value:
            if self._fp != None:
                self._fp.write(f"[%s]:WRN: %s\n" % (FMT_NOW_US(), s)); self._fp.flush()
            else:
                print("\033[0;33;40m[%s]:WRN: %s\033[0m" % (FMT_NOW_US(), s))

    # Print Error Leveled log
    def ERR(self, s:str) -> None:
        if self._level.value <= LOG_LEVEL.ERROR.value:
            if self._fp != None:
                self._fp.write(f"[%s]:ERR: %s\n" % (FMT_NOW_US(), s)); self._fp.flush()
            else:
                print("\033[0;31;40m[%s]:ERR: %s\033[0m" % (FMT_NOW_US(), s))

    # Print Succeed Leveled log
    def SUC(self, s:str) -> None:
        if self._level.value <= LOG_LEVEL.DEBUG.value:
            if self._fp != None:
                self._fp.write(f"[%s]:SUC: %s\n" % (FMT_NOW_US(), s)); self._fp.flush()
            else:
                print("\033[0;32;40m[%s]:SUC: %s\033[0m" % (FMT_NOW_US(), s))

class CSV():
    def __init__(self, path:str):
        self._fp = open(path, 'a+')
        assert self._fp != None

    def __del__(self):
        self._fp.close()

    def Append(self, payload, timestamp=False) -> None:
        __record = f'%s,' % FMT_UNIX_TIME_FOR_CSV(time.time()) if True == timestamp else ""
        if isinstance(payload, list):
            for e in payload:
                __record += f'%s,' % str(e)
        else:
            __record += f'{payload}'
        if self._fp != None:
            self._fp.write(__record + '\n'); self._fp.flush()
        else:
            print(__record)

    def Blank(self):
        self._fp.write('\n'); self._fp.flush()

def test_log(l):
    l.DBG("This is dbg")
    l.INF("Tis is Info")
    l.WRN("This is Warning")
    l.ERR("This is Error")
    l.SUC("This is Succeed")
if __name__ == "__main__":
    l = LOG(level=LOG_LEVEL.WARNING)
    print("log to stdout with WARNING")
    test_log(l)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    now = FMT_NOW().replace(':', '.')
    l2 = LOG(target=f'{current_directory}\\../log/{now}.log')
    print(f'log to {current_directory}/test.log with ALL')
    test_log(l2)
    l3 = LOG(target=f'{current_directory}\\../log/{now}.log')
    print(f'repeat log to {current_directory}/test.log with ALL')
    test_log(l3)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    lc = CSV(path=f'{current_directory}\\../log/{now}.csv')
    lc.Append("This is CSV Caption Line")
    lc.Append("TIME, item1, item2, item3")
    lc.Append("111, 222, 333", True)
    lc.Append([3.45, 2.14, 567], True)
    