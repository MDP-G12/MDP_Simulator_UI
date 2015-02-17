from logger import *
from robot import *


class RobotSimulator(Robot):
    def __init__(self, handler):
        self.map_info       = handler.map

    def get_front_middle(self):
        detect_range    = config.sensor_range['front_middle']
        robot_location  = self.map_info.get_robot_location()
        direction       = self.map_info.get_robot_direction()
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
            print("    [ERROR] Invalid direction!", self.map_info.get_robot_direction(), sep='; ')
            return
        # return [sensor_location, ret]
        return ret

    def get_front_left(self):
        detect_range = config.sensor_range['front_left']
        robot_location = self.map_info.get_robot_location()
        direction = self.map_info.get_robot_direction()
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
        # return [sensor_location, ret]
        return ret

    def get_front_right(self):
        detect_range = config.sensor_range['front_right']
        robot_location = self.map_info.get_robot_location()
        direction = self.map_info.get_robot_direction()
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
        detect_range = config.sensor_range['left']
        robot_location = self.map_info.get_robot_location()
        direction = self.map_info.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0]-1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'N', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0]+1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0], robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'E', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0], robot_location[1]-1]
            return self.get_sensor_data(sensor_location, 'W', detect_range)
        else:
            print("    [ERROR] Invalid direction!")

    def get_right(self):
        detect_range = config.sensor_range['right']
        robot_location = self.map_info.get_robot_location()
        direction = self.map_info.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0]+1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0]-1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'N', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0], robot_location[1]-1]
            return self.get_sensor_data(sensor_location, 'W', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0], robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'E', detect_range)
        else:
            print("    [ERROR] Invalid direction!")

    # ----------------------------------------------------------------------
    #   Function get_sensor_data
    # ----------------------------------------------------------------------
    # return:
    #   integer value indicating distance of first obstacle before the sensor.
    #   negative integer value if no obstacles is detected
    # 
    # parameter:
    #   location        -  [row, column]; location of sensor
    #   direction       -  char; direction where the sensor is facing to
    #   detect_range    -  max dist. the sensor can detect in a straight line
    # ----------------------------------------------------------------------
    def get_sensor_data(self, location, direction, detect_range):
        # print('detect_range:', detect_range)
        dis = 1
        if direction == 'E':
            # while (within boundary) and (block is free) and (not exceeding sensor range)
            while location[1]+dis < 20  and self.map_info.isFree(location[0],location[1]+dis)  and dis <= detect_range:
                dis += 1
        elif direction == 'W':
            while location[1]-dis >= 0   and self.map_info.isFree(location[0],location[1]-dis)  and dis <= detect_range:
                dis += 1
        elif direction == 'S':
            while location[0]+dis < 15  and self.map_info.isFree(location[0]+dis,location[1])  and dis <= detect_range:
                dis += 1
        elif direction == 'N':
            while location[0]-dis >= 0   and self.map_info.isFree(location[0]-dis,location[1])  and dis <= detect_range:
                dis += 1
        if dis > detect_range:
            dis = -detect_range

        # verbose("    >> get_sensor_data; loc="+location + "; dir="+direction + "; ran="+detect_range + "; ret="+dis, tag='sensor')
        return dis
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    #     Function get_all_sensor_data
    # ----------------------------------------------------------------------
    # return:
    #     a list containing all sensor datas following get_sensor_data() format
    #     the order is as follows:
    #         front_middle,
    #         front_left,
    #         front_right,
    #         left,
    #         right
    # ----------------------------------------------------------------------
    def receive(self):
        return [self.get_front_middle(),
                self.get_front_left(),
                self.get_front_right(),
                self.get_left(),
                self.get_right()]
    # ----------------------------------------------------------------------



    # # ----------------------------------------------------------------------
    # # a thread-safe queue implementation from Phyton
    # # a testing function
    # def execute_command(self):
    #     command_queue = queue.Queue()
    #     for x in self.command_sequence:
    #         command_queue.put(x)

    #     while not command_queue.empty():
    #         next_command = command_queue.get()
    #         self.event_buffer.put(next_command)
    #         print("Command: " + next_command)
    # # ----------------------------------------------------------------------


    # def send_sendsor_data(self):
    #     last_robot_location = []
    #     last_robot_direction = ''
    #     while True:
    #         self.map_info.map_lock.acquire()
    #         print("[Map Lock] Locked by ", threading.current_thread())
    #         print("[Map Info] Location: ", self.map_info.robot_location)
    #         print("[Map Info] Direction: ", self.map_info.robot_direction)
    #         print("[Map Info] Last location: ", last_robot_location)
    #         print("[Map Info] Last direction: ", last_robot_direction)
    #         if not (self.map_info.robot_location == last_robot_location and self.map_info.robot_direction == last_robot_direction):
    #             data_to_send = SensorData(self.map_info.get_robot_location(), self.map_info.get_robot_direction(),
    #                                       {'front_middle': self.get_front_middle(),
    #                                        'front_left': self.get_front_left(),
    #                                        'front_right': self.get_front_right(),
    #                                        'left': self.get_left(),
    #                                        'right': self.get_right()})
    #             last_robot_direction = self.map_info.get_robot_direction()
    #             last_robot_location = []+self.map_info.get_robot_location()
    #             print("Robot position updated!")
    #             # self.event_buffer_lock.acquire()
    #             print("[Sensor] Sending data to buffer")
    #             self.event_buffer.put(data_to_send)
    #             print("[Buffer] size = ", self.event_buffer.qsize())
    #             # self.event_buffer_lock.release()
    #         else:
    #             print("[Sensor] Robot is not moving")
    #         self.map_info.map_lock.release()
    #         print("[Map Lock] Released by ", threading.current_thread())
    #         print('[Thread] ', threading.current_thread(), 'Giving up control')
    #         time.sleep(1)