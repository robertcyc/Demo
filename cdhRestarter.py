# Date: 2022-08-03
# Function: restart Cogent datahub when it is not running.
#
import time
import win32con
import win32gui,win32console,win32api
import subprocess,sys,psutil
from datetime import datetime
from mylogs import pyLogger

#pyinstaller --onefile --icon=restart.ico cdhRestarter.py

def selfCheck():
    procCnt = 0
    # allow only one running program instance.
    for p in psutil.process_iter(attrs=['pid', 'name']):
        processName = "cdhRestarter.exe"
        if p.info['name'] == processName:
            procCnt += 1
    if procCnt >= 3:
        sts.logger.warning("cdhRestarter.exe has already started.")
        sys.exit()
    else:
        # disable close button for the console window.

        win32api.SetConsoleTitle("Cogent Datahub Restarter by robert@ractw.com.tw | Radiance Automation")
        hwnd = win32console.GetConsoleWindow()
        if hwnd:
            hMenu = win32gui.GetSystemMenu(hwnd, 0)
            if hMenu:
                win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)
                sts.logger.info("Disable close button for the console window.")

def checkRunning():
    procCnt=0
    cdhAppName = "CogentDataHub.exe"
    cdhAppPath = "C:\Program Files (x86)\Cogent\Cogent DataHub\CogentDataHub.exe"
    for p in psutil.process_iter(attrs=['pid', 'name']):
        processName = cdhAppName
        if p.info['name'] == processName:
            procCnt += 1
    if procCnt<=0:
        # call Cogent Datahub main program
        GCDT = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        print("{}Cogent Datahub is not running, restart it.".format(GCDT))
        sts.logger.info("Cogent Datahub restarted.")
        cdhAppPath = "C:\Program Files (x86)\Cogent\Cogent DataHub\CogentDataHub.exe"
        subprocess.Popen(cdhAppPath)

# script starts from here

sts=pyLogger("cdhRestarter")
cdhCnt=0
selfCheck()
GCDT = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
print("{}Cogent Datahub Restarter started.".format(GCDT))
sts.logger.info("Cogent Datahub Restarter started.")

while True:

    try:
        #find window's title.
        hwnd=win32gui.FindWindow(None,"Cogent DataHub")
        #hwnd = win32gui.FindWindow(None, "Windows 工作管理員")
        if hwnd:
            GCDT = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            win32gui.SendMessage(hwnd,win32con.WM_CLOSE,0,0)
            print ("{}Terminating Cogent Datahub Pop-up window.".format(GCDT))
            sts.logger.info("Terminating Cogent Datahub Pop-up window.")
            time.sleep(1)
            # call Cogent Datahub main program
            GCDT = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            print("{}Cogent Datahub is not running, restart it.".format(GCDT))
            sts.logger.info("Cogent Datahub is not running, restart it.")

            cdhAppPath = "C:\Program Files (x86)\Cogent\Cogent DataHub\CogentDataHub.exe"
            subprocess.Popen(cdhAppPath)
        else:
            pass
    except Exception as err:
        GCDT = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        print("{} {}...".format(GCDT,err))
        sts.logger.error(err)
        #check Cogent Datahub running or not every 60 seconds., if not, run it.
    if cdhCnt>=5:
        cdhCnt=0
        checkRunning()
    else:
        cdhCnt+=1
    time.sleep(1)
