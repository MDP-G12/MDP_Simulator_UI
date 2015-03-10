import time
import socket
from robot import *
from logger import *

import sys


class Connector(Robot):
    def __init__(self):
        self.androMsgNbr    = 0
        self.androMsgNbrUpd = 0
        self.androMsgNbrMod = 100

        family = socket.AF_INET
        socket_type = socket.SOCK_STREAM
        self.socket = socket.socket(family, socket_type)
        self.socket.settimeout(1)
        self.host = '192.168.12.12'

        if '-host' in sys.argv:
            self.host = sys.argv[sys.argv.index('-host')+1]

        self.connected = False
        while not self.connect():
            time.sleep(3)

    def connect(self):
        host = self.host
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

    def send(self, msg, isByte=False):
        if not self.connected:
            self.connect()
        if self.connected:
            if not isByte:
                msg = str.encode(msg)
            verbose("Sending message: \'{}\'".format(msg), tag='RoboConn')
            try:
                self.socket.sendall(msg)
            except Exception:
                verbose("[Error] Unable to send message. Connection loss.", tag='RoboConn', pre='ERR>')
                # self.connected = False

    def receive(self, convert=True, retByte=False):
        if not self.connected:
            self.connect()
        if self.connected:
            try:
                msg = self.socket.recv(1024)
                if msg:
                    if retByte:
                        verbose("Received message", msg, tag='RoboConn')
                        return msg
                    ret = msg.decode()                                      # msg decoded
                    verbose("Received message", ret[:len(ret)-2], tag='RoboConn')
                    if convert:
                        sensor_data_in_str = ret.split(',')         # 3 values: (cm, V, V)
                        s   = sensorConverter()
                        ret = s.getReturnSensorList( sensor_data_in_str )   # list of 5 values in block
                    return ret
            except socket.timeout:
                verbose("No message received.", tag='RoboConn')
        # else:
        #     verbose("[Error] Unable to receive message. Connection loss.")

    # this boy here doesn't wait... or so I think.
    def androListen(self, simulator, exploreFunc, runFunc):
        # if (self.androMsgNbr == self.androMsgNbrUpd):
        #     self.send('RN')
        #     tmp = None
        #     while not tmp:
        #         tmp = self.receive(convert=False, retByte=True)
        #     self.androMsgNbrUpd = int.from_bytes(tmp, 'big')

        # if self.androMsgNbrUpd > self.androMsgNbr:
        #     self.androMsgNbr = (self.androMsgNbr + 1) % self.androMsgNbrMod
        #     self.send( b''.join([str.encode('RT'), bytes([self.androMsgNbr])]), isByte=True )
        #     txt = None
        #     while txt == None:
        #         txt = self.receive(convert=False)
        #     if config.androCmd['Explore'] in txt:
        #         exploreFunc()
        #     elif config.androCmd['Run'] in txt:
        #         runFunc()

        # simulator.master.after( config.androListenInterval, self.androListen, simulator, exploreFunc, runFunc )
        pass


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

    def frMid(self, x):
        if x < 1:
            return config.sensor_range['front_middle']*10
        return self.__lflfCon*x**self.__lflfPow
    
    def frLeft(self, x):
        if x < 1:
            return config.sensor_range['front_left']*10
        return self.__lfCon*x**self.__lfPow-3
    def frRight(self, x):
        if x < 1:
            return config.sensor_range['front_right']*10
        return self.__rgCon*x**self.__rgPow-3
    def lfMid(self, x):
        if x < 1:
            return config.sensor_range['left']*10
        return self.__rgrgCon*x**self.__rgrgPow
    def rgMid(self, x):
        if x < 1:
            return config.sensor_range['right']*10
        return self.__rgrgCon*x**self.__rgrgPow

    # create a list of 5 datas to be returned to handler
    def getReturnSensorList(self, sensor_data_in_str):
        ret = []
        while len(sensor_data_in_str) < config.sensor_nbr:
            sensor_data_in_str.append('0')
        ret.append( self.distToBlock( self.frMid(  int(sensor_data_in_str[1]) ), config.sensor_range['front_middle' ] ) )
        ret.append( self.distToBlock( self.frLeft(  int(sensor_data_in_str[1]) ), config.sensor_range['front_left' ] ) )
        ret.append( self.distToBlock( self.frRight( int(sensor_data_in_str[2]) ), config.sensor_range['front_right'] ) )
        ret.append( self.distToBlock( self.lfMid( int(sensor_data_in_str[3]) ), config.sensor_range['left'] ) )
        ret.append( self.distToBlock( self.rgMid( int(sensor_data_in_str[4]) ), config.sensor_range['right'] ) )
        return ret

    # ASSUMING obstacle will never be too close
    def distToBlock(self, dist, maxRange):
        errCompromise   = 2           # in cm
        distCm = dist // 1
        # block detected within range (1, 2, 3, 4)
        # 1: <12 cm,                    5
        # 2: 12 - 22 cm,                15
        # 3: 22 - 32 cm,                25
        # 4: 32 - 42 cm, and so on      35
        blockRangeLimit = [12, 22, 32, 42, 52, 62]
        ret = 1
        for i in blockRangeLimit:
            if distCm < i:
                break
            ret += 1
        if   ret > maxRange  or  ret > len(blockRangeLimit):
            ret = -maxRange

        verbose(dist, distCm, ret, maxRange, tag='distToBlock', pre='    ', lv='debug')
        return ret

