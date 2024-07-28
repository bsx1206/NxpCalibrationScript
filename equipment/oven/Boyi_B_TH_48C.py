'''
@since: 28/08/2020
@version: V1.01
@author: peter.pan
@change: 
        28/08/2020 Peter.Pan    
        1.    Created
        02/09/2020 Peter.Pan
        1.    Fixed negative temperature miscalculation problem
        2.    Changed the symbol in the file name
'''

import time,sys,os
WORK_SPACE_PATH=os.path.dirname(os.path.abspath(__file__))+r'/../..'
sys.path.append(WORK_SPACE_PATH+'/driver/')
import phy

BAUDRATE = 9600
TIMEOUT  = 0.5

class chamber(phy.ser):
    def __init__(self, COM=None):
        phy.ser.__init__(self, COM)
        self.ser.baudrate = BAUDRATE
        self.ser.timeout = TIMEOUT

    def read(self, addr32, cnt32=1):
        addrH = (addr32 & 0xFF00) >> 8
        addrL = (addr32 & 0x00FF)
        cntH = (cnt32 & 0xFF00) >> 8
        cntL = (cnt32 & 0x00FF)
        frame = [0x01, 0x03, addrH, addrL, cntH, cntL]
        crc = CRC_cal(frame)
        crcH = (crc & 0xFF00) >> 8
        crcL = (crc & 0x00FF)
        tx_data = frame + [crcH, crcL]
        print("\n > Tx:")
        list_print(tx_data)
        tx_buf = b''.join(map(hex_decode_str, tx_data))
        self.tx(tx_buf,True)
        rx_buf = []
        rx_buf.extend(list(self.rx(True)))
        rx_data = []
        rx_data.extend(list(map(str_encode_hex, rx_buf)))
        print(" < Rx:")
        list_print(rx_data)
        if len(rx_data) < 7: return False
        if not rx_data[0] == 0x01: return False
        if not rx_data[1] == 0x03: return False
        cnt = rx_data[2]
        if len(rx_data) < (cnt+5): return False
        frame = rx_data[0:cnt+5]
        crc = CRC_cal(frame[0:-2])
        crcH = (crc & 0xFF00) >> 8
        crcL = (crc & 0x00FF)
        if not (crcH == frame[-2] and crcL == frame[-1]): return False
        return frame
    
    def write_s(self, addr32, data32):
        addrH = (addr32 & 0xFF00) >> 8
        addrL = (addr32 & 0x00FF)
        dataH = (data32 & 0xFF00) >> 8
        dataL = (data32 & 0x00FF)
        frame = [0x01, 0x06, addrH, addrL, dataH, dataL]
        crc = CRC_cal(frame)
        crcH = (crc & 0xFF00) >> 8
        crcL = (crc & 0x00FF)
        tx_data = frame + [crcH, crcL]
        print("\n > Tx:", end=' ')
        list_print(tx_data)
        tx_buf = b''.join(map(hex_decode_str, tx_data))
        self.tx(tx_buf,True)
        rx_buf = []
        rx_buf.extend(list(self.rx(True)))
        rx_data = []
        rx_data.extend(list(map(str_encode_hex, rx_buf)))
        print(" < Rx:", end=' ')
        list_print(rx_data)
        if len(rx_data) < 8: return False
        frame = rx_data[0:8]
        if not (crcH == frame[-2] and crcL == frame[-1]): return False
        return frame
    def write_single_coil(self, addr32, data32):
        addrH = (addr32 & 0xFF00) >> 8
        addrL = (addr32 & 0x00FF)
        dataH = (data32 & 0xFF00) >> 8
        dataL = (data32 & 0x00FF)
        frame = [0x01, 0x05, addrH, addrL, dataH, dataL]
        crc = CRC_cal(frame)
        crcH = (crc & 0xFF00) >> 8
        crcL = (crc & 0x00FF)
        tx_data = frame + [crcH, crcL]
        print("\n > Tx:", end=' ')
        list_print(tx_data)
        tx_buf = b''.join(map(hex_decode_str, tx_data))
        self.tx(tx_buf,True)
        rx_buf = []
        rx_buf.extend(list(self.rx(True)))
        rx_data = []
        rx_data.extend(list(map(str_encode_hex, rx_buf)))
        print(" < Rx:", end=' ')
        list_print(rx_data)
        if len(rx_data) < 8: return False
        frame = rx_data[0:8]
        if not (crcH == frame[-2] and crcL == frame[-1]): return False
        return frame
    
    def write(self, addr32, data32_lst):
        addrH = (addr32 & 0xFF00) >> 8
        addrL = (addr32 & 0x00FF)
        cnt = len(data32_lst)
        cntH = (cnt & 0xFF00) >> 8
        cntL = (cnt & 0x00FF)
        cnt2 = cnt * 2
        data_lst = []
        for i in range(cnt):
            data_lst.append((data32_lst[i] & 0xFF00) >> 8)
            data_lst.append((data32_lst[i] & 0x00FF))
        frame = [0x01, 0x10, addrH, addrL, cntH, cntL, cnt2] + data_lst
        crc = CRC_cal(frame)
        crcH = (crc & 0xFF00) >> 8
        crcL = (crc & 0x00FF)
        tx_data = frame + [crcH, crcL]
        print("\n > Tx:", end=' ')
        list_print(tx_data)
        tx_buf = b''.join(map(hex_decode_str, tx_data))
        self.tx(tx_buf,True)
        rx_buf = []
        rx_buf.extend(list(self.rx(True)))
        rx_data = []
        rx_data.extend(list(map(str_encode_hex, rx_buf)))
        print(" < Rx:", end=' ')
        list_print(rx_data)
        if len(rx_data) < 8: return False
        frame = rx_data[0:8]
        crc = CRC_cal(frame[0:-2])
        crcH = (crc & 0xFF00) >> 8
        crcL = (crc & 0x00FF)
        if not (crcH == frame[-2] and crcL == frame[-1]): return False
        return frame
# ---------------------------------------------------------
    
    def set_Status(self, status=0):                         # 0: stop, 1: run
        data_lst = False
        if status == 0: #stop
            data_lst = self.write_single_coil(addr32=213, data32=0xFF00)
            data_lst = self.write_single_coil(addr32=1200, data32=0x0000)
        else:   #run
            data_lst = self.write_single_coil(addr32=212, data32=0xFF00)
            data_lst = self.write_single_coil(addr32=1200, data32=0xFF00)
        print(" # Set operating status to", end=' ')
        print('"stop" ------' if status == 0 else '"run" ------', end=' ')
        if data_lst == False:
            print("Failed!")
            return False
        print("Successful!")
        return True

    def set_TargetT(self, temp=25.0):
        Temp_temp = None  
        set_temp = int(temp * 10)
        data_lst = self.write_s(addr32=1870, data32=set_temp)
        print(" # Set temperature target to %s(degreeC) ------" %temp, end=' ')
        if data_lst == False:
            print("Failed!")
            return False
        print("Successful!")
        return True        
        
    def get_TargetT(self):
        data_lst = self.read(addr32=1870)
        if data_lst == False: return None
        if not data_lst[2] == 2: return None
        data = ((data_lst[3] << 8) + data_lst[4])
        if data > 0x8000:
            data = data -65536
        data = data/10.0
        print(" * Target temperature (degreeC): %s" %data)
        return data
    
    def get_T(self):
        data_lst = self.read(addr32=540)
        print(data_lst)
        if data_lst == False: return None
        if not data_lst[2] == 2: return None
        data = (data_lst[3] << 8) + data_lst[4]
        if data > 0x8000:
            data = data -65536
        data = data/100.0
        print(" * Current temperature (degreeC): %s" %data)
        return data

# -----------------------------------------------------------------------------
def CRC_cal(buf):
    crc16 = 0xFFFF
    for i in range(len(buf)):
        crc16 ^= buf[i]
        for j in range(8):
            if ((crc16 & 0x01) == 1):
                crc16 = (crc16 >> 1) ^ 0xA001
            else:
                crc16 = crc16 >> 1
    return ((crc16 & 0x00FF) << 8) | ((crc16 & 0xFF00) >> 8)

def hex_decode_str(hex_data):
    if not isinstance(hex_data, int): return None
    hex_str = hex(hex_data)[2::]
    if len(hex_str)%2 != 0: hex_str = '0' + hex_str
    return bytes.fromhex(hex_str)

def str_encode_hex(str_data):
    try:
        return  str_data
    except:
        return None

def list_print(list_int):
    if list_int == None: return
    for i in list_int: print('0x%02x' %i, end=' ')
    print()
    return
# -------------------------------------------------------------------------------------------------
def test():
    Tchamber = chamber("COM4")
    if not Tchamber.open(): return False
    print("chamber open successful")

    print(Tchamber.set_TargetT(temp=40.0))
    Tchamber.set_Status(status = 1)
    while True:
        tem = Tchamber.get_T()
        time.sleep(10)
        print(tem)
        if abs(tem-25) <1:
            Tchamber.set_Status(status = 0)
            break
        
    return

if __name__ == "__main__":
    test()
    exit()
