from tkinter import *
from tkinter import ttk
from map import Map


class Simulator:
    def __init__(self, map_info):
        root = Tk()
        root.title("Map Simulator")

        # s = ttk.Style()
        # s.theme_use('aqua')

        map_pane = ttk.Frame(root, borderwidth=1, relief="solid")
        map_pane.grid(column=0, row=0, sticky=(N, S, E, W))
        control_pane = ttk.Frame(root, padding=(12, 10))
        control_pane.grid(column=1, row=0, sticky=(N, S, E, W))

        map_widget = []

        robot_n = PhotoImage(file='images/icon_N.gif')
        robot_s = PhotoImage(file='images/icon_S.gif')
        robot_e = PhotoImage(file='images/icon_E.gif')
        robot_w = PhotoImage(file='images/icon_W.gif')
        map_free = PhotoImage(file='images/green.gif')
        map_obstacle = PhotoImage(file='images/red.gif')

        # cell_N = ttk.Label(map_pane, image=image_N, borderwidth=1, relief="solid")
        # cell_S = ttk.Label(map_pane, image=image_S, borderwidth=1, relief="solid")
        # cell_E = ttk.Label(map_pane, image=image_E, borderwidth=1, relief="solid")
        # cell_W = ttk.Label(map_pane, image=image_W, borderwidth=1, relief="solid")

        for i in range(10):
            row = []
            for j in range(15):
                if map_info.robot[0] <= i <= map_info.robot[0]+2 and map_info.robot[1] <= j <= map_info.robot[1]+2:
                    if map_info.robot_direction == 'N':
                        robot_image = robot_n
                    elif map_info.robot_direction == 'S':
                        robot_image = robot_s
                    elif map_info.robot_direction == 'W':
                        robot_image = robot_w
                    else:
                        robot_image = robot_e
                    cell = ttk.Label(map_pane, image=robot_image, borderwidth=1, relief="solid")
                elif map_info.map_real[i][j] == 0:
                    cell = ttk.Label(map_pane, image=map_free, borderwidth=1, relief="solid")
                else:
                    cell = ttk.Label(map_pane, image=map_obstacle, borderwidth=1, relief="solid")
                cell.grid(column=j, row=i)
                row.append(cell)
            map_widget.append(row)

        control_pane_window = ttk.Panedwindow(control_pane, orient=VERTICAL)
        control_pane_window.grid(column=0, row=0, sticky=(N, S, E, W))
        parameter_pane = ttk.Labelframe(control_pane_window, text='Parameters')
        action_pane = ttk.Labelframe(control_pane_window, text='Action')
        control_pane_window.add(parameter_pane, weight=20)
        control_pane_window.add(action_pane, weight=1)

        explore_button = ttk.Button(action_pane, text='Explore', padding=(20, 10))
        explore_button.grid(column=0, row=0, sticky=(W, E), pady=(0, 10))
        fastest_path_button = ttk.Button(action_pane, text='Fastest Path', padding=(20, 10))
        fastest_path_button.grid(column=0, row=1, stick=(W, E))

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

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        control_pane.columnconfigure(0, weight=1)
        control_pane.rowconfigure(0, weight=1)

        # for i in range(10):
        #     map_pane.rowconfigure(i, weight=1)
        # for j in range(15):
        #     map_pane.columnconfigure(j, weight=1)

        root.mainloop()


map_info = Map()
map_simulator = Simulator(map_info)