import time
import threading
from config import *


class SensorSimulator():
    def __init__(self, map_info, simulator, event_queue):

        self.command_sequence = []
        # self.command_sequence = ['move', 'move', 'move', 'move',
        #                          'move', 'move', 'left', 'move',
        #                          'right', 'move', 'move', 'move',
        #                          'left', 'move', 'move', 'right',
        #                          'move', 'move', 'move', 'move',
        #                          'left', 'move', 'move', 'move',
        #                          'move', 'move', 'move', 'move',
        #                          'move', 'move', 'move', 'move',
        #                          'move', 'move', 'move', 'move']
        self.next_command_index = 0
        self.map_info = map_info
        self.simulator = simulator
        self.event_queue = event_queue

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
        print("location:", location)
        print("direction:", direction)
        print("detect range:", detect_range)
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
            while location[1]-dis > 0 and not self.map_info.map_real[location[0]-dis-1][location[0]] and dis < detect_range:
                dis += 1
        print("dis:", dis)
        return dis

    def update_map(self):
        # while True:
        print("[Thread] ", threading.current_thread())
        print("Updating map...")
        direction = self.get_robot_direction()
        robot_location = self.get_robot_location()
        front_middle = self.get_front_middle()
        front_left = self.get_front_left()
        front_right = self.get_front_right()
        print(front_middle)
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
        time.sleep(1)

    def update_map_by_sensor_data(self, sensor_location, direction, distance, sensor_capability):
        print("distance:", distance)
        if direction == 'E':
            for i in range(distance):
                self.map_info.map_explored[sensor_location[0]][sensor_location[1]+i+1] = 1
                self.simulator.put_map(sensor_location[0], sensor_location[1]+i+1)
            if distance + sensor_location[1] < 19 and distance < sensor_capability:
                self.map_info.map_explored[sensor_location[0]][sensor_location[1]+distance+1] = 1
                self.simulator.put_map(sensor_location[0], sensor_location[1]+distance+1)
        elif direction == 'W':
            for i in range(distance):
                self.map_info.map_explored[sensor_location[0]][sensor_location[1]-i-1] = 1
                self.simulator.put_map(sensor_location[0], sensor_location[1]-i-1)
            if -distance + sensor_location[1] > 0 and distance < sensor_capability:
                self.map_info.map_explored[sensor_location[0]][sensor_location[1]-distance-1] = 1
                self.simulator.put_map(sensor_location[0], sensor_location[1]-distance-1)
        elif direction == 'S':
            for i in range(distance):
                self.map_info.map_explored[sensor_location[0]+i+1][sensor_location[1]] = 1
                self.simulator.put_map(sensor_location[0]+i+1, sensor_location[1]+i+1)
            if distance + sensor_location[1] < 14 and distance < sensor_capability:
                self.map_info.map_explored[sensor_location[0]+distance+1][sensor_location[1]] = 1
                self.simulator.put_map(sensor_location[0]+distance+1, sensor_location[1])
        elif direction == 'N':
            for i in range(distance):
                self.map_info.map_explored[sensor_location[0]-i-1][sensor_location[1]] = 1
                self.simulator.put_map(sensor_location[0]-i-1, sensor_location[1])
            if distance + sensor_location[1] > 0 and distance < sensor_capability:
                self.map_info.map_explored[sensor_location[0]-distance-1][sensor_location[1]] = 1
                self.simulator.put_map(sensor_location[0]-distance-1, sensor_location[1])
        else:
            print("    [ERROR] Invalid direction!")
            return



