'''
Created on Jul 18, 2024

@author: Jessie.bian
'''

import LOG
import Keysight_34970A
import pyvisa, time,datetime,os

#import pyvisa, time
rsc_Keysight_34970  = "GPIB0::3::INSTR"




def Keysight_34970A_GetData():
    meter = Keysight_34970A.instr()
    if not meter.open():
        print("error open meter")
        return
    # meter.temp_conf()
    meter.temp_conf(Channels="(@301, 302, 303, 304)",Type="K")
    count=10
    while count>0:
        #count -= 1
        Test_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S-%f")
        #Test_time = time.strftime("%H:%M:%S", time.localtime())
        data = meter.data_read(1)
        #print(data,Test_time)
        #print(data[0])
        lc = LOG.LOG(target=f'{current_directory}/test.csv')
        lc.CSV([data[0],data[1],data[2],data[3]],True)
        #lc.CSV(data,Test_time,True)

        # time.sleep(1)



if __name__ == "__main__":
    LOG_LEVEL = LOG.LOG_LEVEL
    #l = LOG.LOG_CLASS(level=LOG_LEVEL.ALL)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    Keysight_34970A_GetData()
    exit()
    