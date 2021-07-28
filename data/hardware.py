import psutil
import system

from platforms import rpi

def get_memory():
    return psutil.virtual_memory().total

def get_used_memory():
    return psutil.virtual_memory().used

def get_cpu_temperature():
    if system.is_raspberrypi():
        return rpi.get_rpi_soc_temperature()

def get_cpu_frequency():
    if system.is_raspberrypi():
        return rpi.get_rpi_soc_frequency()