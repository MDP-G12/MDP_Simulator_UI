import config
import time
from logger import *

import queue

# ----------------------------------------------------------------------
# class definition of algoAbstract.
# 
#   - explore()
#		robot starts doing exploration
# 
#   - findSP()
#		Finding Shortest Path, based on the known maps.
# 
#   - run()
#		robot starts running according shortest path algorithm
#
#   > handler   Handler class
#   > map       Map class
#   > stopFlag  Flag to tell robot to stop doing anything
# ----------------------------------------------------------------------
class algoAbstract:
    def __init__(self, handler=None):
        self.handler            = handler
        if handler != None:
            self.map            = handler.map
        self.stopFlag           = True
        self.lastCalibration    = 0

    # remember to update the time it start by calling self.startMove = time.clock()
    def explore(self):
        raise NotImplementedError

    def findSP(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def updateStopFlagStatus(self):
        # map coverage limit
        if (0 <= config.exploration_covLimit < 100) and self.map:
            if (self.map.countExplored()*100/(self.map.width*self.map.height)) >= config.exploration_covLimit:
                self.stop()
                return
        # time limit
        if (config.exploration_timeLimit > 0) and ((time.clock()-self.startMove) > config.exploration_timeLimit):
            self.stop()
            return


    # Uh? is it okay to put it here?
    def stop(self):
        self.stopFlag = True;
        verbose('Robot is asked to stop', tag='algo')



# ----------------------------------------------------------------------
# Dumb boy. This boy does nothing. I SWEAR!!
class algoDum(algoAbstract):
    def explore(self):
        pass
    def findSP(self):
        pass
    def run(self):
        pass
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# class definition of algoFactory.
# 
#   - explore()
#		robot starts doing exploration
# 
#   - findSP()
#		Finding Shortest Path, based on the known maps.
# 
#   - run()
#		robot starts running according shortest path algorithm
# ----------------------------------------------------------------------
class algoFactory:
    def __init__(self, handler, algoName="BF1"):
        if (algoName == "BF1"):
            self.algo = algoBF1(handler)
        elif (algoName == "dum"):
            self.algo = algoDum()
        elif (algoName == 'LHR'):
            self.algo = LeftHandRule(handler)
        elif (algoName == 'DFS'):
            self.algo = algoDFS(handler)
        elif (algoName == 'BFS'):
            self.algo = algoBFS(handler)
        else:
            raise NameError('algoName not found')

    # def explore(self):
    #     self.algo.explore()

    # def findSP(self):
    #     self.algo.findSP()

    # def run(self):
    #     self.algo.run()

    # def stop(self):
    #     self.algo.stop()


# ----------------------------------------------------------------------
# algoName = 'BF1'
# Implementation class of algoAbstract using algorithm Brute Force #1
# ----------------------------------------------------------------------
class algoBF1(algoAbstract):
    def __init__(self, handler):
        super().__init__(handler)

    def explore(self):
        # robot_location  = self.map.get_robot_location()
        self.periodic_check()

    def periodic_check(self):
        self.handler.move()
        self.handler.simulator.master.after(config.simulator_mapfrequency, self.periodic_check)

    def findSP(self):
        pass

    def run(self):
        pass
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# algoName = 'LHR'
# Left Hand Rule Exploration Algorithm:
#     Walking by the wall; Wall is on the left side; Turn right on corner 
# ----------------------------------------------------------------------
class LeftHandRule(algoAbstract):
    def __init__(self, handler):
        super().__init__(handler)
        self.left_flag = True

    def explore(self):
        self.stopFlag = False
        self.periodic_check()

    def periodic_check(self):
        if self.check_left() and self.left_flag:
            self.handler.left()
            print(" [Info] Stop turning left.")
            self.left_flag = False
        elif self.check_front():
            self.handler.move()
            self.left_flag = True
        else:
            self.handler.right()
            self.left_flag = True
        if not self.stopFlag:
            self.handler.simulator.master.after(config.simulator_mapfrequency, self.periodic_check)

    def findSP(self):
        pass

    def run(self):
        pass

    def check_left(self):
        self.handler.left()
        ret = self.check_front()
        self.handler.right()
        return ret

        # robot_location = self.handler.map.get_robot_location()
        # print(robot_location)
        # left_direction = self.handler.map.get_robot_direction_left()
        # map_explored = self.map.get_map()
        # if left_direction == 'N':
        #     if robot_location[0] < 2:
        #         return False
        #     if map_explored[robot_location[0]-2][robot_location[1]] == 1 and map_explored[robot_location[0]-2][robot_location[1]-1] == 1 and map_explored[robot_location[0]-2][robot_location[1]+1] == 1:
        #         return True
        #     else:
        #         return False
        # elif left_direction == 'S':
        #     if robot_location[0] > 12:
        #         return False
        #     if map_explored[robot_location[0]+2][robot_location[1]] == 1 and map_explored[robot_location[0]+2][robot_location[1]-1] == 1 and map_explored[robot_location[0]+2][robot_location[1]+1] == 1:
        #         return True
        #     else:
        #         return False
        # elif left_direction == 'E':
        #     if robot_location[1] > 17:
        #         return False
        #     if map_explored[robot_location[0]][robot_location[1]+2] == 1 and map_explored[robot_location[0]+1][robot_location[1]+2] == 1 and map_explored[robot_location[0]-1][robot_location[1]+2] == 1:
        #         return True
        #     else:
        #         return False
        # elif left_direction == 'W':
        #     if robot_location[1] < 2:
        #         return False
        #     if map_explored[robot_location[0]][robot_location[1]-2] == 1 and map_explored[robot_location[0]+1][robot_location[1]-2] == 1 and map_explored[robot_location[0]-1][robot_location[1]-2] == 1:
        #         return True
        #     else:
        #         return False
        #
        # else:
        #     print("[Error] Invalid direction.")

    def check_front(self):
        sensor_data = self.handler.robot.receive()
        print('Sensor data: ', sensor_data)
        if (sensor_data[0] > 1 or sensor_data[0] < 0) and (sensor_data[1] > 1 or sensor_data[1] < 0) and (sensor_data[2] > 1 or sensor_data[2] < 0):
            return True
        else:
            return False
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# algoName = 'DFS'
# Depth First Search exploration algorithm.
#   - DFS + heuristic (incomplete exploration due to heuristic)
#   - BFS for the rest of the unexplored boxes
#   - Go to finish area then go back to start area 
# Assumption made on this algorithm:
#   - turning left, turning right, and move forward are considered 1 move
# Shortest Path using BFS
# ----------------------------------------------------------------------
class algoDFS(algoAbstract):
    def __init__(self, handler):
        super().__init__(handler)
        self.gotoList       = None
        self.goalVisited    = False

    # ------------------------------------------------------------------
    # map related own function
    # ------------------------------------------------------------------
    DIRECTIONS  = ('N', 'E', 'S', 'W')
    locDisp     = ((-1, 0),  ( 0, 1),  ( 1, 0),  ( 0,-1))

    Displacement= ( ((-2,-1), (-2, 0), (-2, 1)),   # North
                    ((-1, 2), ( 0, 2), ( 1, 2)),   # East
                    (( 2, 1), ( 2, 0), ( 2,-1)),   # South
                    (( 1,-2), ( 0,-2), (-1,-2))    # West
                )

    goalLocation= [13,18]

    # return True if the 3x1 boxes adjacent to robot are free given robot location (y,x)
    # idx in parameter is an integer value equivalent to DIRECTIONS.index(direction)
    #
    def _areFree(self, y, x, idx):
        # Matrix computation to get the boxes given the direction
        verbose('_areFree', (y, x, idx), tag='Algo DFS', lv='deepdebug')
        for i in self.Displacement[idx]:
            if not self.map.isFree(i[0]+y, i[1]+x, config.algoMapKnown):
                return False
        return True

    # pasted and adjusted from Handler.__do_read()
    # return True if there is unexplored box on sight; False otherwise
    def _anyNewBlock( self, locY, locX, drc, goalVisitedFlag = False ):
        
        # as grading criteria, must visit goal on exploration
        if goalVisitedFlag and ([locY, locX] == self.goalLocation) and not self.goalVisited:
            return True

        robot_direction = self.DIRECTIONS[drc]
        robot_location  = [locY, locX]
        sensor_data     = [ config.sensor_range['front_middle'],
                            config.sensor_range['front_left'],
                            config.sensor_range['front_right'],
                            config.sensor_range['left'],
                            config.sensor_range['right'] ]

        dis_y = [-1, 0, 1, 0]
        dis_x = [ 0, 1, 0,-1]
        direction_ref   = ['N', 'E', 'S', 'W']
        sensor_loc      = [[-1, 0], [ 0, 1], [ 1, 0], [ 0,-1]]  # displacement of sensor relative to robot location
        sensor_locd     = [[-1,-1], [-1, 1], [ 1, 1], [ 1,-1]]  # displacement of diagonal sensor relative to robot location
        idx_disp        = [0, -4, -1, 3, 1]                     # index displacement
        idx_dire        = [0,  0,  0, 3, 1]                     # direction displacement index
        sensor_nbr      = config.sensor_nbr

        # print('_anyNewBlock', locY, locX, drc, sep='; ')

        # front sensor
        idx = drc
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
            
            # see the criteria on robot_simulator.py
            dis = sensor_data[i]
            curDrc = (idx+idx_dire[i]) % 4

            yy = dis_y[ curDrc ]
            xx = dis_x[ curDrc ]

            # print('_anyNewBlock', yy, xx, curDrc sep='; ')
            for i in range(dis):
                loc[0] += yy
                loc[1] += xx
                # if this is an unexplored block
                if   not self.map.isExplored(loc[0], loc[1]):
                    return True
                # if free block then we continue searching
                elif self.map.isFree(loc[0], loc[1]):
                    continue
                # if explored and not free then we proceed to next sensor
                else:
                    break

        return False

    # ------------------------------------------------------------------
    

    # ------------------------------------------------------------------
    # Robot related own function
    # ------------------------------------------------------------------
    # Execute list of actions inside self.act
    # Calling back caller on finish if simulator exist
    def actExec(self, caller=None, *args):
        roboLoc = None
        if self.map:
            roboLoc = self.map.get_robot_location()
        if caller:
            verbose('actExec', roboLoc, caller.__name__, tag='Algo DFS', lv='deepdebug', pre='  ')
        else:
            verbose('actExec', roboLoc, tag='Algo DFS', lv='deepdebug', pre='  ')

        # if currently at Goal points then set the flag
        if self.map and (self.map.get_robot_location() == self.goalLocation):
            self.goalVisited = True

        # update the stopFlag status
        self.updateStopFlagStatus()

        # if simulator exists
        if self.handler.simulator:
            # Unfinished condition
            if not self.stopFlag and self.act:
                # Move
                self.handler.command( self.act.pop() )
                # if calibratable then do calibration
                calib = self.__calibrateable()
                if calib[0]:
                    self.lastCalibration = 0
                    self.handler.calibrate(calib[1])
                else:
                    self.lastCalibration += 1
                self.handler.simulator.master.after(config.simulator_mapfrequency, self.actExec, caller, *args)
                return

            # Finished
            self.handler.simulator.master.after(0, caller, *args)

        # if simulator doesn't exist
        else:
            while not self.stopFlag and self.act:
                self.handler.command( self.act.pop() )
                calib = self.__calibrateable()
                if calib[0]:
                    self.lastCalibration = 0
                    self.handler.calibrate(calib[1])
                else:
                    self.lastCalibration += 1

    def __calibrateable(self, y=None, x=None, roboDir=None):
        if (y==None) or (x==None) or (roboDir==None):
            [y,x] = self.map.get_robot_location()
            roboDir = self.map.get_robot_direction()
        idx     = self.DIRECTIONS.index( roboDir )
        
        # Orientation Calibration
        i   = self.Displacement[idx][0]
        j   = self.Displacement[idx][2]
        mv  = self.locDisp[idx]
        ret = []
        if ((self.map.isObstacle(i[0]+y, i[1]+x, config.algoMapKnown) and
             self.map.isObstacle(j[0]+y, j[1]+x, config.algoMapKnown)) or
            (self.map.isObstacle(i[0]+mv[0]+y, i[1]+mv[1]+x, config.algoMapKnown) and
             self.map.isObstacle(j[0]+mv[0]+y, j[1]+mv[1]+x, config.algoMapKnown))):
            ret.append(True)
        else:
            ret.append(False)

        # Distance Calibration
        i = self.Displacement[idx][1]
        ret.append(self.map.isObstacle(i[0]+y, i[1]+x, config.algoMapKnown))

        # verbose("__calibrateable", ret, y, x, idx, i, j,
        #         self.map.isObstacle(i[0]+y, i[1]+x, config.algoMapKnown), self.map.isObstacle(j[0]+y, j[1]+x, config.algoMapKnown),
        #         tag='algoDFS', lv='debug')

        return ret

    # ------------------------------------------------------------------



    # ------------------------------------------------------------------
    # Traversal related own function
    # ------------------------------------------------------------------
    # return A STACK (list, last element as top) of command,
    #     the shortest known path to coordinate (y,x) using BFS algorithm
    # 
    def _gotoYX(self, y, x, faceto=None, loc=None, drcO=None):
        map = self.map
        if not loc:
            loc = map.get_robot_location()                                          # original location
        if not drcO:
            drcO= self.DIRECTIONS.index(map.get_robot_direction())                  # original direction
        else:
            drcO= self.DIRECTIONS.index(drcO)
        drc = drcO
        step= 0
        ret = None

        # flag and step; -1 unvisited; -2 source; otherwise index of DIRECTIONS
        mvt = [[[-1]*4 for i in range(map.width)] for j in range(map.height)]


        verbose('_gotoYX ({},{}) starts..'.format(y, x), tag='Algo DFS', lv='debug')
        # --------------------
        # the BFS
        q = queue.Queue()
        q.put((loc[0],loc[1],drc,-2))                       # push source node into queue
        while (not q.empty()) and (ret == None):
            sz = q.qsize()
            # verbose('_gotoYX ({},{}): step {}; size {};'.format(y, x, step, sz), tag='Algo DFS', lv='debug')
            while sz > 0:
                sz  = sz-1
                fr  = q.get()
                [locY, locX, drc] = fr[:3]

                # skip if visited before
                if mvt[locY][locX][drc] != -1:
                    continue
                mvt[locY][locX][drc] = fr[3]

                verbose('> Pop queue item and execute (fr, y, x, d, faceto) ', (fr, locY, locX, drc, faceto), tag=None, lv='deepdebug', pre='\t')
                # print('>>>', locY, locX, drc, ':', mvt[locY][locX], mvt[1][2], sep=' ')

                # Terminate condition
                if ((locY == y) and (locX == x) and 
                    ( (faceto == None) or (faceto == drc) or (faceto == self.DIRECTIONS[drc]) )):
                    ret = drc
                    break

                # move forward
                nextY   = locY + self.locDisp[drc][0]
                nextX   = locX + self.locDisp[drc][1]
                # print('>>>', nextY, nextX, drc, ':', mvt[nextY][nextX][drc], sep=' ')
                if (mvt[nextY][nextX][drc]==-1) and (self._areFree( locY, locX, drc )):
                    q.put( ( nextY, nextX, drc, drc ) )

                # turn right
                nextDrc = (drc+1) % 4
                if (mvt[locY][locX][nextDrc] == -1):
                    q.put(( locY, locX, nextDrc, drc ))

                # turn left
                nextDrc = (drc+3) % 4
                if (mvt[locY][locX][nextDrc] == -1):
                    q.put(( locY, locX, nextDrc, drc ))

            # counting steps; currently it is unused
            step = step + 1


        verbose('_gotoYX ({},{}) trace back.'.format(y, x), tag='Algo DFS', lv='debug')
        # --------------------
        # Trace back the steps
        if (ret != None):
            locY= y
            locX= x
            drc = ret
            ret = []
            while (locY != loc[0]) or (locX != loc[1]) or (drc != drcO):
                tmp = mvt[locY][locX][drc]
                if   (tmp == drc):
                    ret.append('M')
                    locY = locY - self.locDisp[drc][0]
                    locX = locX - self.locDisp[drc][1]
                elif ((tmp+1)%4 == drc):
                    ret.append('R')
                    drc = tmp
                elif ((tmp+3)%4 == drc):
                    ret.append('L')
                    drc = tmp
                else:
                    verbose('ERROR: _gotoYX trace back failed.', tag='Algo DFS', pre='  ')
                    return None


        # --------------------
        # ret.reverse()     # see return format on the top of this function
        return ret

    # DFS Exploration algorithm with heuristic
    # Followed by BFS Search of unknown area
    def _do_DFS(self, s, visited):
        # verbose('_do_DFS', s, tag='Algo DFS', lv='debug')
        if self.stopFlag:
            return

        while not self.stopFlag and s:
            top = s.pop()
            verbose('_do_DFS', top, tag='Algo DFS', lv='debug')
            [locY, locX, drc, cmd] = top[:4]

            # if visited before
            if visited[locY][locX][drc]:
                continue

            # heuristic part
            # is it important to go to this stage? if by going this state doesn't explore new block just skip
            if (cmd) and (not self._anyNewBlock( locY, locX, drc )):
                visited[locY][locX][drc] = 1
                continue

            # compare with current state
            # if not equal then robot goto current state first
            if (([locY, locX] != self.map.get_robot_location()) or
                (self.DIRECTIONS[drc] != self.map.get_robot_direction())):
                # verbose('WOW: ', top, locY, locX, drc, cmd, tag='Algo DFS')
                self.act = self._gotoYX( locY, locX, drc )
                self.actExec( self._do_DFS, s, visited )
                if self.handler.simulator:
                    s.append(( locY, locX, drc, None ))
                    return

            # set flag
            visited[locY][locX][drc] = 1

            # right
            nextDrc = (drc+1) % 4
            if not visited[locY][locX][nextDrc]:
                s.append(( locY, locX, nextDrc, 'R' ))

            # left
            nextDrc = (drc+3) % 4
            if not visited[locY][locX][nextDrc]:
                s.append(( locY, locX, nextDrc, 'L' ))

            # forward
            nextY = locY + self.locDisp[drc][0]
            nextX = locX + self.locDisp[drc][1]
            if (not visited[nextY][nextX][drc]) and (self._areFree( locY, locX, drc )):
                s.append(( nextY, nextX, drc, 'F' ))


        if self.handler.simulator:
            self.act = self._do_findUnexplored()
            if self.act:
                self.actExec( self._do_DFS, s, visited )
                return
        else:
            self.act = self._do_findUnexplored()
            while not self.stopFlag and self.act:
                self.actExec( self._do_DFS, s, visited )
                self.act = self._do_findUnexplored()

        # Grading purpose part (go inside finish then inside start)
        self.act = self.__exploreGrading()
        self.actExec(None)

    # the exhaustive BFS search for unexplored block
    def _do_findUnexplored(self):
        map = self.map
        loc = map.get_robot_location()                                          # original location
        drcO= self.DIRECTIONS.index(map.get_robot_direction())                  # original direction
        drc = drcO
        step= 0
        ret = None

        # flag and step; -1 unvisited; -2 source; otherwise index of DIRECTIONS
        mvt = [[[-1]*4 for i in range(map.width)] for j in range(map.height)]

        # --------------------
        # the BFS
        q = queue.Queue()
        q.put((loc[0],loc[1],drc,-2))                       # push source node into queue
        while (not q.empty()) and (ret == None):
            sz = q.qsize()
            # verbose('_gotoYX ({},{}): step {}; size {};'.format(y, x, step, sz), tag='Algo DFS', lv='debug')
            while sz > 0:
                sz  = sz-1
                fr  = q.get()
                [locY, locX, drc] = fr[:3]

                # skip if visited before
                if mvt[locY][locX][drc] != -1:
                    continue
                mvt[locY][locX][drc] = fr[3]

                # verbose('> Pop queue item and execute (fr, y, x, d, faceto) ', fr, locY, locX, drc, faceto, tag=None, lv='deepdebug', pre='\t')
                # print('>>>', locY, locX, drc, ':', mvt[locY][locX], mvt[1][2], sep=' ')

                # Terminate condition
                if self._anyNewBlock( locY, locX, drc, True ):
                    ret = drc
                    break

                # move forward
                nextY   = locY + self.locDisp[drc][0]
                nextX   = locX + self.locDisp[drc][1]
                if (mvt[nextY][nextX][drc]==-1) and (self._areFree( locY, locX, drc )):
                    q.put( ( nextY, nextX, drc, drc ) )

                # turn right
                nextDrc = (drc+1) % 4
                if (mvt[locY][locX][nextDrc] == -1):
                    q.put(( locY, locX, nextDrc, drc ))

                # turn left
                nextDrc = (drc+3) % 4
                if (mvt[locY][locX][nextDrc] == -1):
                    q.put(( locY, locX, nextDrc, drc ))

            # counting steps; currently it is unused
            step = step + 1

        # --------------------
        # Trace back the steps
        if (ret != None):
            ret = []
            while (locY != loc[0]) or (locX != loc[1]) or (drc != drcO):
                tmp = mvt[locY][locX][drc]
                if   (tmp == drc):
                    ret.append('M')
                    locY = locY - self.locDisp[drc][0]
                    locX = locX - self.locDisp[drc][1]
                elif ((tmp+1)%4 == drc):
                    ret.append('R')
                    drc = tmp
                elif ((tmp+3)%4 == drc):
                    ret.append('L')
                    drc = tmp
                else:
                    verbose('ERROR: _gotoYX trace back failed.', tag='Algo DFS', pre='  ')
                    return None

        return ret


    # BFS based on _do_findUnexplored to find nearest calibratable position within limit
    def _do_findCalibration(self):
        map = self.map
        loc = map.get_robot_location()                                          # original location
        drcO= self.DIRECTIONS.index(map.get_robot_direction())                  # original direction
        drc = drcO
        step= 0
        ret = None

        # flag and step; -1 unvisited; -2 source; otherwise index of DIRECTIONS
        mvt = [[[-1]*4 for i in range(map.width)] for j in range(map.height)]

        # --------------------
        # the BFS
        q = queue.Queue()
        q.put((loc[0],loc[1],drc,-2))                       # push source node into queue
        while (step <= config.maxCalibrationMove) and (not q.empty()) and (ret == None):
            sz = q.qsize()
            # verbose('_gotoYX ({},{}): step {}; size {};'.format(y, x, step, sz), tag='Algo DFS', lv='debug')
            while sz > 0:
                sz  = sz-1
                fr  = q.get()
                [locY, locX, drc] = fr[:3]

                # skip if visited before
                if mvt[locY][locX][drc] != -1:
                    continue
                mvt[locY][locX][drc] = fr[3]

                # Terminate condition
                calib = self.__calibrateable( locY, locX, self.DIRECTIONS[drc] )
                if calib[0]:
                    ret = drc
                    break

                # move forward
                nextY   = locY + self.locDisp[drc][0]
                nextX   = locX + self.locDisp[drc][1]
                if (mvt[nextY][nextX][drc]==-1) and (self._areFree( locY, locX, drc )):
                    q.put( ( nextY, nextX, drc, drc ) )

                # turn right
                nextDrc = (drc+1) % 4
                if (mvt[locY][locX][nextDrc] == -1):
                    q.put(( locY, locX, nextDrc, drc ))

                # turn left
                nextDrc = (drc+3) % 4
                if (mvt[locY][locX][nextDrc] == -1):
                    q.put(( locY, locX, nextDrc, drc ))

            # counting steps;
            step = step + 1

        # --------------------
        # Trace back the steps
        if (ret != None):
            # ret = ['C']
            ret = []
            while (locY != loc[0]) or (locX != loc[1]) or (drc != drcO):
                tmp = mvt[locY][locX][drc]
                if   (tmp == drc):
                    ret.append('M')
                    locY = locY - self.locDisp[drc][0]
                    locX = locX - self.locDisp[drc][1]
                elif ((tmp+1)%4 == drc):
                    ret.append('R')
                    drc = tmp
                elif ((tmp+3)%4 == drc):
                    ret.append('L')
                    drc = tmp
                else:
                    verbose('ERROR: _gotoYX trace back failed.', tag='Algo DFS', pre='  ')
                    return None

        print(ret)

        return ret

    # ------------------------------------------------------------------


    def explore(self):
        verbose('exploring...', tag='Algo DFS')

        map             = self.map
        [robY, robX]    = map.get_robot_location()
        robD            = self.DIRECTIONS.index(map.get_robot_direction())
        visited         = [[[0]*4 for i in range(map.width)] for j in range(map.height)]
        s               = [(robY, robX, robD, None)]
        self.stopFlag   = False
        self.startMove  = time.clock()
        self._do_DFS(s, visited)


    def __exploreGrading(self):
        verbose('Entering Explore Grading..', tag='algoDFS', lv='debug')
        ret = self._gotoYX(1,1, loc=(13,18), drcO='S')
        if ret:
            ret = ret + self._gotoYX(13,18,'S')
        return ret

    def findSP(self):
        verbose('Entering find Shortest Path..', tag='algoDFS', lv='debug')
        return self._gotoYX(13,18, loc=(1,1), drcO='E') + self._gotoYX(1,1,'E')

    def run(self):
        self.act = self.findSP()
        self.stopFlag = False
        if self.handler.simulator:
            self.actExec(None)
        else:
            while self.act:
                self.handler.command( self.act.pop() )

# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
# algoName = 'BFS'
# Breadth First Search algorithm.
# Exploration:
#   - Find minimum step to get the sensor read unexplored block then
#     then command the robot to go and read. (Using BFS)
#   - [Move], [turn right], [turn left] are considered as 1 step
#   - Once done go to finish area then go back to start area
# Shortest Path:
#   - BFS lo
# ----------------------------------------------------------------------
class algoBFS(algoDFS):
    def __init__(self, handler):
        super().__init__(handler)

    def explore(self):
        verbose('exploring...', tag='Algo-BFS')
        self.stopFlag   = False
        self.startMove  = time.clock()
        self._do_BFS()

    def _do_BFS(self):
        if self.stopFlag:
            return

        if self.handler.simulator:
            # if too long never calibrate
            if (self.lastCalibration > config.noCalibrationLimit):
                print('lastCalibration:', self.lastCalibration);
                self.act = self._do_findCalibration()
                # if got place to calibrate within limit then go. Otherwise continue the algo
                if self.act:
                    self.actExec( self._do_BFS )
                    return

            self.act = self._do_findUnexplored()
            if self.act:
                self.actExec( self._do_BFS )
                return
        else:
            self.act = self._do_findUnexplored()
            while not self.stopFlag and self.act:
                self.actExec( self._do_BFS )
                self.act = self._do_findUnexplored()

        # Grading purpose part (go inside finish then inside start)
        verbose('_do_BFS finished', tag='algoBFS', lv='debug')
        self.act = self.__exploreGrading()
        self.actExec(None)

    def __exploreGrading(self):
        verbose('Entering Explore Grading..', tag='algoDFS', lv='debug')
        if (self.goalVisited):
            return self._gotoYX(1,1)
        else:
            ret = self._gotoYX(1,1, loc=(13,18), drcO='S')
            if ret:
                ret = ret + self._gotoYX(13,18,'S')
            return ret
