import psutil
import sys,time
from datetime import datetime
import subprocess

# have to use pip install pywin32 to make it work.
import win32api,win32console,win32gui,win32con

# TODO pyinstaller --onefile cdhAlive.py

class CDH:
    def __init__(self):
        self.cdhAppName="CogentDataHub.exe"
        self.cdhAppPath="C:\Program Files (x86)\Cogent\Cogent DataHub\CogentDataHub.exe"
        self.CdhAliveAppName="cdhAlive.exe"
        self.procCnt=0



    def checkRunning(self,appName):
        for p in psutil.process_iter(attrs=['pid', 'name']):
            processName = appName
            if p.info['name'] == processName:
                self.procCnt += 1
        if self.procCnt >= 3:
            sys.exit()

    def windowCloseDisable(self):
        # disable close button for the console window.
        win32api.SetConsoleTitle("Watch dog for Cogent Datahub by robertcyc@gmail.com >>Radiance Automation<<")
        hwnd = win32console.GetConsoleWindow()
        if hwnd:
            hMenu = win32gui.GetSystemMenu(hwnd, 0)
            if hMenu:
                win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)


#script starts from here
appStart=CDH()
appStart.windowCloseDisable()
appStart.checkRunning(appStart.CdhAliveAppName)

while True:
    try:
        #reset app start counter
        appStart.procCnt =0
        GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print ("{}>> Checking Cogent Datahub status...".format(GCDT))

        for p in psutil.process_iter(attrs=['pid', 'name']):
            processName = appStart.cdhAppName
            if p.info['name'] == processName:
                appStart.procCnt += 1
                print ("{}>> AppCounter={} | {}".format(GCDT,appStart.procCnt,p.info['name']))

        if appStart.procCnt >= 1:
            GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print ("{}>> Cogent Datahub is running just fine.:>".format(GCDT))
        else:
            GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("{}>> Cogent Datahub is NOT running, run it automatically.:>".format(GCDT))
            subprocess.Popen(appStart.cdhAppPath)
            time.sleep(0.5)


    except Exception as err:
        GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print ("{}>> {}".format(GCDT,err))

    time.sleep(60)
