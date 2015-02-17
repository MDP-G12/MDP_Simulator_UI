# ----------------------------------------------------------------------
# class definition of Robot.
#
#   - receive()
#		receive sensor data
#
#   - send()
#		send command to robot (not required for simulator)
# ----------------------------------------------------------------------


class Robot:
    # def __init__(self):

    def receive(self):
        raise NotImplementedError

    def send(self, msg):
        pass

