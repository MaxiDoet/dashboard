import serial

nextion_cmd_end = bytearray([0xff, 0xff, 0xff])

class NextionDisplay():
    def __init__(self, serial_port, baud_rate, debug_enabled=False):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.debug_enabled = debug_enabled
        self.event_handlers = []

        # Init serial dev
        self.serial_dev = serial.Serial(self.serial_port, self.baud_rate, timeout=2)

    def read(self):
        data = self.serial_dev.read_all()

        if self.debug_enabled:
            print("RX <-- NEXTION: %s" % data)

        return data

    def write(self, cmd):
        self.serial_dev.write(bytearray(cmd, encoding="ASCII") + nextion_cmd_end)

        if self.debug_enabled:
            print("CMD --> NEXTION: %s" % cmd)

    def reset(self):
        self.write("rest")

        if self.debug_enabled:
            print("RESET --> NEXTION")

    def add_event_handler(self, type, callback):
        event = {"type": type, "callback": callback}
        self.event_handlers.append(event)

    def handle_events(self):
        data = self.read()

        if len(data) == 0:
            return

        for event_handler in self.event_handlers:
            event_type = event_handler["type"]
            event_callback = event_handler["callback"]

            if (data[0] == event_type):
                if event_type == 0x00:
                    event_callback()
                elif event_type == 0x65:
                    event_callback(data[1], data[2], data[3])