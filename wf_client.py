
import socket
import sys

HOST = '192.168.12.12'    # This one should be 192.168.9.9 - our Raspberry Pi server address
PORT = 8008              # The same port as used by the server

s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)
while 1:
    #s.sendall("{\"destination\": \"N\"}")
    #data = s.recv(1024)
    #print 'Received', data
    dataToBeSent = raw_input("Input string: ")
    s.sendall(dataToBeSent)
    # if dataToBeSent == "1":
    #     s.sendall("a1")    
    # elif dataToBeSent == "2":
    #     s.sendall("a2")
    # elif dataToBeSent == "3":
    #     s.sendall("a3")
    # elif dataToBeSent == "4":
    #     s.sendall("a4")
    # elif dataToBeSent == "5":
    #     s.sendall("a5")
    # elif dataToBeSent == "6":
    #     s.sendall("a6")
    # elif dataToBeSent == "7":
    #     s.sendall("a7")
    # elif dataToBeSent == "8":
    #     s.sendall("a8")
    # else:
    #     s.sendall("a0")
    #s.sendall(dataToBeSent)
    data = s.recv(1024)
    print 'Received', repr(data)
s.close()
