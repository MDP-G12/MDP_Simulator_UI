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
        self.gotoList = None

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

    # return True if the 3x1 boxes adjacent to robot are free given robot location (y,x)
    # idx in parameter is an integer value equivalent to DIRECTIONS.index(direction)
    #
    def __areFree(self, y, x, idx):
        # Matrix computation to get the boxes given the direction
        verbose('__areFree', y, x, idx, tag='Algo DFS', lv='deepdebug')
        for i in self.Displacement[idx]:
            if not self.map.isFree(i[0]+y, i[1]+x, config.algoMapKnown):
                return False
        return True


    # return A STACK (list, last element as top) of command,
    #     the shortest known path to coordinate (y,x) using BFS algorithm
    # 
    def gotoYX(self, y, x, faceto=None, loc=None, drcO=None):
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


        # --------------------
        # the BFS
        q = queue.Queue()
        q.put((loc[0],loc[1],drc,-2))                       # push source node into queue
        while (not q.empty()) and (ret == None):
            sz = q.qsize()
            verbose('gotoYX ({},{}): step {}; size {};'.format(y, x, step, sz), tag='Algo DFS', lv='debug')
            while sz > 0:
                sz  = sz-1
                fr  = q.get()
                [locY, locX, drc] = fr[:3]

                # skip if visited before
                if mvt[locY][locX][drc] != -1:
                    continue
                mvt[locY][locX][drc] = fr[3]

                if (locY < 0 or locX < 0):
                    print("\n\tWOWOW: ", y, x, '---\n')

                verbose('> Pop queue item and execute (fr, y, x, d, faceto) ', fr, locY, locX, drc, faceto, tag=None, lv='deepdebug', pre='\t')
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
                    verbose('ERROR: gotoYX trace back failed.', tag='Algo DFS', pre='  ')
                    return None


        # --------------------
        # ret.reverse()     # see return format on the top of this function
        return ret

    # ------------------------------------------------------------------


    def explore(self):
        # if not self.gotoList:
        #     self.gotoList = [   (1,1,None),     (7,3,'N'),      (9,11,None),
        #                         (5,11,'S'),     (5,11,'N'),
        #                         (1,1,None),     (13,1,None),    (13,18,None) ]       # a STACK, executed from tail / last element
        # self.stopFlag = False
        # self.gotoListExec()

        verbose('exploring...', tag='Algo DFS')

        map             = self.map
        [robY, robX]    = map.get_robot_location()
        robD            = self.DIRECTIONS.index(map.get_robot_direction())
        visited         = [[[0]*4 for i in range(map.width)] for j in range(map.height)]
        s               = [(robY, robX, robD, None)]
        self.stopFlag   = False
        self.do_DFS(s, visited)


    def do_DFS(self, s, visited):
        # verbose('do_DFS', s, tag='Algo DFS', lv='debug')
        while s:
            top = s.pop()
            verbose('do_DFS', top, tag='Algo DFS', lv='debug')
            [locY, locX, drc, cmd] = top[:4]

            # if visited before
            if visited[locY][locX][drc]:
                continue

            # goto current state first
            if ((top[:2] != self.map.get_robot_location()) or
                (self.DIRECTIONS[top[2]] != self.map.get_robot_direction())):
                self.gotoList = [top[:3]]
                self.gotoListExec()
                # if self.handler.simulator

            # set flag
            visited[locY][locX][drc] = 1

            # assuming robot is at current state alr
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
            if (not visited[nextY][nextX][drc]) and (self.__areFree( locY, locX, drc )):
                s.append(( nextY, nextX, drc, 'F' ))


            # updating state for simulator
            if self.handler.simulator:
                if not self.stopFlag:
                    self.handler.simulator.master.after(config.simulator_mapfrequency, self.do_DFS, s, visited)
                break

    def do_unknown(self, s, visited):
        pass


    # Execute goto list
    def gotoListExec(self):
        if not self.gotoList:
            return
        if self.handler.simulator:
            loc = self.gotoList.pop()
            self.act = self.gotoYX( loc[0], loc[1], loc[2] )
            self.periodic_check(self.gotoListExec)
        else:
            while self.gotoList:
                loc = self.gotoList.pop()
                self.act = self.gotoYX( loc[0], loc[1], loc[2] )
                while self.act:
                    self.handler.command( self.act.pop() )

    def periodic_check(self, caller=None):
        if caller:
            verbose('periodic_check', caller.__name__, tag='Algo DFS', lv='deepdebug', pre='  ')
        else:
            verbose('periodic_check', tag='Algo DFS', lv='deepdebug', pre='  ')
        if self.act:
            self.handler.command( self.act.pop() )
        if not self.stopFlag:
            if (self.act):
                self.handler.simulator.master.after(config.simulator_mapfrequency, self.periodic_check, caller)
            elif caller != None:
                self.handler.simulator.master.after(config.simulator_mapfrequency, caller)

    def findSP(self):
        return self.gotoYX(13,18, loc=(1,1), drcO='E') + self.gotoYX(1,1,'E')

    def run(self):
        self.act = self.findSP()
        self.stopFlag = False
        if self.handler.simulator:
            self.periodic_check(None)
        else:
            while self.act:
                self.handler.command( self.act.pop() )



# ----------------------------------------------------------------------
