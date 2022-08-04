from icmplib import ping,multiping
import time,datetime
import threading
from mylogs import pyLogger


#TODO
# if .exe file is not working, make sure pyinstaller is up-to-date, or install it again.(pip install pyinstaller)
# pyinstaller --onefile --icon=ping.ico myPinger.py
#

class pingIP:
    def __init__(self):
        self.hostList=[]
        self.hostCnt=0
        self.totalAliveHostIp=[]
        self.totalDeadHostIp = []
        self.totalAliveHostCnt = 0
        self.totalDeadHostCnt=0
        self.totalSearchTime=0
        self.hostStatus=[]
        self.logs = pyLogger("PINGER")
        self.gDT=""
        self.ipPool=[]

    def goPing(self,hostIP):
        host=ping(hostIP,timeout=1)
        if host.is_alive:
            print(">>{:<15} | Avg rtt={:<5} ".format(host.address, host.avg_rtt))
            self.totalAliveHostIp.append(host.address)
            self.totalAliveHostCnt += 1
            self.hostStatus.append("{},{},{}".format(self.gDT,host.address,1))
        else:
            self.totalDeadHostIp.append(host.address)
            self.totalDeadHostCnt+=1
            self.hostStatus.append("{},{},{}".format(self.gDT, host.address, 0))
        pass

    def run(self):

        with open('ipCfg.txt', 'r') as f:
            for line in f.readlines():
                self.ipPool.append(line.rstrip())
        self.gDT=datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S]")
        print ("{} Start Searching Hosts...".format(self.gDT))
        #self.logs.logger.info("Start Searching Hosts...")
        startTime = (datetime.datetime.now())
        for host in self.ipPool:
            t = threading.Thread(target=self.goPing, args=(host,))
            t.start()
        t.join()
        endTime=(datetime.datetime.now())
        self.totalSearchTime = endTime-startTime
        time.sleep(1)
        print("{} Total SearchingTime {}".format(self.gDT,self.totalSearchTime))
        print("{} {} Dead Hosts:{}".format(self.gDT,self.totalDeadHostCnt,self.totalDeadHostIp))
        #write host status to a file
        with open("hostSts.txt",'w') as f:
            for line in self.hostStatus:
                f.write(line+"\n")

        self.ipPool.clear()
        self.totalDeadHostIp.clear()
        self.totalAliveHostCnt = 0
        self.totalDeadHostCnt=0
        self.hostStatus.clear()
#++++++++++++++++++++ TEST ZONE +++++++++++++++++++++++++++++
try:
    test123=pingIP()
    test123.logs.logger.info("Program Started.")

    while True:
        test123.run()
        time.sleep(30)
except Exception as err:
    test123.logs.logger.error(err)


