from config import *
from sensor_data import *
import time
import threading


class SensorSimulator():
    def __init__(self, map_info, buffer):

        self.map_info = map_info
        self.buffer = buffer

    def get_robot_location(self):
        return self.map_info.robot_location

    def get_robot_direction(self):
        return self.map_info.robot_direction

    def get_front_middle(self):
        detect_range = sensor_range['front_middle']
        robot_location = self.get_robot_location()
        direction = self.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0], robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'E', detect_range)
        if direction == 'W':
            sensor_location = [robot_location[0], robot_location[1]-1]
            return self.get_sensor_data(sensor_location, 'W', detect_range)
        if direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'S', detect_range)
        if direction == 'N':
            sensor_location = [robot_location[0]-1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'N', detect_range)
        else:
            print("    [ERROR] Invalid direction!")

    def get_front_left(self):
        detect_range = sensor_range['front_left']
        robot_location = self.get_robot_location()
        direction = self.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0]-1, robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'E', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0]+1, robot_location[1]-1]
            return self.get_sensor_data(sensor_location, 'W', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0]-1, robot_location[1]-1]
            return self.get_sensor_data(sensor_location, 'N', detect_range)
        else:
            print("    [ERROR] Invalid direction!")

    def get_front_right(self):
        detect_range = sensor_range['front_right']
        robot_location = self.get_robot_location()
        direction = self.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0]+1, robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'E', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0]-1, robot_location[1]-1]
            return self.get_sensor_data(sensor_location, 'W', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]-1]
            return self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0]-1, robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'N', detect_range)
        else:
            print("    [ERROR] Invalid direction!")

    def get_left(self):
        pass

    def get_right(self):
        pass

    def get_sensor_data(self, location, direction, detect_range):
        dis = 0
        # print("location:", location)
        # print("direction:", direction)
        # print("detect range:", detect_range)
        if direction == 'E':
            while location[1]+dis < 19 and not self.map_info.map_real[location[0]][location[1]+dis+1] and dis < detect_range:
                dis += 1
        if direction == 'W':
            while location[1]-dis > 0 and not self.map_info.map_real[location[0]][location[1]-dis-1] and dis < detect_range:
                dis += 1
        if direction == 'S':
            while location[0]+dis < 14 and not self.map_info.map_real[location[0]+dis+1][location[1]] and dis < detect_range:
                dis += 1
        if direction == 'N':
            while location[0]-dis > 0 and not self.map_info.map_real[location[0]-dis-1][location[1]] and dis < detect_range:
                dis += 1
        print("dis:", dis)
        return dis

    def send_sendsor_data(self):
        last_robot_location = []
        last_robot_direction = ''
        while True:
            self.map_info.map_lock.acquire()
            print("[Map Lock] Locked by ", threading.current_thread())
            print("[Map Info] Location: ", self.map_info.robot_location)
            print("[Map Info] Direction: ", self.map_info.robot_direction)
            print("[Map Info] Last location: ", last_robot_location)
            print("[Map Info] Last direction: ", last_robot_direction)
            if not (self.map_info.robot_location == last_robot_location and self.map_info.robot_direction == last_robot_direction):
                data_to_send = SensorData(self.get_robot_location(), self.get_robot_direction(),
                                          {'front_middle': self.get_front_middle(),
                                           'front_left': self.get_front_left(),
                                           'front_right': self.get_front_right()})
                last_robot_direction = self.get_robot_direction()
                last_robot_location = []+self.get_robot_location()
                print("Robot position updated!")
                # self.buffer_lock.acquire()
                print("[Sensor] Sending data to buffer")
                self.buffer.put(data_to_send)
                print("[Buffer] size = ", self.buffer.qsize())
                # self.buffer_lock.release()
            else:
                print("[Sensor] Robot is not moving")
            self.map_info.map_lock.release()
            print("[Map Lock] Released by ", threading.current_thread())
            print('[Thread] ', threading.current_thread(), 'Giving up control')
            time.sleep(1)