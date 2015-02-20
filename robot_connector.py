import socket
from robot import *
from logger import *


class Connector(Robot):
    def __init__(self):

        family = socket.AF_INET
        socket_type = socket.SOCK_STREAM
        self.socket = socket.socket(family, socket_type)
        self.socket.settimeout(1)
        self.connected = False
        self.connect()

    def connect(self):
        host = '192.168.12.12'
        port = 8008
        try:
            self.socket.connect((host, port))
        except Exception:
            verbose("ERROR: Unable to establish connection.", tag='RoboConn', pre='ERR>')
        else:
            self.connected = True
            verbose("Connection established.", tag='RoboConn')

    def send(self, msg):
        if not self.connected:
            self.connect()
        if self.connected:
            verbose("Sending message: \'{}\'".format(msg), tag='RoboConn')
            try:
                self.socket.sendall(str.encode(msg))
            except Exception:
                verbose("[Error] Unable to send message. Connection loss.", tag='RoboConn', pre='ERR>')
                # self.connected = False

    def receive(self):
        if not self.connected:
            self.connect()
        if self.connected:
            try:
                msg = self.socket.recv(1024)
                if msg:
                    msg_decoded = msg.decode()
                    verbose("Received message", msg_decoded, tag='RoboConn')
                    sensor_data_in_str = msg.split(',')
                    sensor_data = []
                    for data in sensor_data_in_str:
                        sensor_data.append(int(data))
                    return sensor_data
            except socket.timeout:
                verbose("No message received.", tag='RoboConn')
        # else:
        #     verbose("[Error] Unable to receive message. Connection loss.")

