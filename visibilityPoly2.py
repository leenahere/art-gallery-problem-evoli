import random
from collections import namedtuple

import math
from PIL import ImageDraw, Image

Pt = namedtuple('Pt', 'x, y')
Edge = namedtuple('Edge', 'a, b')
Ray = namedtuple('Ray', 'a, b')
Intersection = namedtuple('Intersection', 'p, param')


class Polygon(object):
    def __init__(self, vertices, edges=None, clockwise=False):
        if not clockwise:
            self.vertices = vertices
        else:
            self.vertices = []
            for vertex in reversed(vertices):
                self.vertices.append(vertex)
        if edges:
            self.edges = edges
        else:
            self.edges = []
            for i in range(len(self.vertices) - 1):
                self.edges.append(Edge(a=self.vertices[i], b=self.vertices[i + 1]))
            self.edges.append(Edge(a=self.vertices[len(self.vertices) - 1], b=self.vertices[0]))

    def get_adjacent_edges(self, vertex):
        incoming = None
        outgoing = None
        for edge in self.edges:
            if vertex == edge.b:
                incoming = edge
            elif vertex == edge.a:
                outgoing = edge
        return incoming, outgoing


def get_angle(line):
    # Returns the angle of a straight line in the range 0..2pi
    dx = float(line.b.x - line.a.x)
    dy = - float(line.b.y - line.a.y)
    if dx == 0:
        if dy > 0:
            return 0.5 * math.pi
        elif dy < 0:
            return 1.5 * math.pi
        else:
            return None
    else:
        angle = math.atan(dy / dx)
        if dx < 0:
            angle += math.pi
        elif dy < 0:
            angle += 2.0 * math.pi
        return angle


def get_param(intersection):
    return intersection.param


def get_intersection(ray, segment):
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
    if s_dx * r_dy == s_dy * r_dx:
        return None

    # SOLVE FOR T1 & T2
    T1 = -1
    T2 = -1
    # r_px + r_dx * T1 = s_px + s_dx * T2  &&  r_py + r_dy * T1 = s_py + s_dy * T2
    if r_dx == 0:
        T2 = (r_px - s_px) / s_dx
        T1 = (s_py + s_dy * T2 - r_py) / r_dy
    else:
        # == > T1 = (s_px + s_dx * T2 - r_px) / r_dx = (s_py + s_dy * T2 - r_py) / r_dy
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


def shoot_rays(polygon, guard):
    incoming, outgoing = polygon.get_adjacent_edges(guard)
    incoming_reverse_angle = get_angle(Edge(a=incoming.b, b=incoming.a))
    outgoing_angle = get_angle(outgoing)
    contains_zero = incoming_reverse_angle < outgoing_angle

    rays = []
    for vertex in polygon.vertices:
        if vertex == guard:
            continue
        ray = Ray(a=guard, b=vertex)
        ray_angle = get_angle(ray)
        if not contains_zero and (ray_angle < outgoing_angle or ray_angle > incoming_reverse_angle):
            continue
        elif contains_zero and (outgoing_angle > ray_angle > incoming_reverse_angle):
            continue
        rays.append(ray)
    if not contains_zero:
        rays.sort(key=get_angle)
    else:
        big_rays, small_rays = [], []
        for ray in rays:
            ray_angle = get_angle(ray)
            big_rays.append(ray) if ray_angle > incoming_reverse_angle else small_rays.append(ray)
        big_rays.sort(key=get_angle)
        small_rays.sort(key=get_angle)
        for ray in small_rays:
            big_rays.append(ray)
        rays = big_rays
    return rays


def get_visibility_polygon_vertices(polygon, guard):
    rays = shoot_rays(polygon, guard)
    visibility_polygon_vertices = [guard]
    for ray in rays:
        intersections = []
        for edge in polygon.edges:
            if ray.a == edge.a and ray.b == edge.b:
                continue
            intersection = get_intersection(ray, edge)
            if not intersection or intersection.param == 0 or intersection in intersections:
                continue
            intersections.append(intersection)
        intersections.sort(key=get_param)

        second_intersection = False
        second_intersection_reverse_order = False
        if intersections[0].param == 1 and len(intersections) > 1:
            incoming, outgoing = polygon.get_adjacent_edges(intersections[0].p)
            incoming_reverse_angle = get_angle(Edge(a=incoming.b, b=incoming.a))
            outgoing_angle = get_angle(outgoing)
            incoming_angle = get_angle(incoming)
            outgoing_reverse_angle = get_angle(Edge(a=outgoing.b, b=outgoing.a))
            contains_zero = incoming_reverse_angle < outgoing_angle
            ray_angle = get_angle(ray)

            if not contains_zero:
                if outgoing_angle < math.pi and incoming_angle < math.pi:
                    if outgoing_angle <= ray_angle <= incoming_angle:
                        second_intersection = True
                    elif outgoing_reverse_angle <= ray_angle <= incoming_reverse_angle:
                        second_intersection_reverse_order = True
            else:
                if outgoing_angle < math.pi:
                    if outgoing_angle <= ray_angle <= incoming_angle:
                        second_intersection = True
                    elif outgoing_reverse_angle <= ray_angle or ray_angle <= incoming_reverse_angle:
                        second_intersection_reverse_order = True
                elif incoming_angle < math.pi:
                    if outgoing_angle <= ray_angle or ray_angle <= incoming_angle:
                        second_intersection = True
                    elif outgoing_reverse_angle <= ray_angle <= incoming_reverse_angle:
                        second_intersection_reverse_order = True
                else:
                    if outgoing_angle <= ray_angle <= incoming_angle:
                        second_intersection = True
                    elif outgoing_reverse_angle <= ray_angle <= incoming_reverse_angle:
                        second_intersection_reverse_order = True
        if second_intersection:
            visibility_polygon_vertices.append(intersections[0].p)
            visibility_polygon_vertices.append(intersections[1].p)
        elif second_intersection_reverse_order:
            visibility_polygon_vertices.append(intersections[1].p)
            visibility_polygon_vertices.append(intersections[0].p)
        else:
            visibility_polygon_vertices.append(intersections[0].p)
    return visibility_polygon_vertices


def valid_coverage(polygon, guards):
    uncovered_vertices = set(polygon.vertices)
    for i, guard in enumerate(guards):
        if guard == 1:
            uncovered_vertices -= set(get_visibility_polygon_vertices(polygon, guard=polygon.vertices[i]))
    return len(uncovered_vertices) == 0


def valid_coverage_draw(polygon, guards):
    uncovered_vertices = set(polygon.vertices)
    visibility_polygons = []
    for i, guard in enumerate(guards):
        if guard == 1:
            visibility_polygon = get_visibility_polygon_vertices(polygon, guard=polygon.vertices[i])
            visibility_polygons.append(visibility_polygon)
            uncovered_vertices -= set(visibility_polygon)
    draw(polygon, visibility_polygons=visibility_polygons)
    return len(uncovered_vertices) == 0


def draw(polygon, rays=None, visibility_polygon_vertices=None, visibility_polygons=None):
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (211, 67, 27)
    blue = (50, 50, 240)
    green = (50, 240, 50)
    im = Image.new('RGB', (500, 500), white)
    imPxAccess = im.load()
    draw = ImageDraw.Draw(im)
    tup_verts = list(map(tuple, polygon.vertices))
    draw.line(tup_verts + [tup_verts[0]], width=1, fill=black)

    if rays:
        for ray in rays:
            draw.line([ray.a, ray.b], width=1, fill=red)
        draw.line([rays[0].a, rays[0].b], width=1, fill=blue)

    if visibility_polygon_vertices:
        tup_verts_intersec = list(map(tuple, visibility_polygon_vertices))
        draw.line(tup_verts_intersec + [tup_verts_intersec[0]], width=1, fill=green)

    if visibility_polygons:
        for vertices in visibility_polygons:
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())
            tup_verts_intersec = list(map(tuple, vertices))
            draw.polygon(tup_verts_intersec + [tup_verts_intersec[0]], fill=color)

    im.show()
