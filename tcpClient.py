import socket
import keyboard

#TODO
# pyinstaller --onefile --icon=client.ico --clean tcpClient.py


try:
    HOST=input("TCP Socket Server IP:")
    PORT=int(input("TCP Socket Server Port:"))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        outdata = input('Input a command: ')
        if not outdata:
            continue

        if outdata=='exit' or outdata=="EXIT":
            s.close()
            break

        print('Data TX >> ' + outdata)
        s.send(outdata.encode())

        #data received from server.
        indata = s.recv(8192)
        print('Data RX >> ' + indata.decode())

except Exception as err:
    print (err)
    pass
