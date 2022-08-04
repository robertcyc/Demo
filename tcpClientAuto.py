import socket
from datetime import datetime
import time
import random

#TODO
# pyinstaller --onefile --icon=client.ico --clean tcpClient.py


try:
    HOST=input("TCP Socket Server IP:")
    PORT=int(input("TCP Socket Server Port:"))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        randX=random.randint(0,1000)
        now=datetime.now()
        gdt=now.strftime("%Y-%m-%d %H:%M:%S")
        # outdata = input('Input a command: ')
        # print('Data TX >> ' + outdata)
        # s.send(outdata.encode())
        # indata = s.recv(1024)
        print ("Data TX >> {}".format(gdt))
        s.send(gdt.encode())

        indata=s.recv(1024)
        print('Data RX >> ' + indata.decode())
        time.sleep(5)
except Exception as err:
    print (err)
    pass
