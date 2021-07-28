import threading
from utils import translate
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

class Watchdog(threading.Thread):
    def __init__(self, shutdown_handler):
        super(Watchdog, self).__init__()

        self._setup_loop()
        self._connect_to_bus()

        self._freedesktop_login_interface.connect_to_signal("PrepareForShutdown", shutdown_handler)

    def _connect_to_bus(self):
        self.bus = dbus.SystemBus()
        self._freedesktop_login_object = self.bus.get_object("org.freedesktop.login1", "/org/freedesktop/login1")
        self._freedesktop_login_interface = dbus.Interface(self._freedesktop_login_object, dbus_interface="org.freedesktop.login1.Manager")

    def _setup_loop(self):
        DBusGMainLoop(set_as_default=True)
        self.loop = GLib.MainLoop()

    def run(self):
        self.loop.run()

    def stop(self):
        self.loop.quit()