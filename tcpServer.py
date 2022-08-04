import socket
import threading
import time
import subprocess
from datetime import datetime

#TODO
# pyinstaller --onefile --icon=pc.ico tcpServer.py

clients=[]

Host = ''
Port = 63210

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.setblocking(True)
srv.bind((Host, Port))
srv.listen(5)

# commands to run

def runCommands(cmd):
    if cmd == 'notepad':
        subprocess.Popen("notepad.exe")
    if cmd == 'explorer':
        subprocess.Popen("explorer.exe")

    pass
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   Date: 2020-04-29
#   Function: get current IP address
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def currentIP():
    # retrive current ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # it doesn't matter what ip address you put in.(10.255.255.255)
    s.connect(('10.255.255.255', 1))
    currIP = s.getsockname()[0]
    s.close()
    return currIP

def GCDT():
    # get current date and time.
    now = datetime.now()
    dnt = now.strftime("[%Y-%m-%d %H:%M:%S]")
    return dnt

def clientHandler(client,addr):
    while True:
        try:
            text=client.recv(8192)
            if not text:
                #remove client's ip and port from the list
                #if the client enter no data.
                popItem = addr[0] + ":" + str(addr[1])
                for idx, itm in enumerate(clients):
                    if itm == popItem:
                        clients.pop(idx)
                print("{} {}:{} >> Client disconnected.".format(GCDT(), addr[0], addr[1]))
                client.close()
                break

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            runCommands(text.decode())
            # show how many clients ONLINE.
            if text.decode() == 'show clients':
                # print (str(clients))
                client.send(str(clients).encode())
                print("{} {}:{} | RX >> {}".format(GCDT(), addr[0], addr[1], text.decode()))
            elif text.decode() == "arp":
                ret = subprocess.Popen("arp -a", stdout=subprocess.PIPE)
                for line in ret.stdout:
                    # print(line.decode('big5', errors='ignore'))
                    client.sendall(line)
                #read a file and send
                # with open("note.txt", "r") as f:
                #     fileDat = f.read()
                #     client.sendall(fileDat.encode())
            elif text.decode()=="ipconfig":
                ret = subprocess.Popen("ipconfig /all", stdout=subprocess.PIPE)
                for line in ret.stdout:
                    # print(line.decode('big5', errors='ignore'))
                    client.sendall(line)

            else:
                client.send(text)
                print("{} {}:{} | RX >> {}".format(GCDT(), addr[0], addr[1], text.decode()))

        except Exception as err:
            popItem=addr[0]+":"+str(addr[1])
            for idx,itm in enumerate(clients):
                if itm==popItem:
                    # print ("Index:{}".format(idx))
                    clients.pop(idx)

            print ("{} {}:{} >> Client disconnected.".format(GCDT(),addr[0],addr[1]))
            print ("{} Clients ONLINE:{}".format(GCDT(),clients))
            client.close()
            print("{} TCP Socket Server IP:Port | {}:{}".format(GCDT(),currentIP(), Port))
            #clients.pop(addr[0])
            # print ("Clients IP:{}".format(clients))
            break

try:
    print("{} TCP Socket Server IP:Port | {}:{}".format(GCDT(),currentIP(), Port))
    print("{} Waiting for TCP Socket client connection....".format(GCDT()))

    while True:
        client,addr=srv.accept()
        clients.append(addr[0]+":"+str(addr[1]))
        print ("{} Connected from {}".format(GCDT(),addr))
        t=threading.Thread(target=clientHandler,args=(client,addr,))
        t.start()

except Exception as err:
    print (err)
    input("Press Enter key to exit.")
