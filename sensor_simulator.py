import time
from config import *


class SensorSimulator():
    def __init__(self, map_info, event_queue):

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
        if direction == 'E':
            while location[1]+dis < 19 and not self.map_info.map_real[location[0]][location[1]+dis] and dis < detect_range:
                dis += 1
        if direction == 'W':
            while location[1]-dis > 0 and not self.map_info.map_real[location[0]][location[1]-dis] and dis < detect_range:
                dis += 1
        if direction == 'S':
            while location[0]+dis < 14 and not self.map_info.map_real[location[0]+dis][location[1]] and dis < detect_range:
                dis += 1
        if direction == 'N':
            while location[1]-dis > 0 and not self.map_info.map_real[location[0]-dis][location[0]] and dis < detect_range:
                dis += 1
        return dis

    def issue_command(self):

        while self.next_command_index < len(self.command_sequence):
            time.sleep(0)
            next_command = self.command_sequence[self.next_command_index]
            self.event_queue.put(next_command)
            self.next_command_index += 1
            print("Command: " + next_command)
