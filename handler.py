from logger import *
# import simulator
import config
import algo
import map
import robot_simulator
import robot_connector
import time

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
            time.sleep(0.1)
            self.robot.send('I')
            self.__do_read()
            self.robot.androListen( simulator, self.algo.explore, self.algo.run )
        time.clock()

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
        tmp = self.__do_move()
        if tmp:
            self.__do_read()
        self.__update_map()

    # Change direction backwards, move 1 block, revert directions
    def back(self):
        verbose("Action: move backward", tag='Handler')
        cur_dir = self.map.get_robot_direction()
        self.map.set_robot_direction( self.map.get_robot_direction_back() )
        tmp = self.__do_move(forward=False)
        self.map.set_robot_direction( cur_dir )
        if tmp:
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

    def calibrate(self, distCalibrate=False):
        verbose("Action: calibrate", tag='Handler')
        self.robot.send('C')
        tmp = self.robot.receive(convert=False)
        while '[Cmd] C' not in tmp:
            tmp = self.robot.receive(convert=False)
        time.sleep(config.CWait)
        if (distCalibrate):
            self.calibDist()

    def calibDist(self):
        verbose("Action: Calibrate Distance", tag='Handler')
        self.robot.send('E')
        tmp = self.robot.receive(convert=False)
        while '[Cmd] E' not in tmp:
            tmp = self.robot.receive(convert=False)
        time.sleep(config.EWait)

    def command(self, cmd):
        if   cmd == 'M':
            self.move()
        elif cmd == 'L':
            self.left()
        elif cmd == 'R':
            self.right()
        elif cmd == 'C':
            self.calibrate()
        elif cmd == 'E':
            self.calibDist()
        else:
            verbose("Command: unknown command", cmd, tag='Handler')

    def explore(self):
        self.algo.explore()

    def stop(self):
        self.algo.stop()
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    #   Real Actions
    # ----------------------------------------------------------------------
    # Sending signal to robot, get the sensors data and process it to map;
    # ----------------------------------------------------------------------

    # Updating simulator map if exist
    def __update_map(self):
        if self.simulator:
            self.simulator.update_map()
        if (verbose("Current Map:", tag='Handler', lv='deepdebug', pre='  ')):
            curmap = self.map.get_map()
            for y in range(self.map.height):
                print('\t', curmap[y])

    # sending signal to robot and set the new location to map class
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
            return True
        else:
            verbose("WARNING: Not moving due to obstacle or out of bound",
                tag='Handler', pre='    ', lv='debug')
            return False

        # map_info.map_lock.release()
        # print("[Map Lock] Released by ", threading.current_thread())

    # getting data from sensor then set the value to map class
    # please read robot_simulator.py :: receive() for the order of return value from sensors
    def __do_read(self):
        sensor_data = None
        while not sensor_data:
            sensor_data = self.robot.receive()
            verbose('__do_read', sensor_data, tag='Handler', lv='debug', pre='  ')
        robot_direction = self.map.get_robot_direction()
        robot_location  = self.map.get_robot_location()

        verbose('__do_read from sensor', robot_location+[robot_direction], sensor_data, tag='Handler', lv='debug')

        # return
        # print(sensor_data)

        dis_y = [-1, 0, 1, 0]
        dis_x = [ 0, 1, 0,-1]
        direction_ref   = ['N', 'E', 'S', 'W']
        sensor_loc      = [[-1, 0], [ 0, 1], [ 1, 0], [ 0,-1]]  # displacement of sensor relative to robot location
        sensor_locd     = [[-1,-1], [-1, 1], [ 1, 1], [ 1,-1]]  # displacement of diagonal sensor relative to robot location
        idx_disp        = [0, -4, -1, 3, 1]                     # index displacement
        idx_dire        = [0,  0,  0, 3, 1]                     # direction displacement index
        sensor_nbr      = 5

        # sensor
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
            verbose('sensor location', loc, tag='Handler', pre='  ', lv='deepdebug')
            
            # sensor return value
            # see the criteria on robot_simulator.py
            dis = sensor_data[i]
            if dis < 1:
                dis *= -1
                obs  = False
            else:
                obs  = True
            
            # set the free boxes
            yy = dis_y[ (idx+idx_dire[i]) % 4 ]
            xx = dis_x[ (idx+idx_dire[i]) % 4 ]
            while dis > 1:
                loc[0]  += yy
                loc[1]  += xx
                dis     -= 1
                self.map.set_map(loc[0], loc[1], 'free')

            # set last block if obstacle
            if (dis == 1):  # special case for 0, since dis will be 0
                loc[0]  += yy
                loc[1]  += xx
                dis     -= 1
                if obs:
                    self.map.set_map(loc[0], loc[1], 'obstacle')
                else:
                    self.map.set_map(loc[0], loc[1], 'free')

        # update map data in RPi
        p1, p2 = self.map.descripted_map()
        p3  = p1 + p2
        msg = b''.join([ str.encode('Map'), bytes([int(p3[x*2:x*2+2],16) for x in range(len(p3)>>1)]),
                        bytes(robot_location), str.encode(robot_direction) ])
        self.robot.send( msg, isByte=True )
        txt = None
        while not txt or '[Cmd] Map' not in txt:
            txt = self.robot.receive(convert=False)


    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    #   Additional functions
    # ----------------------------------------------------------------------
    def showCurMap(self):
        curmap = self.map.get_map()
        for y in range(self.map.height):
            print('\t', curmap[y])
    # ----------------------------------------------------------------------
    

# x = Handler()

# x.showCurMap()
