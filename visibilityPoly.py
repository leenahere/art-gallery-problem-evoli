import math
import matplotlib.path as mplPath
import random
import numpy as np
from collections import namedtuple
from PIL import Image, ImageDraw

Pt = namedtuple('Pt', 'x, y')
Edge = namedtuple('Edge', 'a, b')
Ray = namedtuple('Ray', 'a, b')
Intersection = namedtuple('Intersection', 'p, param')

m = Pt(x=300, y=300)

points = [Pt(277, 241), Pt(286, 260), Pt(293, 184), Pt(320, 249), Pt(341, 225),
          Pt(409, 238), Pt(375, 279), Pt(388, 290), Pt(388, 362), Pt(316, 359),
          Pt(285, 397), Pt(259, 370), Pt(211, 314), Pt(162, 270), Pt(245, 255)]

polygon = [
    Edge(a=Pt(x=277, y=241), b=Pt(x=286, y=260)),
    Edge(a=Pt(x=286, y=260), b=Pt(x=293, y=184)),
    Edge(a=Pt(x=293, y=184), b=Pt(x=320, y=249)),
    Edge(a=Pt(x=320, y=249), b=Pt(x=341, y=225)),
    Edge(a=Pt(x=341, y=225), b=Pt(x=409, y=238)),
    Edge(a=Pt(x=409, y=238), b=Pt(x=375, y=279)),
    Edge(a=Pt(x=375, y=279), b=Pt(x=388, y=290)),
    Edge(a=Pt(x=388, y=290), b=Pt(x=388, y=362)),
    Edge(a=Pt(x=388, y=362), b=Pt(x=316, y=359)),
    Edge(a=Pt(x=316, y=359), b=Pt(x=285, y=397)),
    Edge(a=Pt(x=285, y=397), b=Pt(x=259, y=370)),
    Edge(a=Pt(x=259, y=370), b=Pt(x=211, y=314)),
    Edge(a=Pt(x=211, y=314), b=Pt(x=162, y=270)),
    Edge(a=Pt(x=162, y=270), b=Pt(x=245, y=255)),
    Edge(a=Pt(x=245, y=255), b=Pt(x=277, y=241))]

#polyPath = mplPath.Path(np.array(polygon))

polygon2 = [
    Edge(a=Pt(x=162, y=270), b=Pt(x=245, y=255)),
    Edge(a=Pt(x=211, y=314), b=Pt(x=162, y=270)),
    Edge(a=Pt(x=259, y=370), b=Pt(x=211, y=314)),
    Edge(a=Pt(x=285, y=397), b=Pt(x=259, y=370)),
    Edge(a=Pt(x=316, y=359), b=Pt(x=285, y=397)),
    Edge(a=Pt(x=388, y=362), b=Pt(x=316, y=359)),
    Edge(a=Pt(x=388, y=290), b=Pt(x=388, y=362)),
    Edge(a=Pt(x=375, y=279), b=Pt(x=388, y=290)),
    Edge(a=Pt(x=409, y=238), b=Pt(x=375, y=279)),
    Edge(a=Pt(x=341, y=225), b=Pt(x=409, y=238)),
    Edge(a=Pt(x=320, y=249), b=Pt(x=341, y=225)),
    Edge(a=Pt(x=293, y=184), b=Pt(x=320, y=249)),
    Edge(a=Pt(x=286, y=260), b=Pt(x=293, y=184)),
    Edge(a=Pt(x=277, y=241), b=Pt(x=286, y=260))]

guards = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# optimale Loesung
guards2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

def adjustVertices():
    increasedX = False
    increasedY = False
    decreasedX = False
    decreasedY = False
    adjustedPoints = []
    for point in points:
        if point.x < m.x:
            point = Pt(point.x+2, point.y)
            increasedX = not increasedX
        if point.y < m.y:
            point = Pt(point.x, point.y+2)
            increasedY = True
        if point.x > m.x:
            point = Pt(point.x-2, point.y)
            decreasedX = True
        if point.y > m.y:
            point = Pt(point.x, point.y-2)
            decreasedY = True

        if not point_inside_polygon(point.x, point.y, points):
            print("point not in poly %i %i", point.x, point.y)

        adjustedPoints.append(point)

    return adjustedPoints

def getGuardsFromIndividual(polyPoints, guardIndividual):
    vertexGuards = []
    i = 0
    for point in polyPoints:
        guard = guardIndividual[i]
        if guard is 1:
            vertexGuards.append(point)
        i += 1

    return vertexGuards

def getIntersection(ray, segment):
    # RAY in parametric: Point + Delta * T1
    r_px = float(ray.a.x)
    r_py = float(ray.a.y)
    r_dx = float(ray.b.x - ray.a.x)
    r_dy = float(ray.b.y - ray.a.y)

    # SEGMENT in parametric: Point + Delta * T2
    s_px = float(segment.a.x)
    s_py = float(segment.a.y)
    s_dx = float(segment.b.x - segment.a.x)
    s_dy = float(segment.b.y - segment.a.y)

    # Are they parallel? If so, no intersect
    r_mag = math.sqrt(r_dx * r_dx + r_dy * r_dy)
    s_mag = math.sqrt(s_dx * s_dx + s_dy * s_dy)
    if r_dx / r_mag == s_dx / s_mag and r_dy / r_mag == s_dy / s_mag:
        return None

    # SOLVE FOR T1 & T2
    # r_px + r_dx * T1 = s_px + s_dx * T2 & & r_py + r_dy * T1 = s_py + s_dy * T2
    # == > T1 = (s_px + s_dx * T2 - r_px) / r_dx = (
    # s_py + s_dy * T2 - r_py) / r_dy
    # == > s_px * r_dy + s_dx * T2 * r_dy - r_px * r_dy = s_py * r_dx + s_dy * T2 * r_dx - r_py * r_dx
    # == > T2 = ( r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / (s_dx * r_dy - s_dy * r_dx)
    T2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / (s_dx * r_dy - s_dy * r_dx)
    T1 = (s_px + s_dx * T2 - r_px) / r_dx

    # Must be within parametic whatevers for RAY / SEGMENT
    if T1 < 0:
        return None

    if T2 < 0 or T2 > 1:
        return None

    # Return the POINT OF INTERSECTION
    return Intersection(Pt(x=r_px+r_dx*T1, y=r_py+r_dy*T1), T1)


def findIntersections():
    adjustedPoints = adjustVertices()
    proposedGuards = getGuardsFromIndividual(adjustedPoints, guards)
    #guard = proposedGuards[0]

    for guard in proposedGuards:
        intersects = []
        for angle in np.arange(0, math.pi * 2, (math.pi * 2) / 50):
            dx = math.cos(angle)
            dy = math.sin(angle)

            ray = Ray(a=guard, b=Pt(x=guard.x + dx, y=guard.y + dy))

            closestIntersect = 0

            for border in polygon:
                intersect = getIntersection(ray, border)

                if not intersect:
                    continue

                if (closestIntersect is 0) or (intersect.param < closestIntersect.param):
                    closestIntersect = intersect

            if not closestIntersect == 0:
                intersects.append(closestIntersect)

        draw(intersects, guard)


def draw(intersects, guard):
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (211, 67, 27)
    im = Image.new('RGB', (500, 500), white)
    imPxAccess = im.load()
    draw = ImageDraw.Draw(im)
    tupVerts = list(map(tuple, points))

    draw.line(tupVerts + [tupVerts[0]], width=1, fill=black)

    r = lambda: random.randint(0, 255)
    color = '#%02X%02X%02X' % (r(), r(), r())
    for intersect in intersects:
        rayLine = [(intersect.p.x, intersect.p.y), guard]
        draw.line(rayLine, width=1, fill=color)

    draw.point(guard, fill=red)

    im.show()

def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

if __name__ == "__main__":
    findIntersections()
