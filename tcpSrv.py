import socket
import time
import SocketServer
import threading


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        BUFSIZE = 1024
        print('Connect from: {0}:{1}'.format(self.client_address[0], self.client_address[1]))
        while (True):
            data = self.request.recv(BUFSIZE)
            self.request.sendall(data)
            time.sleep(0.1)

    def finish(self):
        print("client {0}:{1} disconnect!".format(self.client_address[0], self.client_address[1]))


def connect():
    HOST = socket.gethostname()
    PORT = 8000

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print('Server is starting up...')
    print('Host: {0}, listen to port: {1}'.format(HOST, PORT))


if __name__ == '__main__':
    connect()