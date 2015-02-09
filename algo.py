import time
import threading
from sensor_simulator import *

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
    def __init__(self, simulator, map_info, algoName="BF1"):
        if (algoName == "BF1"):
            self.algo = algoBF1(simulator, map_info)
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
    def __init__(self, simulator, map_info):
        self.sim = simulator
        self.map_info = map_info

    def explore(self):
        sensor_simulator = SensorSimulator(self.map_info, self.sim, self.sim.event_queue)
        sensor_thread = threading.Thread(name="SensorThread", target=sensor_simulator.update_map)
        sensor_thread.start()
        i = 1
        while (True):
            if ((i%13) > 0):
                # self.sim.move_delay(i)
                self.issue_command('move')
            else:
                # self.sim.right_delay(i)
                self.issue_command('right')
            i = i + 1
            if (i > 200):
                break

    def findSP(self):
        pass

    def run(self):
        pass

    def issue_command(self, command):
        # time.sleep(1)
        print("[Thread] ", threading.current_thread())
        self.sim.event_queue.put(command)
        print("Command: " + command)
