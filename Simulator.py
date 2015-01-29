from tkinter import *
from tkinter import ttk
from Map import *
import config


class Simulator:
    def __init__(self):

        self.root = Tk()
        self.root.title("Map Simulator")

        # s = ttk.Style()
        # s.theme_use('aqua')

        # left side map panel
        self.map_pane = ttk.Frame(self.root, borderwidth=1, relief="solid")
        self.map_pane.grid(column=0, row=0, sticky=(N, S, E, W))
        # right side control panel
        self.control_pane = ttk.Frame(self.root, padding=(12, 10))
        self.control_pane.grid(column=1, row=0, sticky=(N, S, E, W))
        # map size
        self.map_height = config.map_detail['height']
        self.map_width = config.map_detail['width']
        # robot size
        self.robot_size = config.robot_detail['size']
        # stores instances of widgets on the map
        self.map_widget = [[None]*self.map_width]*self.map_height

        # photo instances
        self.robot_n = PhotoImage(file=config.icon_path['north'])
        self.robot_s = PhotoImage(file=config.icon_path['south'])
        self.robot_e = PhotoImage(file=config.icon_path['east'])
        self.robot_w = PhotoImage(file=config.icon_path['west'])
        self.map_free = PhotoImage(file=config.icon_path['free'])
        self.map_obstacle = PhotoImage(file=config.icon_path['obstacle'])

        # cell_N = ttk.Label(map_pane, image=image_N, borderwidth=1, relief="solid")
        # cell_S = ttk.Label(map_pane, image=image_S, borderwidth=1, relief="solid")
        # cell_E = ttk.Label(map_pane, image=image_E, borderwidth=1, relief="solid")
        # cell_W = ttk.Label(map_pane, image=image_W, borderwidth=1, relief="solid")

        # ----------------------------------------------------------------------
        # map initialization.
        # map_info = Map()      =>  see Map.py
        # ----------------------------------------------------------------------
        for i in range(self.map_height):
            for j in range(self.map_width):
                if map_info.robot[0] <= i <= map_info.robot[0]+2 and map_info.robot[1] <= j <= map_info.robot[1]+2:
                    if map_info.robot_direction == 'N':
                        self.put_robot(i, j, 'N')
                    elif map_info.robot_direction == 'S':
                        self.put_robot(i, j, 'S')
                    elif map_info.robot_direction == 'W':
                        self.put_robot(i, j, 'W')
                    else:
                        self.put_robot(i, j, 'E')
                else:
                    self.put_map(i, j)

        control_pane_window = ttk.Panedwindow(self.control_pane, orient=VERTICAL)
        control_pane_window.grid(column=0, row=0, sticky=(N, S, E, W))
        parameter_pane = ttk.Labelframe(control_pane_window, text='Parameters')
        action_pane = ttk.Labelframe(control_pane_window, text='Action')
        control_pane_window.add(parameter_pane, weight=4)
        control_pane_window.add(action_pane, weight=1)

        explore_button = ttk.Button(action_pane, text='Explore', width=16)
        explore_button.grid(column=0, row=0, sticky=(W, E))
        fastest_path_button = ttk.Button(action_pane, text='Fastest Path')
        fastest_path_button.grid(column=0, row=1, sticky=(W, E))
        move_button = ttk.Button(action_pane, text='Move', command=self.move)
        move_button.grid(column=0, row=2, sticky=(W, E))
        left_button = ttk.Button(action_pane, text='Left', command=self.left)
        left_button.grid(column=0, row=3, sticky=(W, E))
        right_button = ttk.Button(action_pane, text='Right', command=self.right)
        right_button.grid(column=0, row=4, sticky=(W, E))

        step_per_second = StringVar()
        step_per_second_label = ttk.Label(parameter_pane, text="Step Per Second:")
        step_per_second_label.grid(column=0, row=0, sticky=W)
        step_per_second_entry = ttk.Entry(parameter_pane, textvariable=step_per_second)
        step_per_second_entry.grid(column=0, row=1, pady=(0, 10))

        coverage_figure = StringVar()
        coverage_figure_label = ttk.Label(parameter_pane, text="Coverage Figure(%):")
        coverage_figure_label.grid(column=0, row=2, sticky=W)
        coverage_figure_entry = ttk.Entry(parameter_pane, textvariable=coverage_figure)
        coverage_figure_entry.grid(column=0, row=3, pady=(0, 10))

        time_limit = StringVar()
        time_limit_label = ttk.Label(parameter_pane, text="Time Limit(s):")
        time_limit_label.grid(column=0, row=4, sticky=W)
        time_limit_entry = ttk.Entry(parameter_pane, textvariable=time_limit)
        time_limit_entry.grid(column=0, row=5, pady=(0, 10))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.control_pane.columnconfigure(0, weight=1)
        self.control_pane.rowconfigure(0, weight=1)

        # for i in range(10):
        #     map_pane.rowconfigure(i, weight=1)
        # for j in range(15):
        #     map_pane.columnconfigure(j, weight=1)

        self.root.bind("<Left>", lambda e: self.left())
        self.root.bind("<Right>", lambda e: self.right())
        self.root.bind("<Up>", lambda e: self.move())
        self.root.mainloop()

    def put_robot(self, x, y, direction):
        if direction == 'N':
            robot_image = self.robot_n
        elif direction == 'S':
            robot_image = self.robot_s
        elif direction == 'W':
            robot_image = self.robot_w
        else:
            robot_image = self.robot_e
        cell = ttk.Label(self.map_pane, image=robot_image, borderwidth=1, relief="solid")
        try:
            self.map_pane[x][y].destroy()
        except Exception:
            pass
        cell.grid(column=y, row=x)
        self.map_widget[x][y] = cell

    def put_map(self, x, y):
        map_image = self.map_obstacle if map_info.map_real[x][y] else self.map_free
        cell = ttk.Label(self.map_pane, image=map_image, borderwidth=1, relief="solid")
        try:
            self.map_pane[x][y].destroy()
        except Exception:
            pass
        cell.grid(column=y, row=x)
        self.map_widget[x][y] = cell


    # ----------------------------------------------------------------------
    #   Function valid_pos
    # ----------------------------------------------------------------------
    # parameter:
    #   y   -   row position to be validated of robot
    #   x   -   coloumn position to be validated of robot
    # ----------------------------------------------------------------------
    def valid_pos(self, y, x):
        ret = True if ((0 <= y) and (y < self.map_height-self.robot_size) and
                        (0 <= x) and (x < self.map_width-self.robot_size)) else False
        if ret == True:
            for i in range (y, y+self.robot_size):
                for j in range (x, x+self.robot_size):
                    if (map_info.map_real[i][j] == 1):
                        return False
        return ret


    def move(self):
        print("Action: move forward")
        if map_info.robot_direction == 'N':
            robot_next = [map_info.robot[0]-1, map_info.robot[1]]
        elif map_info.robot_direction == 'S':
            robot_next = [map_info.robot[0]+1, map_info.robot[1]]
        elif map_info.robot_direction == 'W':
            robot_next = [map_info.robot[0], map_info.robot[1]-1]
        elif map_info.robot_direction == 'E':
            robot_next = [map_info.robot[0], map_info.robot[1]+1]
        else:
            print("    [ERROR] Direction undefined!")
            return

        if (self.valid_pos(map_info.robot[0], map_info.robot[1]) == False):
            print("    [WARNING] Not moving due to obstacle or out of bound")
            return

        # TODO:
        #   - updating value: map_info.robot
        #   - updating map: put_robot and put_map
        
        # if map_info.robot_direction == 'N':
        #     if map_info.robot[0] > 0:
        #         self.put_map(map_info.robot[0]+2, map_info.robot[1])
        #         self.put_map(map_info.robot[0]+2, map_info.robot[1]+1)
        #         self.put_map(map_info.robot[0]+2, map_info.robot[1]+2)

        #         self.put_robot(map_info.robot[0]-1, map_info.robot[1], 'N')
        #         self.put_robot(map_info.robot[0]-1, map_info.robot[1]+1, 'N')
        #         self.put_robot(map_info.robot[0]-1, map_info.robot[1]+2, 'N')

        #         map_info.robot[0] -= 1
        # elif map_info.robot_direction == 'S':
        #     if map_info.robot[0] < 7:
        #         self.put_map(map_info.robot[0], map_info.robot[1])
        #         self.put_map(map_info.robot[0], map_info.robot[1]+1)
        #         self.put_map(map_info.robot[0], map_info.robot[1]+2)

        #         self.put_robot(map_info.robot[0]+3, map_info.robot[1], 'S')
        #         self.put_robot(map_info.robot[0]+3, map_info.robot[1]+1, 'S')
        #         self.put_robot(map_info.robot[0]+3, map_info.robot[1]+2, 'S')

        #         map_info.robot[0] += 1

        # elif map_info.robot_direction == 'W':
        #     if map_info.robot[1] > 0:
        #         self.put_map(map_info.robot[0], map_info.robot[1]+2)
        #         self.put_map(map_info.robot[0]+1, map_info.robot[1]+2)
        #         self.put_map(map_info.robot[0]+2, map_info.robot[1]+2)

        #         self.put_robot(map_info.robot[0], map_info.robot[1]-1, 'W')
        #         self.put_robot(map_info.robot[0]+1, map_info.robot[1]-1, 'W')
        #         self.put_robot(map_info.robot[0]+2, map_info.robot[1]-1, 'W')

        #         map_info.robot[1] -= 1
        # elif map_info.robot_direction == 'E':
        #     if map_info.robot[1] < 12:
        #         self.put_map(map_info.robot[0], map_info.robot[1])
        #         self.put_map(map_info.robot[0]+1, map_info.robot[1])
        #         self.put_map(map_info.robot[0]+2, map_info.robot[1])

        #         self.put_robot(map_info.robot[0], map_info.robot[1]+3, 'E')
        #         self.put_robot(map_info.robot[0]+1, map_info.robot[1]+3, 'E')
        #         self.put_robot(map_info.robot[0]+2, map_info.robot[1]+3, 'E')

        #         map_info.robot[1] += 1

    def left(self):
        print("Action: turn left")
        map_info.robot_direction = DIRECTIONS[(DIRECTIONS.index(map_info.robot_direction)+3) % 4]
        for i in range(3):
            for j in range(3):
                self.put_robot(map_info.robot[0]+i, map_info.robot[1]+j, map_info.robot_direction)

    def right(self):
        print("Action: turn right")
        map_info.robot_direction = DIRECTIONS[(DIRECTIONS.index(map_info.robot_direction)+5) % 4]
        for i in range(3):
            for j in range(3):
                self.put_robot(map_info.robot[0]+i, map_info.robot[1]+j, map_info.robot_direction)

DIRECTIONS = ['N', 'E', 'S', 'W']

map_info = Map()
map_simulator = Simulator()

# while True:
#     command = input("Please issue a command:")
#     if command == "move":
#         map_simulator.move()
