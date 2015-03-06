import time
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
        while not self.connect():
            time.sleep(1)

    def connect(self):
        host = '192.168.12.12'
        port = 8008
        try:
            self.socket.connect((host, port))
        except Exception:
            verbose("ERROR: Unable to establish connection.", tag='RoboConn', pre='ERR>')
            return False
        else:
            self.connected = True
            verbose("Connection established.", tag='RoboConn')
        return True

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

    def receive(self, convert=True):
        if not self.connected:
            self.connect()
        if self.connected:
            try:
                msg = self.socket.recv(1024)
                if msg:
                    ret = msg.decode()                                      # msg decoded
                    verbose("Received message", ret, tag='RoboConn')
                    if convert:
                        sensor_data_in_str = ret.split(',')         # 3 values: (cm, V, V)
                        s   = sensorConverter()
                        ret = s.getReturnSensorList( sensor_data_in_str )   # list of 5 values in block
                    return ret
            except socket.timeout:
                verbose("No message received.", tag='RoboConn')
        # else:
        #     verbose("[Error] Unable to receive message. Connection loss.")


class sensorConverter:
    __lfCon =   config.lfCon
    __lfPow =   config.lfPow
    __rgCon =   config.rgCon
    __rgPow =   config.rgPow
        
    __lflfCon = config.lflfCon
    __lflfPow = config.lflfPow
    __rgrgCon = config.rgrgCon
    __rgrgPow = config.rgrgPow


    def setParam(self, lfCon=None, lfPow=None, rgCon=None, rgPow=None):
        if not lfCon:
            self.__lfCon = lfCon
        if not lfPow:
            self.__lfPow = lfPow
        if not rgCon:
            self.__rgCon = rgCon
        if not rgPow:
            self.__rgPow = rgPow
    
    def frLeft(self, x):
        if not x:
            return 0
        return self.__lfCon*x**self.__lfPow
    def frRight(self, x):
        if not x:
            return 0
        return self.__rgCon*x**self.__rgPow
    def lfMid(self, x):
        if not x:
            return 0
        return self.__lflfCon*x**self.__lflfPow
    def rgMid(self, x):
        if not x:
            return 0
        return self.__rgrgCon*x**self.__rgrgPow

    # create a list of 5 datas to be returned to handler
    def getReturnSensorList(self, sensor_data_in_str):
        ret = []
        while len(sensor_data_in_str) < config.sensor_nbr:
            sensor_data_in_str.append('0')
        ret.append( self.distToBlock( float(sensor_data_in_str[0]), config.sensor_range['front_middle'] ) )
        ret.append( self.distToBlock( self.frLeft(  int(sensor_data_in_str[1]) ), config.sensor_range['front_left' ] ) )
        ret.append( self.distToBlock( self.frRight( int(sensor_data_in_str[2]) ), config.sensor_range['front_right'] ) )
        ret.append( self.distToBlock( self.lfMid( int(sensor_data_in_str[3]) ), config.sensor_range['left'] ) )
        ret.append( self.distToBlock( self.rgMid( int(sensor_data_in_str[4]) ), config.sensor_range['right'] ) )
        return ret

    def distToBlock(self, dist, maxRange):
        errCompromise   = 1           # in cm
        offset          = 10
        # no block detected (5 blocks above)
        if   dist+errCompromise > (maxRange*10):
            return -maxRange
        # block detected within range (1, 2, 3, 4)
        # 1: <10 cm,
        # 2: 10 - 19 cm,
        # 3: 20 - 29 cm,
        # 4: 30 - 39 cm, and so on
        else:
            return (dist + offset + errCompromise) // 10
        # ASSUMING obstacle will never be too close
