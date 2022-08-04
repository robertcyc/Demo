import pyodbc
import time
from datetime import datetime
import threading
import requests
import os,sys
import psutil
from icmplib import ping


# have to use pip install pywin32 to make it work.
import win32api,win32console,win32gui,win32con

#TODO list
#pyinstaller --onefile --icon=lineStatus.ico GwWatchDog.py

class ftcDbQry:
    def __init__(self):
        self.disConnCnt=0
        self.dateTimeList=[]
        self.GwName=''
        self.GwIp=''
        self.GwConnStr=''
        self.GwQryStr=''
        self.lineCnt=0
        self.fileStr=[]

        #how much time for sending err message.
        # send error message to line every one hour.
        self.GwRetryCnt=60 #60 minutes


        # disable close button for the console window.
        win32api.SetConsoleTitle("Watch dog for Gateway IPC by robertcyc@gmail.com >>Radiance Automation<<")
        hwnd=win32console.GetConsoleWindow()
        if hwnd:
            hMenu=win32gui.GetSystemMenu(hwnd,0)
            if hMenu:
                win32gui.DeleteMenu(hMenu,win32con.SC_CLOSE,win32con.MF_BYCOMMAND)
        pass

    def goPing(self):
        host = ping(self.GwIp, timeout=1)
        return host.is_alive

    def readFile(self):
        with open('ftcGwCfg.txt', 'r') as f:
            for line in f.readlines():
                self.fileStr.append(line.rstrip())
        self.GwName=self.fileStr[0]
        self.GwIp = self.fileStr[1]
        self.GwConnStr = self.fileStr[2]
        self.GwQryStr=self.fileStr[3]
        # print (self.GwName, self.GwIp, self.GwConnStr)


    def lineMsg(self, msg):

        GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ACCESS_TOKEN = 'NUsuMwT8RIA8SlcuhX6UUhnMEXG3ywLA8fprebHPEHQ'
        MESSAGE = msg
        URL = 'https://notify-api.line.me/api/notify'
        LINE_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + ACCESS_TOKEN}
        # TEXT only
        MESSAGE_FIELD = {'message': MESSAGE}
        # Text + Sticker
        # MESSAGE_FIELD = {'message': MESSAGE,'stickerPackageId':2,'stickerId':42}
        try:
            response = requests.post(url=URL, headers=LINE_HEADERS, data=MESSAGE_FIELD)
            sts = response.status_code
            if (sts == 200):
                print("{} >> LINE Notify:訊息已傳送 (Success/200).".format(GCDT))
            if (sts == 400):
                print("{} >> LINE Notify:訊息傳送失敗 (Unauthorized request/400).".format(GCDT))
            if (sts == 401):
                print("{} >> LINE Notify:訊息傳送失敗 (Invalid access token/401).".format(GCDT))

        except requests.exceptions.RequestException:
            print ("{} >> No Internet.:<".format(GCDT))
            pass

    def dbQry(self,key,value):
        # check Database connection.
        try:
            GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("{} >> Connecting to {} Database...".format(GCDT,key))
            cnxn = pyodbc.connect(value)
            cursor = cnxn.cursor()
            qryStr = "select top 1 * from CogentDatahub order by 'Datetime' DESC"
            cursor.execute(qryStr)
            rows = cursor.fetchall()

            for row in rows:
                print("{} >> Table Data >> {} | {} ".format(GCDT,row.Datetime, row.LineStatus))
                if len(self.dateTimeList)>=3:
                    self.dateTimeList.append(row.Datetime)
                    self.dateTimeList.pop(0)

                    if self.dateTimeList[0] == self.dateTimeList[2]:
                        self.lineCnt+=1
                        msg="{} >> {} DataBase Data is not updating, check the status of Cogent Datahub.(Retry:{})".format(GCDT,key,self.lineCnt)
                        print (msg)

                        if self.lineCnt>=self.GwRetryCnt:
                            print (msg)
                            FTC.lineMsg(msg)
                            self.lineCnt=0
                        else:
                            pass
                            # print("{} >> {} Database Status OK (Retry:{})".format(GCDT, key,self.lineCnt))

                else:
                    self.dateTimeList.append(row.Datetime)
                    print ("{} >> {} Database status OK (Retry:{})".format(GCDT, key,self.lineCnt))

            # print ("DateTimeList:{}".format(self.dateTimeList))
            cursor.close()
            time.sleep(1)

        except Exception as err:
            GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg="{} >> err".format(GCDT)
            print (msg)
            FTC.lineMsg(msg)
            time.sleep(1)
            pass

    def run(self):
        try:
            t = threading.Thread(target=self.dbQry,args=(self.GwName,self.GwConnStr,))
            t.start()
            time.sleep(1)
            # print (threading.enumerate())
            t.join()

        except Exception as err:
            print ("Something goes wrong...!")
            time.sleep(1)
            pass

# Script starts from here

#Date: 2021-07-08
# to check whether program is running or not.
# only allow this program to run once.



procRunning=0
procCnt=0
gwRetryCnt=0

for p in psutil.process_iter(attrs=['pid','name']):
    processName="GwWatchDog.exe"
    if p.info['name']==processName:
        procCnt+=1
if procCnt>=3:
    sys.exit()
else:
    try:
        FTC=ftcDbQry()
        GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print ("{} >> Loading cfg file...".format(GCDT))
        FTC.readFile()
        time.sleep(0.5)
    except Exception as err:
        print("{} >> Unable to find ftcGwCfg.txt file.:<".format(GCDT))


    while True:
        #checking host connection
        GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print ("{} >> Connecting to {} ({}) Gateway PC (Retry:{})".format(GCDT,FTC.GwName,FTC.GwIp,gwRetryCnt))
        if FTC.goPing():
            FTC.run()
            gwRetryCnt=0
        else:
            gwRetryCnt+=1
            GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("{} >> Unable to connect {} ({}) Gateway PC".format(GCDT, FTC.GwName, FTC.GwIp))
            print("{} >> Will reconnect after 60 seconds.:>".format(GCDT))
            if gwRetryCnt==FTC.GwRetryCnt:
                GCDT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                msg = "{} >> Unable to reach {} ({}) Gateway PC.".format(GCDT, FTC.GwName,FTC.GwIp)
                FTC.lineMsg(msg)
                gwRetryCnt=0

        time.sleep(60)

