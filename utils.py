import math

"""
Basic utility functions
"""

def clamp(value, min_value=0, max_value=1):
    return max(min(value, max_value), min_value)

def velocity2speed(velocity):
    """
    Turns a vector into a scalar. Is never negative.
    """
    speed = 0
    for i in velocity:
        speed += abs(i)
    return speed

def distance(point1, point2):
    """
    Distance on the X/Y plane between two points
    """
    
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y))

def map_range(value, from_min=0, from_max=1, to_min=0, to_max=1):
    """
    Scale value from
    Thanks to this SO post: http://stackoverflow.com/a/5295202/2730823
    """
    
    return ((to_max-to_min)*(value - from_min) / (from_max - from_min)) + to_min

def lerp(value1, value2, fac):
    """
    linear interpolation
    """
    
    return value1 * (1-fac) + value2 * fac