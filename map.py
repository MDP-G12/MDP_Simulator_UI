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
from copy import deepcopy

class Map:
    DIRECTIONS = ('N', 'E', 'S', 'W')

    def __init__(self):
        self.map_lock = threading.Lock()
        if not config.mapFileLocation:
            # ----------------------------------------------------------------------
            #   Map_real Legend:
            #       0 - free
            #       1 - obstacle
            # ----------------------------------------------------------------------
            self.__map_real =  deepcopy(config.map_detail['map_real'])
            
            # ----------------------------------------------------------------------
            #   Map Legend:
            #       0 - unexplored
            #       1 - explored; free
            #       2 - explored; obstacle
            # ----------------------------------------------------------------------
            self.__map      =  deepcopy(config.map_detail['map'])
        else:
            raise Exception

        self.height     = config.map_detail['height']
        self.width      = config.map_detail['width']
        self.mapStat    = ['unexplored', 'free', 'obstacle']
        
        # ----------------------------------------------------------------------
        #   Robot
        # ----------------------------------------------------------------------
        self.__robot_location   = [1, 1]
        self.__robot_direction  = 'E'
        self.__rsize            = config.robot_detail['size']


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
        if self.valid_robot_loc(loc[0], loc[1]):
            self.__robot_location = loc
        else:
            verbose( "Error: Location update out of range", tag="Map", lv='quiet' )

    def set_robot_direction(self, direction):
        if (direction in Map.DIRECTIONS):
            self.__robot_direction = direction
        else:
            verbose( "Error: Direction update invalid!", tag="Map", lv='quiet' )

    # set map special case: once set to free, wont be changed!
    def set_map(self, y, x, stat):
        if not self.valid_range(y, x):
            verbose( "Warning: map to be set is out of bound!", (y, x), tag="Map", lv='debug' )
            return

        if (stat in self.mapStat):
            if self.__map[y][x] != self.mapStat.index('free'):          # if the block to be changed is a free block
                self.__map[y][x] = self.mapStat.index(stat)
            elif self.mapStat.index(stat) != 'free':
                verbose( "Warning: intended box to be set is found to be free previously!", (y,x), tag="Map", lv='deepdebug' )
        else:
            verbose( "Error: set map wrong status!", tag="Map", lv='quiet' )

    def get_map(self):
        return self.__map

    # Comparing the values of 2D arrays, cmpmap with own map. True if values are same
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
    #   - isExplored, isFree, isObstacle, valid_range;
    #   - isFree and isObstacle return False on out of range/index,
    #     isExplored will give an warning msg and return True
    # ----------------------------------------------------------------------
    # parameter:
    #     y, x    - row index and coloumn index respectively
    # ----------------------------------------------------------------------
    def isExplored(self, y, x):
        if not self.valid_range(y,x):
            verbose('WARNING: isExplored Out of Index!', (y, x), tag='Map', pre='  ', lv='debug')
            return True;
        return (self.__map[y][x] != 0)

    def isObstacle(self, y, x, isMapKnown=True):
        if not self.valid_range(y,x):
            return False;
        if (self.__map[y][x] == 0):
            return (not isMapKnown) or (self.__map_real[y][x] == 1);
        return self.__map[y][x] == 2

    def isFree(self, y, x, isMapKnown=True):
        if not self.valid_range(y,x):
            return False;
        verbose( "isFree({0},{1}): {2}; real:{3}".format(y,x,self.__map[y][x],self.__map_real[y][x]), lv='deepdebug' )
        if (self.__map[y][x] == 0):
            return (isMapKnown) and (self.__map_real[y][x] == 0);
        return self.__map[y][x] == 1

    # to check whether the location is within range
    def valid_range(self, y, x):
        return (0 <= y < self.height) and (0 <= x < self.width)

    def valid_robot_loc(self, y, x):
        return ((0 + (self.__rsize>>1)   <= y <   self.height - (self.__rsize>>1)) and
                (0 + (self.__rsize>>1)   <= x <   self.width  - (self.__rsize>>1)))

    def countExplored(self):
        explored = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.__map[y][x] != 0:
                    explored += 1
        return explored
    # ----------------------------------------------------------------------



    # ----------------------------------------------------------------------
    # Grading criteria functions
    #   map to be descripted need to be rotated 90 degrees clockwise
    # ----------------------------------------------------------------------
    def print_descripted_map(self):
        print( self.descripted_map() )

    def descripted_map(self, printThis=False, form='x'):
        part1 = '11'            # the first '11'
        part2 = ''              # the second '11' - Part 1
        cnt   = 0               # part 2 bit counter for padding bit

        for x in range(self.width):
            for y in range(self.height):
                if (self.__map[y][x] != 0) :
                    cnt     += 1
                    part1   += '1'
                    part2   += '1' if (self.__map[y][x] == 2) else '0'
                else:
                    part1   += '0'
        part1 += '11'

        # Padding bits
        while (cnt%8):
            cnt     += 1
            part2   += '0'
        
        # Returning according format
        part1x = ''
        for i in range(len(part1)>>2):
            if (form == 'x' or form == 'X'):
                part1x += '%X' % int(part1[i*4:(i+1)*4], 2)
            elif (form == 'b' or form == 'B'):
                part1x = part1
                break

        part2x = ''
        for i in range(len(part2)>>2):
            if (form == 'x' or form == 'X'):
                part2x += '%X' % int(part2[i*4:(i+1)*4], 2)
            elif (form == 'b' or form == 'B'):
                part2x += part2
                break

        # print?
        if printThis:
            print(part1x, part2x, sep=';\n')

        return [part1x, part2x]

    # ----------------------------------------------------------------------

#################### End of Class ####################