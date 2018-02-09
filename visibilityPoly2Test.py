from visibilityPoly2 import *


poly = Polygon(
    [Pt(277, 241), Pt(286, 260), Pt(293, 184), Pt(320, 249), Pt(341, 225),
     Pt(409, 238), Pt(375, 279), Pt(388, 290), Pt(388, 362), Pt(316, 359),
     Pt(285, 397), Pt(259, 370), Pt(211, 314), Pt(162, 270), Pt(245, 255)],
    clockwise=True
)


valid_coverages = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
]


def test_polygon_single_guard(polygon):
    for guard in polygon.vertices:
        print("TEST RUN")
        rays = shoot_rays(polygon, guard)
        visibility_polygon_vertices = get_visibility_polygon_vertices(polygon, guard)
        draw(polygon, rays=rays, visibility_polygon_vertices=visibility_polygon_vertices)


def test():
    for coverage in valid_coverages:
        print(valid_coverage_draw(poly, coverage))


if __name__ == '__main__':
    rays = shoot_rays(poly, poly.vertices[0])
    draw(poly, rays, get_visibility_polygon_vertices(poly, poly.vertices[0]))
    test()