
def clamp(value, min_value=0, max_value=1):
    return max(min(value, max_value), min_value)

def velocity2speed(velocity):
    speed = 0
    for i in velocity:
        speed += abs(i)
    return speed

def distance(point1, point2):
    """
    Distance on the X/Y plane between two points
    """
    
    return sqrt((point1.x - point2.x)**2 + (point1.y - point2.y))