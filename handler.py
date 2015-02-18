from logger import *
# import simulator
import config
import algo
import map
import robot_simulator
import robot_connector

class Handler:
    def __init__(self, simulator=None):
        self.simulator  = simulator
        self.map        = map.Map()
        self.algo       = algo.algoFactory(self, algoName=config.algoName).algo
        # if robot is simulated
        if config.robot_simulation:
            self.robot = robot_simulator.RobotSimulator(self)
            self.__do_read()
        else:
            self.robot = robot_connector.Connector()

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
        self.__do_read()
        self.__update_map()

    # Change direction backwards, move 1 block, revert directions
    def back(self):
        verbose("Action: move backward", tag='Handler')
        cur_dir = self.map.get_robot_direction()
        self.map.set_robot_direction( self.map.get_robot_direction_back() )
        self.__do_move(forward=False)
        self.map.set_robot_direction( cur_dir )
        self.__do_read()
        self.__update_map()

    def left(self):
        # ===== Threading =====
        # map_info.map_lock.acquire()
        # verbose("Locked by "+threading.current_thread(),
        #     tag='Map Lock', lv='debug')
        # ===== ========= =====
        verbose("Action: turn left", tag='Handler')
        self.map.set_robot_direction( self.map.get_robot_direction_left() )
        # Send command to robot
        self.robot.send('L')
        self.__do_read()
        self.__update_map()
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
        # Send command to robot
        self.robot.send('R')
        self.__do_read()
        self.simulator.update_map()
        # ===== Threading =====
        # map_info.map_lock.release()
        # print("[Map Lock] Released by ", threading.current_thread())
        # ===== ========= =====

    def explore(self):
        self.algo.explore()

    def stop(self):
        self.algo.stop()
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    #   Real Actions
    # ----------------------------------------------------------------------
    # Updating simulator map if exist
    # Sending signal to robot, get the sensors data and process it to map;
    # ----------------------------------------------------------------------
    def __update_map(self):
        if self.simulator != None:
            self.simulator.update_map()
        if (verbose("Current Map:", tag='Handler', lv='debug', pre='  ')):
            for y in range(self.map.height):
                print('\t', curmap[y])

    def __do_move(self, forward=True):
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
            # Send command to robot
            if forward:
                self.robot.send('F')
            else:
                self.robot.send('B')
        else:
            verbose("WARNING: Not moving due to obstacle or out of bound",
                tag='Handler', pre='    ', lv='debug')

        # map_info.map_lock.release()
        # print("[Map Lock] Released by ", threading.current_thread())

    def __do_read(self):
        sensor_data = None
        while not sensor_data:
            sensor_data = self.robot.receive()
        robot_direction = self.map.get_robot_direction()
        robot_location  = self.map.get_robot_location()

        verbose('__do_read from sensor', sensor_data, tag='Handler', lv='debug')

        dis_y = [-1, 0, 1, 0]
        dis_x = [ 0, 1, 0,-1]
        direction_ref   = ['N', 'E', 'S', 'W']
        sensor_loc      = [[-1, 0], [ 0, 1], [ 1, 0], [ 0,-1]]  # displacement of sensor relative to robot location
        sensor_locd     = [[-1,-1], [-1, 1], [ 1, 1], [ 1,-1]]  # displacement of diagonal sensor relative to robot location
        idx_disp        = [0, -4, -1, 3, 1]                     # index displacement
        idx_dire        = [0,  0,  0, 3, 1]                     # direction displacement index
        sensor_nbr      = 5

        # front sensor
        idx = map.Map.DIRECTIONS.index(robot_direction)
        for i in range(sensor_nbr):
            if idx_disp[i] < 0:
                # diagonal sensor. front_right, front_left. using sensor_locd
                sid =  (idx - idx_disp[i]) % 4
                loc =  [robot_location[0] + sensor_locd[sid][0],
                        robot_location[1] + sensor_locd[sid][1]]
            else:
                # axis sensor. front, left, right. using sensor_loc
                sid =  (idx + idx_disp[i]) % 4
                loc =  [robot_location[0] + sensor_loc[sid][0],
                        robot_location[1] + sensor_loc[sid][1]]
            verbose('sensor location', loc, tag='Handler', pre='  ', lv='debug')
            
            # sensor return value
            # see the criteria on robot_simulator.py
            dis = sensor_data[i]
            if dis < 0:
                dis *= -1
                obs = False
            else:
                obs = True
            # set the free boxes
            yy = dis_y[ (idx+idx_dire[i]) % 4 ]
            xx = dis_x[ (idx+idx_dire[i]) % 4 ]
            for i in range(dis):
                loc[0] += yy
                loc[1] += xx
                self.map.set_map(loc[0], loc[1], 'free')
            # set if obstacle
            if (obs):
                self.map.set_map(loc[0], loc[1], 'obstacle')


    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    #   Additional functions
    # ----------------------------------------------------------------------
    def showCurMap(self):
        curmap = self.map.get_map()
        for y in range(self.map.height):
            print('\t', curmap[y])
    # ----------------------------------------------------------------------
    

x = Handler()

# x.showCurMap()