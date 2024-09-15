'''
Created on Feb 14, 2017
Update on Dec 11, 2020

@author: felix.yao
@update: luke.pan
'''

import serial
import time
BAUDRATE = 1000000
TIMEOUT  = 0.01
BYTESIZE = serial.EIGHTBITS     #FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
PARITY   = serial.PARITY_NONE   #PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE
STOPBIT  = serial.STOPBITS_ONE  #STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
XONXOFF  = False                #XON, XOFF

RX_BUFFER = 999999


class ser(object):
    def __init__(self, COM = None):
        self.COM = COM
        self.ser = serial.Serial(baudrate = BAUDRATE,
                                 bytesize = BYTESIZE,
                                 parity   = PARITY,
                                 stopbits = STOPBIT,
                                 timeout  = TIMEOUT,
                                 xonxoff  = XONXOFF)
        
        self.bytesflag=0

    def open(self):
            try:
                self.ser.port = self.COM
                self.ser.open()
                self.ser.reset_output_buffer()
                self.ser.reset_input_buffer()
                print("%s port has been opened successful!" % self.ser.port)
                print(self.ser)
                return True
            except:
                print("<Error!>: COM port open failed!\n")
                return False

    def isopen(self):
        return self.ser.is_open

    def tx(self, tx_buf, isbytes=False,delay=0):
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        time.sleep(delay) if delay != 0 else None
        if isbytes:
            self.ser.write(tx_buf)
        else:
            self.ser.write(tx_buf.encode())
        return

    def rx(self,isbytes=False):
        rx_buf = ""
        while True:
            
            if not isbytes:
                rx_tmp = self.ser.read(RX_BUFFER).decode()
            else:
                rx_tmp = self.ser.read(RX_BUFFER)   
                return rx_tmp
            if rx_tmp == "": return rx_buf
            rx_buf = rx_buf + str(rx_tmp)

        

    def close(self):
        self.ser.close()
        self.ser.port = None
        del self.ser
        return

# -------------------------------------------------------------------------------------------------
def test():
    te=ser("COM62")
    if not te.open():
        print("error open")
        return
    te.tx("cc 0\n")
    rxbuf=te.rx()
    print(rxbuf)
    te.close()
    return

if __name__ == "__main__":
    test()
    exit()
