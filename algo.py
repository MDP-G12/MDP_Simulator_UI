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
# ----------------------------------------------------------------------


class algoAbstract:
    # def __init__(self):

    def explore(self):
        raise NotImplementedError

    def findSP(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


# ----------------------------------------------------------------------
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
        else:
            raise NameError('algoName not found')

    def explore(self):
        self.algo.explore()

    def findSP(self):
        self.algo.findSP()

    def run(self):
        self.algo.run()


# ----------------------------------------------------------------------
# class definition of algoBF1.
# Implementation class of algoAbstract using algorithm Brute Force #1
# ----------------------------------------------------------------------
class algoBF1(algoAbstract):
    def __init__(self, handler):
        self.handler    = handler
        self.map        = handler.map

    def explore(self):
        # robot_location  = self.map.get_robot_location()
        self.periodic_check()

    def periodic_check(self):
        self.handler.move()
        self.handler.simulator.master.after(500, self.periodic_check)

    def findSP(self):
        pass

    def run(self):
        pass


class LeftHandRule(algoAbstract):
    def __init__(self, handler):
        self.handler    = handler
        self.map        = handler.map

    def explore(self):
        self.periodic_check()

    def periodic_check(self):
        if self.check_left():
            self.handler.left()
        elif self.check_front():
            self.handler.move()
        else:
            self.handler.right()
        self.handler.simulator.master.after(500, self.periodic_check)

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