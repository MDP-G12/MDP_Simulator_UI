# import socket

# serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serversocket.bind(('localhost', 8089))
# serversocket.listen(5) # become a server socket, maximum 5 connections

# connection, address = serversocket.accept()
# connection, address = serversocket.accept()
# while True:
#     buf = connection.recv(1024)
#     if len(buf) > 0:
#         print(address, buf.decode())
#         # break


import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    nbr = 0
    cnt = 0
    mod = 10
    IRead = '77,77,77,77,77'

    def handle(self):
        while True:
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)
            if self.data == b'RN':
                self.request.sendall( bytes([self.nbr]) )
                self.cnt += 1
                if (self.cnt >= self.mod):
                    self.cnt = 0
                    self.nbr = 1
                    # self.nbr = (self.nbr+1) % 100
            elif (self.data == b'I' or
                  self.data == b'F' or
                  self.data == b'R' or
                  self.data == b'L'):
                self.request.sendall(str.encode(self.IRead))
            elif (b'Map' in self.data):
                self.request.sendall(str.encode('[Cmd] Map\r\n'))
            else:
                ipt = input('Send back data: ')
                self.request.sendall(str.encode(ipt))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8008

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()