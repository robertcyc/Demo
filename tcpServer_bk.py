import socket


Host = '127.0.0.1'
Port = 6321

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.setblocking(True)
srv.bind((Host, Port))
srv.listen(5)

def clientHandle(client,addr):
    while True:
        try:
            txt=client.recv(1024)
            if not txt:
                client.close()
            client.send(txt)
            print ("{} {} >> {}".format(addr[0],addr[1],txt.decode())
        except Exception as err:
            print (err)

try:
    print("Server start at {}:{}".format(Host, Port))
    print("Waiting for connection....")

    while True:
        client, addr = srv.accept()
        print("Connected by {}".format(addr))

        while True:
            indata = client.recv(1024)
            if len(indata) == 0:
                #print ("Client sent no data.")
                client.close()
                print("Client closed connection.")
                break
            print("Data Received:{}".format(indata.decode()))

            outdata = "Echo:{}".format(indata.decode())
            client.send(outdata.encode())

except Exception as err:
    print (err)
    input("Press Enter key to exit.")
