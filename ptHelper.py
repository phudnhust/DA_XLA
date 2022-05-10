import math

def mid2Point(pt1, pt2):
    mp_x = int(( pt1[0] + pt2[0] ) / 2)
    mp_y = int(( pt1[1] + pt2[1] ) / 2)
    return (mp_x, mp_y)

def dist2Point(pt1, pt2):
    (x1, y1) = pt1
    (x2, y2) = pt2
    return int(math.sqrt( (x2-x1)**2 + (y2-y1)**2 ))