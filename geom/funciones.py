from math import sqrt, pow, hypot, atan2, cos, sin, degrees, radians

from geom.geomcom import Punto2D
import sys


def dist(P, Q):
    """A math Point function to calculate the distance between 2 points."""
    d = sqrt(pow(P.x - Q.x, 2) + pow(P.y - Q.y, 2))
    return d


def mid_point(P, Q):
    """A math Point function to calculate the mid point between 2 points."""
    R = (1. / 2.) * (P + Q)
    return R


def translate2D(P, tx, ty):
    """A math Point function to calculate a  tx, ty translation of a point
    If you put translate((1,2), -2, 3), the function calculate a point with -2
    x-coordinate and +3 y-coordinate, i.e., the point is (-1,5). The function
    calculates for a 2D Point."""
    R = Punto2D()
    R.x = P.x + tx
    R.y = P.y + ty
    return R


def translate3D(P, tx, ty):
    """A math Point function to calculate a  tx, ty, tz translation of a point
    If you put translate((1,2), -2, 3, 4), the function calculate a point with
    -2 x-coordinate, +3 y-coordinate and +4 z-coordinate, i.e., the point is
    (-1,5). The function calculates for a 3D Point."""
    R = Punto2D()
    R.x = P.x + tx
    R.y = P.y + ty
    return R


def incenter(A, B, C):
    """A math Point function to calculate the Incenter Point in a triangle."""
    I = Punto2D()
    a = dist(B, C)
    b = dist(A, C)
    c = dist(A, B)
    sumd=a + b + c
    I = (a / sumd) * A + (b / sumd) * B + (c / sumd) * C
    return I


def rect2pol(P):
    """A math point function to calculate the polar coordinates of a point in
    rectangular points."""
    R = Punto2D()
    R.x = hypot(P.x, P.y)
    R.y = atan2(P.y, P.x)
    return (R)


def rect2poldeg(P):
    """A math point function to calculate the polar coordinates of a point in
    rectangular points. In sexagesimal degrees."""
    R = Punto2D()
    R.x = hypot(P.x, P.y)
    R.y = degrees(atan2(P.y, P.x))
    return (R)


def pol2rect(P):
    """A math point function to calculate the rectangular coordinates of a
    point in polar coordinates."""
    R = Punto2D()
    if P.x <= 0:
        raise ValueError('The radius must be > 0')
    R.x = P.x * cos(P.y)
    R.y = P.x * sin(P.y)
    return (R)


def pol2rectdeg(P):
    """A math point function to calculate the rectangular coordinates of a
    point in polar coordinates. In sexagesimal degrees."""
    R = Punto2D()
    if P.x <= 0:
        raise ValueError('The radius must be > 0')
    R.x = P.x * cos(radians(P.y))
    R.y = P.x * sin(radians(P.y))
    return (R)


def rect2cyl(P):
    """A math point function to calculate the cilindrical coordinates of a
    point in rectangular coordinates."""
    R = Punto2D()
    R.x = hypot(P.x, P.y)
    R.y = atan2(P.y, P.x)
    return (R)


def rect2cyldeg(P):
    """A math point function to calculate the cilindrical coordinates of a
    point in rectangular coordinates. In sexagesimal degrees."""
    R = Punto2D()
    R.x = hypot(P.x, P.y)
    R.y = degrees(atan2(P.y, P.x))
    return (R)


def cyl2rect(P):
    """A math point function to calculate the rectangular coordinates of a
    point in cilindrical coordinates."""
    R = Punto2D()
    if P.x <= 0:
        raise ValueError('The radius must be > 0')
    R.x = P.x * cos(P.y)
    R.y = P.x * sin(P.y)
    return (R)


def cyl2rectdeg(P):
    """A math point function to calculate the rectangular coordinates of a
    point in cilindrical coordinates. In sexagesimal degrees."""
    R = Punto2D()
    if P.x <= 0:
        raise ValueError('The radius must be > 0')
    R.x = P.x * cos(radians(P.y))
    R.y = P.x * sin(radians(P.y))
    return (R)


def input_point(P):
    """A method when the user of a terminal can input a point with 2 or 3
    coordinates. The user must write (1,2,3) or (1,2), for instance."""
    print(('Enter a point (x,y):'))
    point = sys.stdin.readline()
    point = point.replace('(', '')
    point = point.replace(')', '')
    l1 = point.rsplit(',')
    P.x = float(l1[0])
    P.y = float(l1[1])
    #if len(l1) == 3:
    #    P.z = float(l1[2])
    l1 = []


def is_to_the_left_of_line(X, A, B):
    C = B - A
    P = X - A

    if C.x * P.y > C.y * P.x:
        return True
    else:
        return False

