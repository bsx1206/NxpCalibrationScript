import os, sys
WORK_SPACE_PATH=os.path.dirname(os.path.abspath(__file__))+r'/../..'
sys.path.append(WORK_SPACE_PATH+'/modules/')
import LOG

class Recorder(LOG):
    def __init__(self, path, param:str='a+'):
        os.remove(path)
        LOG.__init__(self, target=path, level=LOG.LOG_LEVEL.ALL)
        self._num_record = 0

    def Append(self, title:str):
        LOG.CSV(title, False)

    def SetTitle