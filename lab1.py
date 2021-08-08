from renderer import *

r = Renderer(1000, 1000)
r.glInit()
r.glClearColor(0, 0, 0)
r.glClear()


def render_image_border(a):
    for i in range(len(a) - 1):
        r.glLine(a[i][0], a[i][1], a[i+1][0], a[i+1][1], True)
        if i == len(a) - 2:
            last_item = len(a) - 2
            r.glLine(a[last_item+1][0], a[last_item+1]
                     [1], a[0][0], a[0][1], True)


def paint_inner(points, centerx, centery):
    for i in points:
        r.glLine(int(centerx), int(centery),
                 points[i][0], points[i][1])


def find_center():
    max_x_val = max(r.pointsVisited.values(), key=lambda sub: sub[0])
    max_y_val = max(r.pointsVisited.values(), key=lambda sub: sub[1])
    min_x_val = min(r.pointsVisited.values(), key=lambda sub: sub[0])
    min_y_val = min(r.pointsVisited.values(), key=lambda sub: sub[1])
    centerx = (max_x_val[0] + min_x_val[0]) / 2
    centery = (max_y_val[1] + min_y_val[1]) / 2
    return centerx, centery


# FIRST IMAGE BORDER
polygon_1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330),
             (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
render_image_border(polygon_1)
# FIND SQUEARE THAT CONTAINS THE IMAGE IN ORDER TO FIND ITS CENTER
centerx, centery = find_center()
# PAINT FIRST IMAGE
paint_inner(r.pointsVisited, centerx, centery)
# CLEAR POINTS
r.clear_point()
# SECOND IMAGE
polygon_2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
render_image_border(polygon_2)
# FIND SQUEARE THAT CONTAINS THE IMAGE IN ORDER TO FIND ITS CENTER
centerx, centery = find_center()
# PAINT SECOND IMAGE
paint_inner(r.pointsVisited, centerx, centery)
# CLEAR POINTS
r.clear_point()
# THIRD IMAGE
polygon_3 = [(377, 249), (411, 197), (436, 249)]
render_image_border(polygon_3)
# FIND SQUEARE THAT CONTAINS THE IMAGE IN ORDER TO FIND ITS CENTER
centerx, centery = find_center()
# PAINT THIRD IMAGE
paint_inner(r.pointsVisited, centerx, centery)
# CLEAR POINTS
r.clear_point()
# FOURTH IMAGE
polygon_4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
             (750, 145), (761, 179), (672, 192), (659,
                                                  214), (615, 214), (632, 230), (580, 230),
             (597, 215), (552, 214), (517, 144), (466, 180)]
render_image_border(polygon_4)
# FIND SQUEARE THAT CONTAINS THE IMAGE IN ORDER TO FIND ITS CENTER
centerx, centery = find_center()
# PAINT FOURTH IMAGE
paint_inner(r.pointsVisited, centerx, centery)
# CLEAR POINTS
r.clear_point()
# FIFTH IMAGE
r.glColor(0, 0, 0)
polygon_5 = [(682, 175), (708, 120), (735, 148), (739, 170)]
render_image_border(polygon_5)
# FIND SQUEARE THAT CONTAINS THE IMAGE IN ORDER TO FIND ITS CENTER
centerx, centery = find_center()
# PAINT FIFTH IMAGE
paint_inner(r.pointsVisited, centerx, centery)
r.glFinish('lab1.bmp')
