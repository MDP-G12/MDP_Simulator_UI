import time
import threading
from sensor_data_handler import *
from sensor_simulator import *
from sensor_data import *


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
    def __init__(self, map_info, simulator, algoName="BF1"):
        if (algoName == "BF1"):
            self.algo = algoBF1(map_info, simulator)
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
    def __init__(self, map_info, simulator):
        self.simulator = simulator
        self.map_info = map_info

    def explore(self):
        sensor_buffer = []
        buffer_lock = threading.Lock()
        sensor_simulator = SensorSimulator(self.map_info, sensor_buffer, buffer_lock)
        sensor_thread = threading.Thread(name="SensorThread", target=sensor_simulator.send_sendsor_data)
        sensor_thread.start()
        sensor_data_handler = SensorDataHandler(self.map_info, self.simulator)
        count = 10
        # for i in range(count):
        #     sensor_data = sensor_buffer.pop(0)
        #     sensor_data_handler.update_map(sensor_data)
        #     self.sim.move()
        #     time.sleep(1)

        while True:
            print("[Current Thread] ", threading.current_thread())
            buffer_lock.acquire()
            if len(sensor_buffer):
                sensor_data = sensor_buffer.pop(0)
                self.map_info.map_lock.acquire()
                print("[Map Lock] Locked by ", threading.current_thread())
                sensor_data_handler.update_map(sensor_data)
                if count > 0:
                    self.issue_command('move')
                    # self.sim.move()
                    count -= 1
                else:
                    return
                self.map_info.map_lock.release()
                print("[Map Lock] Released by ", threading.current_thread())

            buffer_lock.release()
            print('[Thread] ', threading.current_thread(), 'Giving up control')
            time.sleep(0.5)

        # i = 1
        # while (True):
        #     if ((i%13) > 0):
        #         # self.sim.move_delay(i)
        #         self.issue_command('move')
        #     else:
        #         # self.sim.right_delay(i)
        #         self.issue_command('right')
        #     i = i + 1
        #     if (i > 200):
        #         break
        # while

    def findSP(self):
        pass

    def run(self):
        pass

    def issue_command(self, command):
        # time.sleep(1)
        print("[Thread] ", threading.current_thread())
        self.simulator.event_queue.put(command)
        print("Command: " + command)
        # print('[Thread] ', threading.current_thread(), 'Giving up control')
        # time.sleep(1)

    # def periodic_call(self):
    #     while True:
    #         if ()
    #     return