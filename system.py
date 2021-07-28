import platform
import psutil
import utils

def is_linux():
    return ((platform.uname().system == "Linux"))

def is_win():
    return ((platform.uname().system == "Windows"))

def is_raspberrypi():
    try:
        fp = open("/sys/firmware/devicetree/base/model", "r")
        model = fp.read()

        if model.find("Raspberry Pi") != -1:
            return True
        else:
            return False
    except:
        return False