import math

from data import weather

def convert_size(unit, size):
    if unit == 'mb':
        return math.ceil(size / (1024 * 1024))
    elif unit == 'gb':
        return round(convert_size('mb', size) / 1024, 2)
    elif unit == 'tb':
        return round(convert_size('gb', size) / 1024, 2)

def format_size(size):
    if convert_size('mb', size) < 1000:
        return "%s MB" % str(convert_size('mb', size))
    elif convert_size('mb', size) >= 1000 and convert_size('gb', size) < 1000:
        return "%s GB" % str(convert_size('gb', size))
    elif convert_size('gb', size) >= 1000:
        return "%s TB" % str(convert_size('tb', size))

def format_frequency(frequency):
    if frequency / 1000 < 1:
        return "%s Mhz" % str(frequency)
    else:
        return "%s Ghz" % str(frequency / 1000)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)