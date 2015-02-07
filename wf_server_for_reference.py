import socket

#reference: https://docs.python.org/2/library/socket.html

HOST = ''     # Symbolic name meaning all available interfaces
PORT = 8008              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#set the wf address reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print "[info] WF Binds to HOST " + str(HOST) +", PORT: " + str(PORT)
s.bind((HOST, PORT))

print "[info] WF Server starts listening"
s.listen(1)

conn, addr = s.accept()
print "[info] WF Connection accepted"

print 'Connected by', addr

information = ["11111", "22222", "33333"]
i=0
while 1:
    print "Sending", information[i]
    conn.sendall(information[i])
    i = (i+1)%3

    data = conn.recv(1024)
    print "Wifi: ", data
    
    if (data == "exit"): break;

conn.close()