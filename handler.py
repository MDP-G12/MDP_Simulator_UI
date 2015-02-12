from logger import *
import simulator
import map

class Handler:
    def __init__(self):
        self.map = map.Map()
        self.createSimulator()

    def createSimulator(self):
        self.simulator = simulator.SimulatorUI(self)

        # map_simulator = Simulator(root)

        # map_simulator.algoObject.explore()

        self.simulator.master.mainloop()


    def get_robot_location(self):
        return self.map.get_robot_location()

    def get_robot_direction(self):
        return self.map.get_robot_direction()


    # ----------------------------------------------------------------------
    #   Actions
    # ----------------------------------------------------------------------
    # List of actions that robot can receive
    # ----------------------------------------------------------------------
    def move(self):
        # self.event_queue.put('move')
        self.__do_move()

    def back(self):
        self.event_queue.put('back')

    def left(self):
        self.event_queue.put('left')

    def right(self):
        self.event_queue.put('right')

    def read_sensor(self):
        self.event_queue.put('read')
    # ----------------------------------------------------------------------

    def __move(self):
        # map_info.map_lock.acquire()
        # print("[Map Lock] Locked by ", threading.current_thread())
        print("Action: move forward")
        self.__do_move()

    # unfinished;
    def __back(self):
        print("Action: move backward")
        cur_dir = map_info.robot_direction
        if   map_info.robot_direction == 'N':
            map_info.robot_direction = 'S'
        elif map_info.robot_direction == 'S':
            map_info.robot_direction = 'N'
        elif map_info.robot_direction == 'E':
            map_info.robot_direction = 'W'
        elif map_info.robot_direction == 'W':
            map_info.robot_direction = 'E'
        else:
            print("    [ERROR] Direction undefined!")
        self.__do_move()
        map_info.robot_direction = cur_dir


    def __do_move(self):
        # Getting the next position
        robot_location = self.map.get_robot_location()
        if   map_info.robot_direction == 'N':
                robot_next = [robot_location[0]-1, robot_location[1]]
        elif map_info.robot_direction == 'S':
                robot_next = [robot_location[0]+1, robot_location[1]]
        elif map_info.robot_direction == 'W':
                robot_next = [robot_location[0], robot_location[1]-1]
        elif map_info.robot_direction == 'E':
                robot_next = [robot_location[0], robot_location[1]+1]
        else:
            print("    [ERROR] Direction undefined!")

        # Validating the next position
        if self.valid_pos(robot_next[0], robot_next[1]):
            # Updating robot position value
            [map_info.robot_location[0], map_info.robot_location[1]] = robot_next

            # Updating the map
                # if map_info.robot_direction == 'N':
                #     self.put_robot(map_info.robot_location[0], map_info.robot_location[1], 'N')
                #     for z in range(map_info.robot_location[1]-1, map_info.robot_location[1]+2):
                #         self.put_map(map_info.robot_location[0]+2, z)

                # elif map_info.robot_direction == 'S':
                #     self.put_robot(map_info.robot_location[0], map_info.robot_location[1], 'S')
                #     for z in range(map_info.robot_location[1]-1, map_info.robot_location[1]+2):
                #         self.put_map(map_info.robot_location[0]-2, z)

                # elif map_info.robot_direction == 'W':
                #     self.put_robot(map_info.robot_location[0], map_info.robot_location[1], 'W')
                #     for z in range(map_info.robot_location[0]-1, map_info.robot_location[0]+2):
                #         self.put_map(z, map_info.robot_location[1]+2)

                # elif map_info.robot_direction == 'E':
                #     self.put_robot(map_info.robot_location[0], map_info.robot_location[1], 'E')
                #     for z in range(map_info.robot_location[0]-1, map_info.robot_location[0]+2):
                #         self.put_map(z, map_info.robot_location[1]-2)
        else:
            print("    [WARNING] Not moving due to obstacle or out of bound")

        map_info.map_lock.release()
        print("[Map Lock] Released by ", threading.current_thread())

    def __left(self):
        map_info.map_lock.acquire()
        print("[Map Lock] Locked by ", threading.current_thread())
        print("Action: turn left")
        map_info.robot_direction = DIRECTIONS[(DIRECTIONS.index(map_info.robot_direction)+3) % 4]
        self.put_robot(map_info.robot_location[0], map_info.robot_location[1], map_info.robot_direction)

    def __right(self):
        map_info.map_lock.acquire()
        print("Action: turn right")
        print("Action: turn right")
        map_info.robot_direction = DIRECTIONS[(DIRECTIONS.index(map_info.robot_direction)+1) % 4]
        self.put_robot(map_info.robot_location[0], map_info.robot_location[1], map_info.robot_direction)

    def action(self):
        while not self.event_queue.empty():
            try:
                command = self.event_queue.get()
                if   command == 'move':
                    self.__move()
                elif command == 'left':
                    self.__left()
                elif command == 'right':
                    self.__right()
                # elif command == 'back':
                #     self.__back()
                elif command == 'read':
                    self.__read()
                else:
                    print("Invalid command.")
                self.update_sensor()
                # map_info.descripted_map(printThis=True, form='b')
            except queue.Empty:
                pass
            time.sleep(0)


    def update_sensor(self):
        sens  = self.sensor.get_front_middle()
        if (sens[1] < 0) :
            sens[1] *= -1
            obs = False
        else:
            obs = True
        print(sens)
        if map_info.robot_direction == 'N':
            for dis in range(sens[1]):
                sens[0][0] -= 1
                map_info.map[sens[0][0]][sens[0][1]] = 1 if map_info.isFree(sens[0][0], sens[0][1]) else 2
                self.put_map(sens[0][0], sens[0][1])
        elif map_info.robot_direction == 'S':
            for dis in range(sens[1]):
                sens[0][0] += 1
                map_info.map[sens[0][0]][sens[0][1]] = 1 if map_info.isFree(sens[0][0], sens[0][1]) else 2
                self.put_map(sens[0][0], sens[0][1])
        elif map_info.robot_direction == 'W':
            for dis in range(sens[1]):
                sens[0][1] -= 1
                map_info.map[sens[0][0]][sens[0][1]] = 1 if map_info.isFree(sens[0][0], sens[0][1]) else 2
                self.put_map(sens[0][0], sens[0][1])
        elif map_info.robot_direction == 'E':
            for dis in range(sens[1]):
                sens[0][1] += 1
                map_info.map[sens[0][0]][sens[0][1]] = 1 if map_info.isFree(sens[0][0], sens[0][1]) else 2
                self.put_map(sens[0][0], sens[0][1])


x = Handler()
