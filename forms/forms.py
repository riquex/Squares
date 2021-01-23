from numpy import absolute
from numpy import array
from numpy import ndarray
from numpy import resize
from numpy import uint8
from numpy import zeros
from numpy import ones
from numpy import square
from numpy import sqrt
from numpy import amax
from numpy import amin
from numpy import sum
from numpy import cos
from numpy import pi
from numpy import sin
from numpy import dot
from numpy import ogrid
from numpy import mgrid
from numpy import where
from numpy import int64
from numpy import arctan2
from numpy import arange
from numpy import repeat
from numpy import arccos
from numpy import repeat
from numpy import flip
from numpy import ndindex
from numpy import dstack
from numpy import meshgrid
from numpy import linalg

import cv2

def join_forms(forms, coords):
    #if (coords < 0).any():
    coords -= amin(coords, axis=(0,))

    shapes = array([f.shape for f in forms], dtype=int64)
    new = zeros((3, amax(shapes[:, 1]+coords[:, 1]), amax(shapes[:, 2]+coords[:, 0])), dtype=uint8)
    
    for xy, f in zip(coords, forms):
        y, x = xy
        xm, ym = x+f.shape[1], y+f.shape[2]
        new[:, x:xm, y:ym] = where(f!=0, f, new[:, x:xm, y:ym])
    return new


def distance(a, b):
    result = linalg.norm(a-b)
    return result

def line(x1, y1, x2, y2, width=1, color=None):
    width = width - 1 if width > 0 else 0

    coords = array(((x1, y1), (x2, y2)), dtype=int64)
    coords -= amin(coords, axis=(0,))
    size = amax(coords, axis=(0,))
    array_ = zeros((3, size[1], size[0]), dtype=uint8)
    layer = zeros((size[1], size[0]), dtype=bool)

    equations = array(((x1, 1), (x2, 1)), dtype=int64)
    solutions = array(((y1), (y2)), dtype=int64)
    a, b = linalg.solve(equations, solutions)

    y, x = mgrid[:size[1], :size[0]]
    layer = where((y-width<=a*x + b)*(a*x + b<=y+width), True, False)
    
    if color==None:
        array_[:] = 255*layer
        return array_

    for e, c in enumerate(color):
        array_[e] = c*layer

def lines(points, width, color=None):
    points -= amin(points, axis=(0,))
    size = amax(points[:, 0]), amax(points[:, 1])
    array_ = zeros((3, size[1], size[0]), dtype=uint8)
    layers = zeros((size[1], size[0]), dtype=uint8)

    points = repeat(points, 2, axis=0)[1:]
    for p in resize(points, (points.shape[0]//2, 2, 2)):
        l = line(*p.flatten(), width=width, color=color)
        array_ = join_forms((array_, l),
                array(
                    ((0, 0),
                    amin(p, axis=(0,)))
                    )
                )

    return array_


def Rectangle(width, height, color):
    array_ = zeros((3, height, width), dtype=uint8)
    
    for e, rgb in enumerate(color):
        array_[e] += rgb
    return array_

def Circle(radius, color):
    array_ = zeros((3, 2*radius, 2*radius), dtype=uint8)
    c = zeros((2*radius, 2*radius), dtype=uint8)
    
    y, x = mgrid[:2*radius, :2*radius]
    c[:] = square(x-radius) + square(y-radius) <= square(radius)
    
    for e, rgb in enumerate(color):
        array_[e][:] = c*rgb
    return array_

def Triangle_from_points(a, b, c, color):
    if a[1] > b[1] and a[1] > c[1]:
        a[1], b[1], c[1] = a[1]-a[1], a[1]-b[1], a[1]-c[1]
    elif b[1] > a[1] and b[1] > c[1]:
        a[1], b[1], c[1] = b[1]-a[1], b[1]-b[1], b[1]-c[1]
    elif c[1] > a[1] and c[1] > b[1]:
        a[1], b[1], c[1] = c[1]-a[1], c[1]-b[1], c[1]-c[1]

    if a[0] > b[0] and a[0] > c[0]:
        a[0], b[0], c[0] = a[0]-a[0], a[0]-b[0], a[0]-c[0]
    elif b[0] > a[0] and b[0] > c[0]:
        a[0], b[0], c[0] = b[0]-a[0], b[0]-b[0], b[0]-c[0]
    elif c[0] > a[0] and c[0] > b[0]:
        a[0], b[0], c[0] = c[0]-a[0], c[0]-b[0], c[0]-c[0]

    width  = amax((a[1], b[1], c[1]))
    height = amax((a[0], b[0], c[0]))

    array_ = zeros((3, width, height), dtype=uint8)
    t = zeros((width, height), dtype=uint8)

    area = lambda x1, y1, x2, y2, x3, y3: absolute(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))/2

    main_area = area(*a, *b, *c)

    y, x = mgrid[:width, :height]
    t[:] = main_area - (area(*a, *b, x, y) + area(*a, *c, x, y) + area(*c, *b, x, y)) == 0

    for e, rgb in enumerate(color):
        array_[e][:] = t*rgb
    array_[:] = flip(array_, axis=(2, 1))
    return array_

def Polygon(points, color):
    if (points < 0).any():
        points -= amin(points, axis=(0,))
    
    points = resize(points, (points.shape[0]//3, 3, 2))

    array_ = zeros([3, 1, 1], dtype=uint8)

    for p in points:
        array_ = join()

def Circular_sector(radius, angle_range, color):
    array_ = zeros((3, 2*radius, 2*radius), dtype=uint8)
    circle = zeros((2*radius, 2*radius), dtype=uint8)
    theta = zeros((2*radius, 2*radius), dtype=uint8)

    x, y = ogrid[:2*radius, :2*radius]
    cx, cy = radius, radius
    tmin, tmax = angle_range

    if tmax < tmin:
        tmax += 2*pi

    circle[:] = square(x-cx)+square(y-cy) <= square(radius)
    theta = arctan2(x-cx, y-cy) - tmin

    theta[:] %= 2*pi

    sector = theta <= (tmax-tmin)
    circle *= sector

    for e, rgb in enumerate(color):
        array_[e][:] = circle*rgb
    array_ = flip(array_, axis=(1))
    return array_

if __name__ == '__main__':
    #a = Rectangle(300, 1000, (255, 10, 0))
    #b = Circle(300, (255, 0, 0))
    '''a1 = array([100, -300])
    b1 = array([0, 300])
    c1 = array([400, 0])
    c = Triangle_from_points(b1, a1, c1, (255, 0, 255))
    d = Circular_sector(500, (pi/2, pi), (255, 0, 0))
    e = join_forms((c, d), array(((-100, -90), (0, 0)))) '''
    #f = line(5,5, 250, 200, 2)
    g = lines(array([[0,0],[500, 100],[0, 400]], dtype=int), 2)
    print(g.shape)

    g = dstack([*g])
    cv2.imshow('img', g)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

