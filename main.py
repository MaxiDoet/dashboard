import sys
import threading

import colorama
from log import *
import utils
from time import sleep
import json

from nextion.display import NextionDisplay
from data import hardware
from data.weather import WeatherApiClient
import system
import utils

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

info("Enabling features")
for feature in config["features"]:
    if not config["features"][feature]["enabled"]:
        continue

    if feature == "spotify":
        info("Spotify Client (client_id=%s)" % config["features"]["spotify"]["client_id"])
        import spotipy
        import spotipy.util as util

        client_id = config["features"]["spotify"]["client_id"]
        client_secret = config["features"]["spotify"]["client_secret"]
        scope = 'user-read-currently-playing user-read-playback-state'
        token = util.prompt_for_user_token("maximilian.doetsch", scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost/callback")
        sp = spotipy.Spotify(auth=token)

        spotify_last_id = None

#weather_client = WeatherApiClient(config["weatherApiKey"], config["weatherLocation"])

# Init display
info("Connecting to nextion display (%s)" % config["serialPort"])
try:
    display = NextionDisplay(config["serialPort"], 115200, debug_enabled=False)
    display_info = display.connect()

    info("Display Info: Model: %s" % display_info["model"])

    info("Connected to nextion display")
except:
    err("Could not connect to display")
    sys.exit()

display.reset()
display.write("dim=0")
display.write("sleep=0")
display.write("ussp=10")
display.write("thup=0")

for i in range(99):
    sleep(0.005)
    display.write("dim=%s" % i)

while True:
    try:
        sleep(config["updateInterval"])
        temp = hardware.get_cpu_temperature()
        display.write('t0.txt="%s"' % (str(temp)))
        
        # Spotify
        spotify_current_playback = sp.current_playback()
        spotify_current_id = spotify_current_playback["item"]["id"]
        if spotify_current_id != spotify_last_id:
            info("Spotify playing: Device: %s%s%s Title: %s%s%s Artist: %s%s%s" % (
                colorama.Fore.GREEN, \
                spotify_current_playback["device"]["name"], \
                colorama.Fore.RESET, \
                colorama.Fore.GREEN, \
                spotify_current_playback["item"]["name"], \
                colorama.Fore.RESET, \
                colorama.Fore.GREEN, \
                spotify_current_playback["item"]["artists"][0]["name"], \
                colorama.Fore.RESET))

        spotify_last_id = spotify_current_id

        display.handle_events()
    except KeyboardInterrupt:
        if watchdog:
            info("Stopping watchdog")
            watchdog.stop()

        info("Sending display to sleep mode")
        display.write("sleep=1")
        sys.exit()