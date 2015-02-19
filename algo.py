import config
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
        self.handler    = handler
        if handler != None:
            self.map    = handler.map
        self.stopFlag   = True

    def explore(self):
        raise NotImplementedError

    def findSP(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

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

    def explore(self):
        self.stopFlag = False
        self.periodic_check()

    def periodic_check(self):
        if self.check_left():
            self.handler.left()
        elif self.check_front():
            self.handler.move()
        else:
            self.handler.right()
        if not self.stopFlag:
            self.handler.simulator.master.after(config.simulator_mapfrequency, self.periodic_check)

    def findSP(self):
        pass

    def run(self):
        pass

    def check_left(self):
        robot_location = self.handler.map.get_robot_location()
        print(robot_location)
        left_direction = self.handler.map.get_robot_direction_left()
        map_explored = self.map.get_map()
        if left_direction == 'N':
            if robot_location[0] < 2:
                return False
            if map_explored[robot_location[0]-2][robot_location[1]] == 1 and map_explored[robot_location[0]-2][robot_location[1]-1] == 1 and map_explored[robot_location[0]-2][robot_location[1]+1] == 1:
                return True
            else:
                return False
        elif left_direction == 'S':
            if robot_location[0] > 12:
                return False
            if map_explored[robot_location[0]+2][robot_location[1]] == 1 and map_explored[robot_location[0]+2][robot_location[1]-1] == 1 and map_explored[robot_location[0]+2][robot_location[1]+1] == 1:
                return True
            else:
                return False
        elif left_direction == 'E':
            if robot_location[1] > 17:
                return False
            if map_explored[robot_location[0]][robot_location[1]+2] == 1 and map_explored[robot_location[0]+1][robot_location[1]+2] == 1 and map_explored[robot_location[0]-1][robot_location[1]+2] == 1:
                return True
            else:
                return False
        elif left_direction == 'W':
            if robot_location[1] < 2:
                return False
            if map_explored[robot_location[0]][robot_location[1]-2] == 1 and map_explored[robot_location[0]+1][robot_location[1]-2] == 1 and map_explored[robot_location[0]-1][robot_location[1]-2] == 1:
                return True
            else:
                return False

        else:
            print("[Error] Invalid direction.")

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
# Assumption made on this algorithm:
#   - turning left, turning right, and move forward are considered 1 move
# ----------------------------------------------------------------------
class algoDFS(algoAbstract):
    def __init__(self, handler):
        super().__init__(handler)
        self.gotoList = [   (1,1,None),     (7,3,'N'),      (9,11,None),
                            (5,11,'S'),     (5,11,'N'),
                            (1,1,None),     (13,1,None),    (13,18,None) ]       # a STACK, executed from tail / last element

    def explore(self, useSimulator=True):
        if not self.gotoList:
            return
        loc = self.gotoList.pop()
        self.act = self.gotoYX( loc[0], loc[1], loc[2] )
        self.stopFlag = False
        if (useSimulator):
            self.periodic_check()

    def periodic_check(self):
        if self.act:
            tmp = self.act.pop()
            self.handler.command(tmp)
        if not self.stopFlag:
            if (self.act):
                self.handler.simulator.master.after(config.simulator_mapfrequency, self.periodic_check)
            else:
                self.handler.simulator.master.after(config.simulator_mapfrequency, self.explore)

    # ------------------------------------------------------------------
    # map related own function
    # ------------------------------------------------------------------
    DIRECTIONS  = ('N', 'E', 'S', 'W')
    # dispY       = (( 1, 0),  ( 0, 1),  (-1, 0),  ( 0,-1))
    # dispX       = (( 0, 1),  (-1, 0),  ( 0,-1),  ( 1, 0))
    # dispMtx     = ((-2,-1), (-2, 0), (-2, 1))      # displacement Matrix
    locDisp     = ((-1, 0),  ( 0, 1),  ( 1, 0),  ( 0,-1))

    Displacement= ( ((-2,-1), (-2, 0), (-2, 1)),   # North
                    ((-1, 2), ( 0, 2), ( 1, 2)),   # East
                    (( 2, 1), ( 2, 0), ( 2,-1)),   # South
                    (( 1,-2), ( 0,-2), (-1,-2))    # West
                )

    # return True if the 3x1 boxes adjacent to robot are free given robot location (y,x)
    # idx in parameter is an integer value equivalent to DIRECTIONS.index(direction)
    def __areFree(self, y, x, idx):
        # Matrix computation to get the boxes given the direction
        verbose('__areFree', y, x, idx, tag='Algo DFS', lv='deepdebug')
        for i in self.Displacement[idx]:
            if not self.map.isFree(i[0]+y, i[1]+x):
                return False
        return True

    # ------------------------------------------------------------------


    # return A STACK (list, last element as top) of command,
    #     the shortest known path to coordinate (y,x) using BFS algorithm
    # 
    def gotoYX(self, y, x, faceto=None):
        map = self.map
        loc = map.get_robot_location()                                          # original location
        drcO= self.DIRECTIONS.index(map.get_robot_direction())                  # original direction
        drc = drcO
        mvt = [[[-1]*4 for i in range(map.width)] for j in range(map.height)]   # flag and step; -1 unvisited; -2 source; otherwise index of DIRECTIONS
        step= 0
        ret = None

        q = queue.Queue()
        q.put((loc[0],loc[1],drc,-2))                       # push source node into queue
        while (not q.empty()) and (ret == None):
            sz = q.qsize()
            verbose('gotoYX ({},{}): step {}; size {};'.format(y, x, step, sz), tag='Algo DFS', lv='debug')
            while sz > 0:
                sz  = sz-1
                fr  = q.get()
                locY= fr[0]
                locX= fr[1]
                drc = fr[2]

                # skip if visited before
                if mvt[locY][locX][drc] != -1:
                    continue
                mvt[locY][locX][drc] = fr[3]

                verbose('> Pop queue item and execute: ', fr, tag=None, lv='deepdebug', pre='\t')
                # print('>>>', locY, locX, drc, ':', mvt[locY][locX], mvt[1][2], sep=' ')

                # Terminate condition
                if (locY == y) and (locX == x) and ((faceto == None) or (faceto == self.DIRECTIONS[drc])):
                    ret = drc
                    break

                # move forward
                nextY   = locY + self.locDisp[drc][0]
                nextX   = locX + self.locDisp[drc][1]
                # print('>>>', nextY, nextX, drc, ':', mvt[nextY][nextX][drc], sep=' ')
                if (mvt[nextY][nextX][drc]==-1) and (self.__areFree( locY, locX, drc )):
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
                    verbose('ERROR: gotoYX trace back failed.', tag='Algo DFS', pre='  ')
                    return None

        # ret.reverse()     # see return format on the top of this function
        return ret


# ----------------------------------------------------------------------
