import time
import queue
from config import *


class SensorSimulator():
    def __init__(self, map_info, event_queue):
        self.map_info       = map_info
        self.event_queue    = event_queue

        # Testing 
        # self.command_sequence =
        #             ['move', 'move', 'move', 'move',
        #              'move', 'move', 'left', 'move',
        #              'right', 'move', 'move', 'move',
        #              'left', 'move', 'move', 'right',
        #              'move', 'move', 'move', 'move',
        #              'left', 'move', 'move', 'move',
        #              'move', 'move', 'move', 'move',
        #              'move', 'move', 'move', 'move',
        #              'move', 'move', 'move', 'move']
        # self.execute_command()

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
            ret = self.get_sensor_data(sensor_location, 'E', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0], robot_location[1]-1]
            ret = self.get_sensor_data(sensor_location, 'W', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]]
            ret = self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0]-1, robot_location[1]]
            ret = self.get_sensor_data(sensor_location, 'N', detect_range)
        else:
            print("    [ERROR] Invalid direction!", self.get_robot_direction(), sep='; ')
            return
        return [sensor_location, ret]

    def get_front_left(self):
        detect_range = sensor_range['front_left']
        robot_location = self.get_robot_location()
        direction = self.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0]-1, robot_location[1]+1]
            ret = self.get_sensor_data(sensor_location, 'E', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0]+1, robot_location[1]-1]
            ret = self.get_sensor_data(sensor_location, 'W', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]+1]
            ret = self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0]-1, robot_location[1]-1]
            ret = self.get_sensor_data(sensor_location, 'N', detect_range)
        else:
            print("    [ERROR] Invalid direction!")
            return
        return [sensor_location, ret]

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

    # ----------------------------------------------------------------------
    #   Function get_sensor_data
    # ----------------------------------------------------------------------
    # return:
    #   integer value indicating distance of first obstacle before the sensor
    #   negative integer value if no obstacles is detected
    # 
    # parameter:
    #   location        -  [row, column]; location of sensor
    #   direction       -  char; direction where the sensor is facing to
    #   detect_range    -  max dist. the sensor can detect in a straight line
    # ----------------------------------------------------------------------
    def get_sensor_data(self, location, direction, detect_range):
        dis = 1
        if direction == 'E':
            # while (within boundary) and (block is free) and (not exceeding sensor range)
            while location[1]+dis < 19  and self.map_info.isFree(location[0],location[1]+dis)  and dis <= detect_range:
                dis += 1
        elif direction == 'W':
            while location[1]-dis > 0   and self.map_info.isFree(location[0],location[1]-dis)  and dis <= detect_range:
                dis += 1
        elif direction == 'S':
            while location[0]+dis < 14  and self.map_info.isFree(location[0]+dis,location[1])  and dis <= detect_range:
                dis += 1
        elif direction == 'N':
            while location[0]-dis > 0   and self.map_info.isFree(location[0]-dis,location[1])  and dis <= detect_range:
                dis += 1
        if (dis > detect_range):
            return -detect_range
        return dis


    # ----------------------------------------------------------------------
    # a thread-safe queue implementation from Phyton
    # a testing function
    def execute_command(self):
        command_queue = queue.Queue()
        for x in self.command_sequence:
            command_queue.put(x)

        while not command_queue.empty():
            next_command = command_queue.get()
            self.event_queue.put(next_command)
            print("Command: " + next_command)
