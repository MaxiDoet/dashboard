import sys
import threading

import colorama
from log import *
import utils
from time import sleep
import json

import nextion
from data import hardware
from data.weather import WeatherApiClient
import system
import utils
import effects

# If we're on windows platform we need to init colorama
if system.is_win():
    colorama.init()

def shutdown_handler():
    info("Received shutdown event")

info("Detecting platform")

if system.is_linux():
    if system.is_raspberrypi():
        info("Platform: Raspberry Pi (Linux)")
    else:
        info("Platform: Linux")

    from platforms.linux import events

    # Setup watchdog
    info("Setting up watchdog for dbus events")
    watchdog = events.Watchdog(shutdown_handler)
    watchdog.start()

if system.is_win():
    info("Platform: Windows")

# Read config
config = []
try:
    fp = open("config.json", "r")
    config = json.load(fp)
    info("Loaded config")
except:
    err("Unable to load config")
    exit(0)

def detect_sensors():
    info("Detecting sensors")

    if system.is_raspberrypi():
        info("Found raspberry pi soc sensor")

detect_sensors()

#weather_client = WeatherApiClient(config["weatherApiKey"], config["weatherLocation"])

# Init display
info("Connecting to nextion display (%s)" % config["serialPort"])
try:
    display = nextion.NextionDisplay(config["serialPort"], 115200)
    info("Connected to nextion display")
except:
    error("Could not connect to display")
    sys.exit()

display.reset()
display.write("sleep=0")

while True:
    try:
        sleep(config["updateInterval"])
        temp = hardware.get_cpu_temperature()
        info("CPU Temp: %s" % temp)
        display.write('t0.txt="%s"' % (str(temp)))
        display.handle_events()
    except KeyboardInterrupt:
        if watchdog:
            info("Stopping watchdog")
            watchdog.stop()

        info("Sending display to sleep mode")
        display.write("sleep=1")
        sys.exit()