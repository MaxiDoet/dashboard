import math

def get_rpi_soc_temperature():
    try:
        fp = open("/sys/class/thermal/thermal_zone0/temp", "r")
        temp = int(fp.read()) / 1000
        return math.ceil(temp)
    except:
        return 0

def get_rpi_soc_frequency():
    try:
        fp = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r")
        freq = int(fp.read()) / 1000
        return math.ceil(freq)
    except:
        return 0