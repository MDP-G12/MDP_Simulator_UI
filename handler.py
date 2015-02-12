from logger import *
# import simulator
import config
import algo
import map

class Handler:
    def __init__(self, simulator):
        self.simulator  = simulator
        self.map        = map.Map()
        self.algo       = algo.algoDum()
        # self.createSimulator()

    # def createSimulator(self):
    #     self.simulator = simulator.SimulatorUI(self)
    #     # map_simulator = Simulator(root)
    #     # map_simulator.algoObject.explore()
    #     self.simulator.master.mainloop()


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
        verbose("Action: move forward", tag='Handler')
        self.__do_move()

    def back(self):
        verbose("Action: move backward", tag='Handler')
        cur_dir = self.map.get_robot_direction()
        self.map.set_robot_direction( self.map.get_robot_direction_back() )
        self.__do_move()
        self.map.set_robot_direction( cur_dir )

    def left(self):
        # ===== Threading =====
        # map_info.map_lock.acquire()
        # verbose("Locked by "+threading.current_thread(),
        #     tag='Map Lock', lv='debug')
        # ===== ========= =====
        verbose("Action: turn left", tag='Handler')
        self.map.set_robot_direction( self.map.get_robot_direction_left() )
        # ===== Threading =====
        # map_info.map_lock.release()
        # print("[Map Lock] Released by ", threading.current_thread())
        # ===== ========= =====

    def right(self):
        # ===== Threading =====
        # map_info.map_lock.acquire()
        # verbose("Locked by "+threading.current_thread(),
        #     tag='Map Lock', lv='debug')
        # ===== ========= =====
        verbose("Action: turn right", tag='Handler')
        self.map.set_robot_direction( self.map.get_robot_direction_right() )
        # ===== Threading =====
        # map_info.map_lock.release()
        # print("[Map Lock] Released by ", threading.current_thread())
        # ===== ========= =====
    # ----------------------------------------------------------------------

    # def __move(self):
    #     verbose("Action: move forward", tag='Handler')
    #     self.__do_move()

    # def __back(self):
    #     verbose("Action: move backward", tag='Handler')
    #     cur_dir = self.map.get_robot_direction()
    #     self.map.set_robot_direction( self.map.get_robot_direction_back() )
    #     self.__do_move()
    #     self.map.set_robot_direction( cur_dir )


    def __do_move(self):
        # Threading
        # map_info.map_lock.acquire()
        # verbose("Locked by "+threading.current_thread(),
        #     tag='Map Lock', lv='debug')
        
        # Getting the next position
        robot_location  = self.map.get_robot_location()
        robot_direction = self.map.get_robot_direction()
        if   robot_direction == 'N':
                robot_next = [robot_location[0]-1, robot_location[1]]
        elif robot_direction == 'S':
                robot_next = [robot_location[0]+1, robot_location[1]]
        elif robot_direction == 'W':
                robot_next = [robot_location[0], robot_location[1]-1]
        elif robot_direction == 'E':
                robot_next = [robot_location[0], robot_location[1]+1]
        else:
            verbose("ERROR: Direction undefined! __do_move",
                tag='Handler', pre='   >> ', lv='quiet')

        # Validating the next position
        if self.map.valid_pos(robot_next[0], robot_next[1]):
            # Updating robot position value
            self.map.set_robot_location( robot_next )
        else:
            verbose("WARNING: Not moving due to obstacle or out of bound",
                tag='Handler', pre='    ', lv='debug')

        # map_info.map_lock.release()
        # print("[Map Lock] Released by ", threading.current_thread())





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


# x = Handler()
