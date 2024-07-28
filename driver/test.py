import api,phy

def test():
    pc=api.chain(phy.ser("COM4"))
    if not pc.open(): exit()
    while not pc.en():continue
    pc.phy.tx("sdc 0\n")
    rxbuf=pc.phy.rx()
    print(rxbuf)
    pc.phy.tx("rt ffe0000\n")
    rxbuf = pc.phy.rx()
    print(rxbuf)
if __name__ == "__main__":
    test()
    exit()