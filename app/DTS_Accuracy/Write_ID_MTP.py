
import sys
import time

sys.path.append(r'../../driver/')
import phy, api
LinxNumber=17
ser = phy.ser("COM4")
chain1 = api.chain(ser)
chain1.open()
while True:
    chain1.en()
    if chain1.linx_num != LinxNumber:continue
    while True:
        if not chain1.cmd("%02X080%02X" %(0xFF,LinxNumber),2): continue
        break
    break
time.sleep(5)
while True:
    chain1.en()
    if chain1.linx_num != LinxNumber:continue
    while True:
        if not chain1.cmd("%02X180%02X" %(0xFF,LinxNumber+1),2): continue
        break
    break
##for i in range(1,LinxNumber):
##    while True:
##        if not chain1.cmd("%02X080%02X" %(i+1,i+1),2): continue
##        break


# -------------------------------------------------------------------------------------------------

