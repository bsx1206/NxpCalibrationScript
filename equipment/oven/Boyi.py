'''
Created on Feb 14, 2018

@author: felix.yao
'''

import time
import phy

BAUDRATE = 9600
TIMEOUT  = 0.2

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
        print("\n > Tx:")
        # list_print(tx_data)
        tx_buf = b''.join(map(hex_decode_str, tx_data))
        print('tx_buf',tx_buf)
        print(tx_buf)
        self.tx(tx_buf,True)
        rx_buf = []
        rx_buf.extend(list(self.rx(True)))
        print('rx_buf',rx_buf)
        rx_data = []
        rx_data.extend(list(map(str_encode_hex, rx_buf)))
        print(" < Rx:")
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
    def set_Mode(self, mode=1):                             # 0: program, 1: constant
        data_lst = self.write_s(addr32=90, data32=mode)
        print(" # Set operating mode to", end=' ')
        print('"program" ------' if mode == 0 else '"constant" ------', end=' ')
        if data_lst == False:
            print("Failed!")
            return False
        print("Successful!")
        return True
    
    def set_Status(self, status=0):                         # 0: stop, 1: run
        data_lst = self.write_s(addr32=63, data32=status)
        print(" # Set operating status to", end=' ')
        print('"stop" ------' if status == 0 else '"run" ------', end=' ')
        if data_lst == False:
            print("Failed!")
            return False
        print("Successful!")
        return True

    def set_TargetT(self, temp=25.0):
        set_temp = int(temp * 10)
        data_lst = self.write_s(addr32=60, data32=set_temp)
        print(" # Set temperature target to %s(degreeC) ------" %temp, end=' ')
        if data_lst == False:
            print("Failed!")
            return False
        print("Successful!")
        return True
    
    def set_Clock(self, year=None, month=None, day=None, hour=None, minute=None, second=None):
        clock = time.localtime()
        if year == None: year = clock.tm_year
        if month == None: month = clock.tm_mon
        if day == None: day = clock.tm_mday
        if hour == None: hour = clock.tm_hour
        if minute == None: minute = clock.tm_min
        if second == None: second = clock.tm_sec
        data_lst = self.write(addr32=92, data32_lst=[year, month, day, hour, minute, second])
        print(" # Set clock to: %d-%02d-%02d %02d:%02d:%02d ------" %(year, month, day, hour, minute, second), end=' ')
        if data_lst == False:
            print("Failed!")
            return False
        print("Successful!")
        return True

    def get_Mode(self):
        data_lst = self.read(addr32=30)
        if data_lst == False: return None
        if not data_lst[2] == 2: return None
        data = (data_lst[3] << 8) + data_lst[4]
        if not data in [0, 1]: return None
        print(" * Operating mode:", end=' ')
        print("program" if data == 0 else "constant")
        return data
    
    def get_Status(self):
        data_lst = self.read(addr32=31)
        if data_lst == False: return None
        if not data_lst[2] == 2: return None
        data = (data_lst[3] << 8) + data_lst[4]
        if not data in [0, 1]: return None
        print(" * Operating status:", end=' ')
        print("stop" if data == 0 else "run")
        return data
    
    def get_TargetT(self):
        data_lst = self.read(addr32=11)
        if data_lst == False: return None
        if not data_lst[2] == 2: return None
        data = ((data_lst[3] << 8) + data_lst[4])/10.0
        if data > 1000:
            data = data -6553.6
        print(" * Target temperature (degreeC): %s" %data)
        return data
    
    def get_T(self):
        data_lst = self.read(addr32=10)
        if data_lst == False: return None
        if not data_lst[2] == 2: return None
        data = ((data_lst[3] << 8) + data_lst[4])/10.0
        if data > 1000:
            data = data -6553.6
        print(" * Current temperature (degreeC): %s" %data)
        return data
    
    def get_Clock(self):
        data_lst = self.read(addr32=92, cnt32=6)
        if data_lst == False: return None
        if not data_lst[2] == 12: return None
        year = (data_lst[3] << 8) + data_lst[4]
        month = (data_lst[5] << 8) + data_lst[6]
        day = (data_lst[7] << 8) + data_lst[8]
        hour = (data_lst[9] << 8) + data_lst[10]
        minute = (data_lst[11] << 8) + data_lst[12]
        second = (data_lst[13] << 8) + data_lst[14]
        print(" * Chamber clock: %d-%02d-%02d %02d:%02d:%02d" %(year, month, day, hour, minute, second))
        return [year, month, day, hour, minute, second]
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
    Tchamber = chamber("COM17")
    if not Tchamber.open(): return False
    Tchamber.set_Mode(mode=1)
    Tchamber.set_Status(status=1)
    for t in [25]:
        Temp_temp = Tchamber.get_T()
        while Temp_temp > t+5 :
            Tchamber.set_TargetT(temp=Temp_temp-5)
            while (Tchamber.get_T() < (t - 2)) or (Tchamber.get_T() > (t + 2)): time.sleep(10)
            Temp_temp = Tchamber.get_T()
        Tchamber.set_TargetT(temp=t)
        while (Tchamber.get_T() < (t - 0.5)) or (Tchamber.get_T() > (t + 0.5)): time.sleep(5)
#    Tchamber.set_Status(status=0)
 
#    Tchamber.set_Mode(mode=1)
#    Tchamber.get_Mode()
#    Tchamber.get_Status()
#    Tchamber.set_TargetT()
#    Tchamber.get_TargetT()
#    Tchamber.set_Status()
#    Tchamber.get_T()
#    Tchamber.get_Clock()
#    Tchamber.set_Clock()
#    Tchamber.get_Clock()
    return
def test1():
    Tchamber = chamber("COM17")
    if not Tchamber.open(): return False
    # Tchamber.set_Mode(mode=1)
    Tchamber.set_TargetT(-25)
    Tchamber.get_TargetT()
if __name__ == "__main__":
    test1()
    exit()
