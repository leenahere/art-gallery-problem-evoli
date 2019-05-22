from visibilityPoly2 import *
from initialPopulation import generateInitialPopulation
from initialPopulation import *


poly = Polygon(
    [Pt(277, 241), Pt(286, 260), Pt(293, 184), Pt(320, 249), Pt(341, 225),
     Pt(409, 238), Pt(375, 279), Pt(388, 290), Pt(388, 362), Pt(316, 359),
     Pt(285, 397), Pt(259, 370), Pt(211, 314), Pt(162, 270), Pt(245, 255)],
    clockwise=True
)

# poly2 = Polygon([Pt(495, 652), Pt(387, 611), Pt(384, 610), Pt(315, 607), Pt(253, 515), Pt(208, 512), Pt(218, 471),
#                 Pt(131, 456), Pt(352, 394), Pt(325, 373), Pt(267, 241), Pt(321, 286), Pt(350, 257), Pt(366, 147),
#                 Pt(394, 355), Pt(417, 212), Pt(437, 129), Pt(514, 212), Pt(559, 300), Pt(521, 325), Pt(591, 288),
#                 Pt(583, 360), Pt(612, 382), Pt(570, 391), Pt(520, 420), Pt(602, 448), Pt(507, 492), Pt(456, 451),
#                 Pt(652, 628), Pt(499, 502)],
#                clockwise=True)

points = [Pt(495, 652), Pt(387, 611), Pt(384, 610), Pt(315, 607), Pt(253, 515), Pt(208, 512), Pt(218, 471),
                Pt(131, 456), Pt(352, 394), Pt(325, 373), Pt(267, 241), Pt(321, 286), Pt(350, 257), Pt(366, 147),
                Pt(394, 355), Pt(417, 212), Pt(437, 129), Pt(514, 212), Pt(559, 300), Pt(521, 325), Pt(591, 288),
                Pt(583, 360), Pt(612, 382), Pt(570, 391), Pt(520, 420), Pt(602, 448), Pt(507, 492), Pt(456, 451),
                Pt(652, 628), Pt(499, 502)]

def convertPolyPoints(points):
    poly = []
    for point in points:
        formattedPoint = Pt(point.x,point.y)
        poly.append(formattedPoint)

    print(poly)
    return Polygon(poly, clockwise=True)

valid_coverages = generateInitialPopulation(convertPolyPoints(points))
# valid_coverages = [
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
# ]

def test_polygon_single_guard(polygon):
    for guard in polygon.vertices:
        print("TEST RUN")
        rays = shoot_rays(polygon, guard)
        visibility_polygon_vertices = get_visibility_polygon_vertices(polygon, guard)
        draw(polygon, rays=rays, visibility_polygon_vertices=visibility_polygon_vertices)


def test():
    for coverage in valid_coverages:
        print(valid_coverage_draw(convertPolyPoints(points), coverage))


if __name__ == '__main__':
    poly2 = convertPolyPoints(points)
    rays = shoot_rays(poly2, poly2.vertices[0])
    draw(poly2, rays, get_visibility_polygon_vertices(poly2, poly2.vertices[0]))
    test()

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (211, 67, 27)
    im = Image.new('RGB', (1200, 1200), white)
    imPxAccess = im.load()
    draw = ImageDraw.Draw(im)
    tupVerts = list(map(tuple, points))
    draw.line(tupVerts + [tupVerts[0]], width=1, fill=black)
    im.show()
