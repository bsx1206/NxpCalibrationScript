'''
Created on Dec 26th, 2019

@author: Peter.Pan

'''

import serial

BAUDRATE = 1000000
TIMEOUT  = 0.005
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

    def tx(self, tx_buf):
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        self.ser.write(tx_buf.encode())
        return

    def rx(self, endchar=0):
        rx_buf = ""
        cnt = 0
        while True:
            cnt += 1
            rx_tmp = self.ser.read(RX_BUFFER).decode()
            rx_buf = rx_buf + rx_tmp
            if endchar == 0:
                sub_cntdiscard = rx_buf.find("trx>")
                if  sub_cntdiscard > 0: return rx_buf
                if cnt > 1000: 
                    print("SER Rx Over Time")
                    return
            if endchar == 1:
                if rx_tmp == "": return rx_buf
    def Relay_Switch(self, switch):        
        cmd_str = "RL %d\n" %switch
        print("\nTurn on relay %d" %switch)
        self.tx(cmd_str)
        rx_buf = self.rx()
        print(rx_buf)
        return 0
    def Relay_Delay(self, delay):        
        cmd_str = "RI %d\n" %delay
        print("\nSet delay between turn off all relays and turn on one relay to %dms" %delay)
        self.tx(cmd_str)
        rx_buf = self.rx()
        print(rx_buf)
        return 0
    def close(self):
        self.ser.close()
        self.ser.port = None
        del self.ser
        return

# -------------------------------------------------------------------------------------------------
def test():
    import time
#     seri = ser("COM3")
    MUX_Board = ser("COM26")
    if not MUX_Board.open(): return
    MUX_Board.Relay_Delay(1000)
    for i in range(1,17):
        MUX_Board.Relay_Switch(i)
        time.sleep(2)
    MUX_Board.Relay_Switch(0)
##    MUX_Board.Relay_Delay(100)
##    time.sleep(0.5)
##    relay_number = 0
##    while relay_number<13:
##        relay_number += 1
##        MUX_Board.Relay_Switch(relay_number)
##        time.sleep(3)
##    MUX_Board.Relay_Switch(0)
##    MUX_Board.close()
    return

if __name__ == "__main__":
    test()
    exit()
