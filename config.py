icon_path = dict(
    north = ['images/robot/Robot_N_01.gif',
             'images/robot/Robot_N_02.gif',
             'images/robot/Robot_N_03.gif',
             'images/robot/Robot_N_04.gif',
             'images/robot/Robot_N_05.gif',
             'images/robot/Robot_N_06.gif',
             'images/robot/Robot_N_07.gif',
             'images/robot/Robot_N_08.gif',
             'images/robot/Robot_N_09.gif'],
    east  = ['images/robot/Robot_E_01.gif',
             'images/robot/Robot_E_02.gif',
             'images/robot/Robot_E_03.gif',
             'images/robot/Robot_E_04.gif',
             'images/robot/Robot_E_05.gif',
             'images/robot/Robot_E_06.gif',
             'images/robot/Robot_E_07.gif',
             'images/robot/Robot_E_08.gif',
             'images/robot/Robot_E_09.gif'],
    south = ['images/robot/Robot_S_01.gif',
             'images/robot/Robot_S_02.gif',
             'images/robot/Robot_S_03.gif',
             'images/robot/Robot_S_04.gif',
             'images/robot/Robot_S_05.gif',
             'images/robot/Robot_S_06.gif',
             'images/robot/Robot_S_07.gif',
             'images/robot/Robot_S_08.gif',
             'images/robot/Robot_S_09.gif'],
    west  = ['images/robot/Robot_W_01.gif',
             'images/robot/Robot_W_02.gif',
             'images/robot/Robot_W_03.gif',
             'images/robot/Robot_W_04.gif',
             'images/robot/Robot_W_05.gif',
             'images/robot/Robot_W_06.gif',
             'images/robot/Robot_W_07.gif',
             'images/robot/Robot_W_08.gif',
             'images/robot/Robot_W_09.gif'],
    
    free  				= 'images/gray.gif',
    obstacle 			= 'images/gray.gif',
    explored_free		= 'images/d_blue.gif',
    explored_obstacle	= 'images/d_red.gif',
    start               = 'images/yellow.gif',
    end                 = 'images/l_green.gif',
    size                = 1
)

map_detail 	= dict(
    height	= 15,
    width	= 20
)

robot_detail = dict (
    size	= 3,
    delay   = 500
)

sensor_range = dict (
    front_middle    = 10,
    front_left      = 4,
    front_right     = 4,
    left            = 6,
    right           = 6
)

verbose = dict (
    silent      = 0,
    quiet       = 1,
    normal      = 2,
    debug       = 3,
    deepdebug   = 4
)
verboseLv = verbose['normal']

robot_simulation = True
