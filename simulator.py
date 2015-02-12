try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    import ttk

from map import *
from sensor_simulator import SensorSimulator
from algo import *
import config
import threading
import queue
import time
from sensor_data import *


class SimulatorUI:
    def __init__(self, handler, title="Map Simulator"):

        self.master  = Tk()
        self.master.title(title)
        self.map     = handler.map
        self.handler = handler

        # Unfinished merging process
        # self.algo = algoFactory(self.map, client)
        self.algo = algoDum()

        t = Toplevel(self.master)
        t.title("Control Panel")
        t.geometry('180x360+1050+28')

        # left side map panel
        self.map_pane = ttk.Frame(self.master, borderwidth=0, relief="solid")
        self.map_pane.grid(column=0, row=0, sticky=(N, S, E, W))
        # right side control panel
        self.control_pane = ttk.Frame(t, padding=(12, 10))
        self.control_pane.grid(column=1, row=0, sticky=(N, S, E, W))

        # robot size
        self.robot_size     = config.robot_detail['size']
        # stores instances of widgets on the map
        self.map_widget     = [[None]*self.map.width]*self.map.height

        # photo instances
        self.robot_n = []
        self.robot_s = []
        self.robot_e = []
        self.robot_w = []
        for i in range(9):
            self.robot_n += [PhotoImage(file=config.icon_path['north'][i])]
            self.robot_s += [PhotoImage(file=config.icon_path['south'][i])]
            self.robot_w += [PhotoImage(file=config.icon_path['west'][i])]
            self.robot_e += [PhotoImage(file=config.icon_path['east'][i])]
        self.map_free               = PhotoImage(file=config.icon_path['free'])
        self.map_free_explored      = PhotoImage(file=config.icon_path['explored_free'])
        self.map_obstacle           = PhotoImage(file=config.icon_path['obstacle'])
        self.map_obstacle_explored  = PhotoImage(file=config.icon_path['explored_obstacle'])
        self.map_start              = PhotoImage(file=config.icon_path['start'])
        self.map_end                = PhotoImage(file=config.icon_path['end'])


        # map initialization.
        self.update_map()


        # unfinished
            # control_pane_window = ttk.Panedwindow(self.control_pane, orient=VERTICAL)
            # control_pane_window.grid(column=0, row=0, sticky=(N, S, E, W))
            # parameter_pane = ttk.Labelframe(control_pane_window, text='Parameters')
            # action_pane = ttk.Labelframe(control_pane_window, text='Action')
            # control_pane_window.add(parameter_pane, weight=4)
            # control_pane_window.add(action_pane, weight=1)

            # explore_button = ttk.Button(action_pane, text='Explore', width=16, command=self.algo.explore)
            # explore_button.grid(column=0, row=0, sticky=(W, E))
            # fastest_path_button = ttk.Button(action_pane, text='Fastest Path', command=self.algo.run)
            # fastest_path_button.grid(column=0, row=1, sticky=(W, E))
            # move_button = ttk.Button(action_pane, text='Move', command=self.move)
            # move_button.grid(column=0, row=2, sticky=(W, E))
            # left_button = ttk.Button(action_pane, text='Left', command=self.left)
            # left_button.grid(column=0, row=3, sticky=(W, E))
            # right_button = ttk.Button(action_pane, text='Right', command=self.right)
            # right_button.grid(column=0, row=4, sticky=(W, E))

            # step_per_second = StringVar()
            # step_per_second_label = ttk.Label(parameter_pane, text="Step Per Second:")
            # step_per_second_label.grid(column=0, row=0, sticky=W)
            # step_per_second_entry = ttk.Entry(parameter_pane, textvariable=step_per_second)
            # step_per_second_entry.grid(column=0, row=1, pady=(0, 10))

            # coverage_figure = StringVar()
            # coverage_figure_label = ttk.Label(parameter_pane, text="Coverage Figure(%):")
            # coverage_figure_label.grid(column=0, row=2, sticky=W)
            # coverage_figure_entry = ttk.Entry(parameter_pane, textvariable=coverage_figure)
            # coverage_figure_entry.grid(column=0, row=3, pady=(0, 10))

            # time_limit = StringVar()
            # time_limit_label = ttk.Label(parameter_pane, text="Time Limit(s):")
            # time_limit_label.grid(column=0, row=4, sticky=W)
            # time_limit_entry = ttk.Entry(parameter_pane, textvariable=time_limit)
            # time_limit_entry.grid(column=0, row=5, pady=(0, 10))

            # self.root.columnconfigure(0, weight=1)
            # self.root.rowconfigure(0, weight=1)
            # self.control_pane.columnconfigure(0, weight=1)
            # self.control_pane.rowconfigure(0, weight=1)

            # for i in range(10):
            #     map_pane.rowconfigure(i, weight=1)
            # for j in range(15):
            #     map_pane.columnconfigure(j, weight=1)

        self.master.bind("<Left>", lambda e: handler.left())
        self.master.bind("<Right>", lambda e: handler.right())
        self.master.bind("<Up>", lambda e: handler.move())
        self.master.bind("<Down>", lambda e: handler.back())

            # self.update_sensor()

        # self.master.mainloop()


    def put_robot(self, x, y, direction):
        if direction == 'N':
            robot_image = self.robot_n
        elif direction == 'S':
            robot_image = self.robot_s
        elif direction == 'W':
            robot_image = self.robot_w
        else:
            robot_image = self.robot_e

        for i in range(3):
            for j in range(3):
                cell = ttk.Label(self.map_pane, image=robot_image[i*3+j], borderwidth=1)
                try:
                    self.map_pane[x+i-1][y+j-1].destroy()
                except Exception:
                    pass
                cell.grid(column=y+j-1, row=x+i-1)
                self.map_widget[x+i-1][y+j-1] = cell


    def put_map(self, x, y):
        # Start & End box
        if   ((0 <= y < 3) and
              (0 <= x < 3)):
                map_image = self.map_start
        elif ((self.map.width -3 <= y < self.map.width) and
              (self.map.height-3 <= x < self.map.height)):
                map_image = self.map_end

        # Map Unexplored
        elif not self.map.isExplored(x,y):
            if self.map.isObstacle(x,y):
                map_image = self.map_obstacle
            else:
                map_image = self.map_free
        
        # Map Explored
        else:
            if self.map.isObstacle(x,y):
                map_image = self.map_obstacle_explored
            else:
                map_image = self.map_free_explored

        # Change map
        cell = ttk.Label(self.map_pane, image=map_image, borderwidth=1)
        try:
            self.map_pane[x][y].destroy()
        except Exception:
            pass
        cell.grid(column=y, row=x)
        self.map_widget[x][y] = cell


    def update_map(self):
        robot_location  = self.handler.get_robot_location()
        robot_direction = self.handler.get_robot_direction()
        for i in range(self.map.height):
            for j in range(self.map.width):
                if (robot_location[0]-1 <= i <= robot_location[0]+1 and
                    robot_location[1]-1 <= j <= robot_location[1]+1):
                    if i == robot_location[0] and j == robot_location[1]:
                        if robot_direction == 'N':
                            self.put_robot(i, j, 'N')
                        elif robot_direction == 'S':
                            self.put_robot(i, j, 'S')
                        elif robot_direction == 'W':
                            self.put_robot(i, j, 'W')
                        else:
                            self.put_robot(i, j, 'E')
                else:
                    self.put_map(i, j)

    

# ----------------------------------------------------------------------
# class SimulatorThread
# ----------------------------------------------------------------------
#     Return:
#         thread for simulator UI
#
#     Thread class with a stop() method. The thread itself has to check
#     regularly for the stopped() condition.
# ----------------------------------------------------------------------
class SimulatorThread(threading.Thread):
    def __init__(self, handler):
        super().__init__()
        self._stop  = threading.Event()
        self.the_UI = SimulatorUI(handler)

    def run(self):
        print("simulator_UI starts")
        self.the_UI.master.mainloop()
        print("simulator_UI exits")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
# ----------------------------------------------------------------------

class wut:
    def __init__(self, master):
        self.master = master

        self.event_queue = queue.Queue()
        print("[Current Thread] ", threading.current_thread())
        # self.simulator = SimulatorUI(self.master, self)
        self.sensor_buffer = queue.Queue()
        self.sensor_simulator = SensorSimulator(self.map, self.sensor_buffer)
        self.sensor_thread = threading.Thread(name="SensorThread", target=self.sensor_simulator.send_sendsor_data)
        self.sensor_thread.start()
        self.sensor_data_handler = SensorDataHandler(self.map, self.simulator)

        print("[Current Thread] ", threading.current_thread())
        # sensor_data_test = SensorData([1, 1], 'E',
        #                                   {'front_middle': 10,
        #                                    'front_left': 10,
        #                                    'front_right': 10})
        # self.sensor_data_handler.update_map(sensor_data_test)

        self.simulator_UI = SimulatorUI(self.master, self.event_queue, sensor=self.sensor_simulator)

        # self.sensor_thread = threading.Thread(name="sensor thread", target=self.sensor_simulator.issue_command)

        # self.sensor_thread.start()

    #     self.periodic_call()
    #
    # def periodic_call(self):
    #     print("[Periodic Run]")
    #     self.simulator_UI.action()
    #     self.master.after(50, self.periodic_call)


