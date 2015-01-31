import time


class SensorSimulator():
    def __init__(self, event_queue):
        self.command_sequence = ['move', 'move', 'move', 'move',
                                 'move', 'move', 'left', 'move',
                                 'right', 'move', 'move', 'move',
                                 'left', 'move', 'move', 'right',
                                 'move', 'move', 'move', 'move',
                                 'left', 'move', 'move', 'move',
                                 'move', 'move', 'move', 'move',
                                 'move', 'move', 'move', 'move',
                                 'move', 'move', 'move', 'move']
        self.next_command_index = 0
        self.event_queue = event_queue

    def issue_command(self):
        while self.next_command_index < len(self.command_sequence):
            time.sleep(1)
            next_command = self.command_sequence[self.next_command_index]
            self.event_queue.put(next_command)
            self.next_command_index += 1
            print("Command: " + next_command)
