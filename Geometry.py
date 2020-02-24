"""Utility functions for performing calculations on vertices."""
# Citation for intersecting line segments:
# https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
import math


# Return the geometric distance between two x, y coordinates
def distance(v2, v1):
    return math.sqrt(pow(v2[0] - v1[0], 2) + pow(v2[1] - v1[1], 2))


# Determine if q lies on the line segment p -> r
def on_segment(p, q, r):
    if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0]))) and (
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
        return True
    else:
        return False


# Determine the orientation between 3 coordinate pairs
def orientation(p, q, r):
    value = (float(q[1] - p[1]) * (r[0] - q[0])) - (
            float(q[0] - p[0]) * (r[1] - q[1]))
    if value > 0:
        # Clockwise points
        return 1
    elif value < 0:
        # Counterclockwise points
        return 2
    else:
        # Collinear points
        return 0


# Determines if two line segments intersect
def has_intersection(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 == 0) and on_segment(p1, p2, q1):
        return True
    elif (o2 == 0) and on_segment(p1, q2, q1):
        return True
    elif (o3 == 0) and on_segment(p2, p1, q2):
        return True
    elif (o4 == 0) and on_segment(p2, q1, q2):
        return True
    else:
        return False
