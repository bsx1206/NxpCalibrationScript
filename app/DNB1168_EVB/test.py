import threading
import time
    
class DevData():
    def __init__(self, name, reg, phy2count, count2phy):
        self.name = name
        self.reg = reg
        self.phy2count = phy2count
        self.count2phy = count2phy

        self.is_running = False
        self.tid = None
        self.tim = 0
        self.locker = threading.RLock()
        
    def GetName(self):
        return self.name
    
    # thread function
    def Run(self, tim:int = 10):
        assert self.is_running == False
        self.tim = tim
        self.is_running = True
        self.tid = threading.Thread(target=self.thread_run, name=self.name)
        self.tid.start()

    def IsRunning(self):
        self.locker.acquire()
        r = self.is_running
        self.locker.release()
        return r

    def Stop(self):
        if self.is_running == False:
            print("Thread not running")
            return
        self.locker.acquire()
        self.is_running = False
        self.locker.release()
        self.tid.join()
        self.tid = None

    def thread_run(self):
        while self.is_running and self.tim:
            time.sleep(1)
            self.locker.acquire()
            self.tim -= 1
            print("%s: Left %d sec" % (threading.current_thread().name, self.tim))
            self.locker.release()
        print("%s STOPPED" % threading.current_thread().name)
        self.is_running = False
        return 0
    
    # static function
    def GetCount(self, phy: float) -> int:
        return self.phy2count(phy)
    def GetPhysical(self, count: int) -> float:
        return self.count2phy(count)
    
    def voltage2count(volt: float) -> int:
        return int(volt / 2.5 * 4096.0)
    def count2voltage(count: int) -> float:
        return float(count)/4096.0 * 2.5
    def temperature2count(temp: float) -> int:
        return int(temp / 100.0 * 1024.0)
    def count2temperature(count: int) -> float:
        return float(count)/1024.0 * 2.5

if __name__ == "__main__":
    print("\033[0;34;40m%s\033[0m" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    print("\033[0;37;40m%s\033[0m" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    print("\033[0;31;40m%s\033[0m" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    dev_volt = DevData("Volt", 0, DevData.voltage2count, DevData.count2voltage)
    dev_temp = DevData("Temp", 0, DevData.temperature2count, DevData.count2temperature)

    print(dev_volt.GetName())
    print("P2C: 1.5V -> %d" % dev_volt.GetCount(1.5))
    print("C2P: 2000 -> %.2fV" % dev_volt.GetPhysical(2000))
    
    print(dev_temp.GetName())
    print("P2C: 50.0C -> %d" % dev_temp.GetCount(50.0))
    print("C2P: 200 -> %.2fC" % dev_temp.GetPhysical(200))

    dev_temp.Run(5)
    time.sleep(0.5)
    dev_volt.Run(10)
    time.sleep(7.5)
    print("dev_temp is %s" % ("running" if dev_temp.IsRunning() else "stop"))
    print("dev_volt is %s" % ("running" if dev_volt.IsRunning() else "stop"))
    if dev_temp.IsRunning(): dev_temp.Stop()
    if dev_volt.IsRunning(): dev_volt.Stop()
    print("done")
    