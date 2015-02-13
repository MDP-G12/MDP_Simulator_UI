import time
import threading
from sensor import *


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
        self.counter = 0

    def explore(self):
        robot_location  = self.map.get_robot_location()

    # def periodic_check(self):
    #     if self.client.sensor_buffer.qsize():
    #         self.client.sensor_data_handler.update_map(self.client.sensor_buffer.get())
    #         if self.counter < 30:
    #             self.counter += 1
    #             if self.counter % 18 == 0:
    #                 self.client.simulator.right()
    #             else:
    #                 self.client.simulator.move()
    #         else:
    #             return
    #     self.client.master.after(100, self.periodic_check)

    def findSP(self):
        pass

    def run(self):
        pass

    # def issue_command(self, command):
    #     # time.sleep(1)
    #     print("[Thread] ", threading.current_thread())
    #     self.simulator.event_queue.put(command)
    #     print("Command: " + command)
        # print('[Thread] ', threading.current_thread(), 'Giving up control')
        # time.sleep(1)

    # def periodic_call(self):
    #     while True:
    #         if ()
    #     return