# ----------------------------------------------------------------------
# class definition of Map.
# 
#   - self.__map_real
#           2 dimensional array that defines the map
#   - self.__map
#           2 dimensional array that defines the eplored part of the map
# 
#   - self.robot
#           A pair of integer that contains current position of robot.
#           Row and Coloumn respectively
#   - self.robot_direction
#           character that contains the direction of robot is heading to
# ----------------------------------------------------------------------

import config
import threading
from logger import *
from map import *

class Map:
    DIRECTIONS = ['N', 'E', 'S', 'W']

    def __init__(self):
        self.map_lock = threading.Lock()
        # ----------------------------------------------------------------------
        #   Map_real Legend:
        #       0 - free
        #       1 - obstacle
        # ----------------------------------------------------------------------
        self.__map_real =  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        # ----------------------------------------------------------------------
        #   Map Legend:
        #       0 - unexplored
        #       1 - explored; free
        #       2 - explored; obstacle
        # ----------------------------------------------------------------------
        self.__map      =  [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]

        self.height     = config.map_detail['height']
        self.width      = config.map_detail['width']
        self.mapStat    = ['unexplored', 'free', 'obstacle']
        
        # ----------------------------------------------------------------------
        #   Robot
        # ----------------------------------------------------------------------
        self.__robot_location = [1, 1]
        self.__robot_direction = 'E'


    # ----------------------------------------------------------------------
    #   Encapsulation functions
    # ----------------------------------------------------------------------
    def get_robot_location(self):
        return self.__robot_location

    def get_robot_direction(self):
        return self.__robot_direction

    def get_robot_direction_right(self):
        return Map.DIRECTIONS[ (Map.DIRECTIONS.index(self.__robot_direction)+1) % 4 ]
    def get_robot_direction_left(self):
        return Map.DIRECTIONS[ (Map.DIRECTIONS.index(self.__robot_direction)+3) % 4 ]
    def get_robot_direction_back(self):
        return Map.DIRECTIONS[ (Map.DIRECTIONS.index(self.__robot_direction)+2) % 4 ]

    def set_robot_location(self, loc):
        if ((0 <= loc[0] < self.height) and
            (0 <= loc[1] < self.width )):
            self.__robot_location = loc
        else:
            verbose( "Error: Location update out of range", tag="Map", lv='quiet' )

    def set_robot_direction(self, direction):
        if (direction in Map.DIRECTIONS):
            self.__robot_direction = direction
        else:
            verbose( "Error: Direction update invalid!", tag="Map", lv='quiet' )

    def set_map(self, y, x, stat):
        if not self.valid_range(y, x):
            verbose( "Warning: map to be set is out of bound!", tag="Map", lv='debug' )
            return

        if (stat in self.mapStat):
            self.__map[y][x] = self.mapStat.index(stat)
        else:
            verbose( "Error: set map wrong status!", tag="Map", lv='quiet' )

    def get_map(self):
        return self.__map

    def isSameMap(self, cmpmap):
        return cmpmap == self.__map
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    #   Function valid_pos
    # ----------------------------------------------------------------------
    # parameter:
    #   y   -   row position to be validated of robot
    #   x   -   coloumn position to be validated of robot
    # ----------------------------------------------------------------------
    def valid_pos(self, y, x):
        if not (0 < y < 14 and 0 < x < 19):
            return False
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if not self.valid_range(i,j) or self.isObstacle(i,j):
                    return False
        return True
    # ----------------------------------------------------------------------



    # ----------------------------------------------------------------------
    # map checking functions
    #     isExplored, isFree, isObstacle, valid_range
    # ----------------------------------------------------------------------
    # parameter:
    #     y, x    - row index and coloumn index respectively
    # ----------------------------------------------------------------------
    def isExplored(self, y, x):
        try:
            return (self.__map[y][x] != 0)
        except IndexError:
            print(y,x,sep="; ")

    def isObstacle(self, y, x):
        if (self.__map[y][x] == 0):
            return self.__map_real[y][x] == 1;
        return self.__map[y][x] == 2

    def isFree(self, y, x):
        verbose( "isFree({0},{1}): {2}; real:{3}".format(y,x,self.__map[y][x],self.__map_real[y][x]), lv='deepdebug' )
        if (self.__map[y][x] == 0):
            return self.__map_real[y][x] == 0;
        return self.__map[y][x] == 1

    # to check whether the location is within range
    def valid_range(self, y, x):
        return (0 <= y < self.height) and (0 <= x < self.width)
    # ----------------------------------------------------------------------



    # ----------------------------------------------------------------------
    # Grading criteria functions
    #   map to be descripted need to be rotated 90 degrees clockwise
    # ----------------------------------------------------------------------
    def descripted_map(self, printThis=False, form='x'):
        part1 = 3           # the first '11'
        part2 = 3           # the second '11' - Part 1
        cnt   = 0           # part 2 bit counter for padding bit

        for x in range(self.width):
            for y in range(self.height):
                part1 <<= 1
                if (self.__map[y][x] != 0) :
                    part1  |= 1
                    part2 <<= 1
                    cnt += 1
                    if (self.__map[y][x] == 2):
                        part2 |= 1
        
        
        # Padding bits
        cnt      %= 8
        part2   <<= 8-cnt

        # Returning accoring format
        part1 = format(part1,form)
        part2 = format(part2,form)
        if printThis:
            print(part1, part2, sep=';\n')

        return [part1, part2]

    # ----------------------------------------------------------------------

#################### End of Class ####################