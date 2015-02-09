import threading
import time
from config import *

class SensorDataHandler:
    def __init__(self, map_info, simulator):
        self.map_info = map_info
        self.simulator = simulator

        # self.receiver_buffer = receiver_buffer

    # def get_robot_direction(self):
    #     return self.sensor_simulator.get_robot_direction()
    #
    # def get_robot_location(self):
    #     return self.sensor_simulator.get_robot_location()
    #
    # def get_front_middle(self):
    #     return self.sensor_simulator.get_front_middle()
    #
    # def get_front_left(self):
    #     return self.sensor_simulator.get_front_left()
    #
    # def get_front_right(self):
    #     return self.sensor_simulator.get_front_right()

    def update_map(self, sensor_data):
        print("[Thread] ", threading.current_thread())
        print("Updating map...")
        direction = sensor_data.robot_direction
        robot_location = sensor_data.robot_location
        front_middle = sensor_data.distance['front_middle']
        front_left = sensor_data.distance['front_left']
        front_right = sensor_data.distance['front_right']
        print("front middle: ", front_middle)
        # if front_middle:
        if direction == 'E':
            sensor_location = [robot_location[0], robot_location[1]+1]
            self.update_map_by_sensor_data(sensor_location, 'E', front_middle, sensor_range['front_middle'])
        elif direction == 'W':
            sensor_location = [robot_location[0], robot_location[1]-1]
            self.update_map_by_sensor_data(sensor_location, 'W', front_middle, sensor_range['front_middle'])
        elif direction == 'N':
            sensor_location = [robot_location[0]-1, robot_location[1]]
            self.update_map_by_sensor_data(sensor_location, 'N', front_middle, sensor_range['front_middle'])
        elif direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]]
            self.update_map_by_sensor_data(sensor_location, 'S', front_middle, sensor_range['front_middle'])
        else:
            print("    [ERROR] Invalid direction!")
            return
        print('[Thread] ', threading.current_thread(), 'Giving up control')
        time.sleep(1)

    def update_map_by_sensor_data(self, sensor_location, direction, distance, sensor_capability):
        print("distance:", distance)
        if direction == 'E':
            for i in range(distance):
                print("x=", sensor_location[0], " y=", sensor_location[1]+i+1)
                self.map_info.map[sensor_location[0]][sensor_location[1]+i+1] = 1
                self.simulator.put_map(sensor_location[0], sensor_location[1]+i+1)
            if distance + sensor_location[1] < 19 and distance < sensor_capability:
                self.map_info.map[sensor_location[0]][sensor_location[1]+distance+1] = 1
                self.simulator.put_map(sensor_location[0], sensor_location[1]+distance+1)
        elif direction == 'W':
            for i in range(distance):
                self.map_info.map[sensor_location[0]][sensor_location[1]-i-1] = 1
                self.simulator.put_map(sensor_location[0], sensor_location[1]-i-1)
            if -distance + sensor_location[1] > 0 and distance < sensor_capability:
                self.map_info.map[sensor_location[0]][sensor_location[1]-distance-1] = 1
                self.simulator.put_map(sensor_location[0], sensor_location[1]-distance-1)
        elif direction == 'S':
            for i in range(distance):
                self.map_info.map[sensor_location[0]+i+1][sensor_location[1]] = 1
                self.simulator.put_map(sensor_location[0]+i+1, sensor_location[1]+i+1)
            if distance + sensor_location[1] < 14 and distance < sensor_capability:
                self.map_info.map[sensor_location[0]+distance+1][sensor_location[1]] = 1
                self.simulator.put_map(sensor_location[0]+distance+1, sensor_location[1])
        elif direction == 'N':
            for i in range(distance):
                self.map_info.map[sensor_location[0]-i-1][sensor_location[1]] = 1
                self.simulator.put_map(sensor_location[0]-i-1, sensor_location[1])
            if distance + sensor_location[1] > 0 and distance < sensor_capability:
                self.map_info.map[sensor_location[0]-distance-1][sensor_location[1]] = 1
                self.simulator.put_map(sensor_location[0]-distance-1, sensor_location[1])
        else:
            print("    [ERROR] Invalid direction!")
            return

    # def listen(self):
    #     print("[Sensor] Sensor receiver is listening...")
    #     # some action to transfer json string to SensorData object
    #     while True:
    #         print("[Thread] ", threading.current_thread())
    #         if len(self.receiver_buffer):
    #             self.update_map()
    #         else:
    #             time.sleep(.1)