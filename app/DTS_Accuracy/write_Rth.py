#coding:utf-8
'''
Created on 23th Sep. 2021

@author: Mark.Kan


'''
import time
import phy, api, reg
import Keysight_34465A
import MUX
import OVEN
import POWER
import Fluke_1524



def PC_Init(com="COM80"):
    pc = api.chain(phy.ser(com))
    print("Open Pack Controller Board ")
    if not pc.open():
        print("Failed")
        return False
    print("Successful")
    pc.phy.tx("CC 0\n")  # The interval of dummy command is set to 80 ms.
    rxbuf=pc.phy.rx()
    pc.phy.tx("sdi 80\n")  # The interval of dummy command is set to 80 ms.
    pc.phy.tx("sdc 0\n")  # Sending dummy command ON
    pc.phy.tx("slp 16000\n")
    pc.phy.tx("snp 16000\n")
    pc.phy.tx("ssp 16000\n")
    pc.phy.tx("stp 16000\n")
    return pc

def write_Rth():
    pc=PC_Init(com="COM26")
    count = 0
    while pc.linx_num < 2:
        pc.en()
        count += 1
        if count > 5:
            return False
    pc.Initialise()
    pc.phy.tx("rt ff21111 2\n")
    time.sleep(0.5)
    pc.phy.tx("rt fff017e 2\n")
    time.sleep(0.5)
    pc.phy.tx("rt ff80000\n")
    time.sleep(0.5)
    pcrx=pc.phy.rx()
    print('pcrx',pcrx)
    pc.phy.tx("rt ff00000\n")
    time.sleep(0.5)
    pcrx = pc.phy.rx()
    print('pcrx', pcrx)
    pc.phy.tx("rt fff006e 2\n")
    time.sleep(0.5)
    # pc.phy.tx("rt ff91111 2\n")
    # time.sleep(1)
    # pc.phy.tx("rt ff01234 2\n")
    # time.sleep(0.5)
    pc.phy.tx("rt fff017e 2\n")
    time.sleep(0.5)
    pc.phy.tx("rt ff00000 2\n")
    time.sleep(0.5)
    pcrx = pc.phy.rx()
    print('pcrx', pcrx)
    pc.phy.tx("rt fff016e 2\n")
    time.sleep(0.5)
    pc.phy.tx("rt ff00000 2\n")
    time.sleep(0.5)
    pcrx = pc.phy.rx()
    print('pcrx', pcrx)
    pc.phy.tx("rt fff0000 2\n")



def main():    
    print("\n%s\n*%sTest RT!%s*\n%s" %("* "*36, " "*17, " "*18, "* "*36))
    write_Rth()
    return

if __name__ == "__main__":
    main()
    exit()

