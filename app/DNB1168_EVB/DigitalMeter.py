
import sys, os, time
WORK_SPACE_PATH=os.path.dirname(os.path.abspath(__file__))+r'/../..'
sys.path.append(WORK_SPACE_PATH+'/equipment/multimeter')
from Keysight_34970A import instr
import LOG

class Meter():
    def __init__(self, name='meter', chan_num=1):
        self._name = name
        self._chan_num = chan_num

    def Read(self) -> list:
        assert 0

    def Read(self, chan:int) -> float:
        assert 0


class DigitalMeter(Meter):
    def __init__(self, port, name='DigitalMeter'):
        Meter.__init__(self, name, 1)
        self._obj = instr(port)
        assert self._obj.open() == True, "Fail to open meter"
        self._obj.temp_conf(Channels="(@301, 302, 303, 304)",Type="K")

    def __del__(self):
        self._obj.close()

    def Read(self):
        return [self._obj.data_read(1)]
    
    def Read(self, chan:int):
        assert chan < self._chan_num
        return self._obj.data_read(1)