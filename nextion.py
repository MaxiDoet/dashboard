import serial

nextion_cmd_end = bytearray([0xff, 0xff, 0xff])

class NextionDisplay():
    def __init__(self, serial_port, baud_rate, debug_enabled=True):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.debug_enabled = debug_enabled

        # Init serial dev
        self.serial_dev = serial.Serial(self.serial_port, self.baud_rate, timeout=2)

    def read(self):
        data = self.serial_dev.read_all()

        if self.debug_enabled:
            print("RX <-- NEXTION: %s" % data)

        return data

    def write(self, cmd):
        self.serial_dev.write(bytearray(cmd, encoding="ASCII")) + nextion_cmd_end

        if self.debug_enabled:
            print("CMD --> NEXTION: %s" % cmd)

    def reset(self):
        self.write("rest")

        if self.debug_enabled:
            print("RESET --> NEXTION")