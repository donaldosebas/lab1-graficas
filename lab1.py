from renderer import *

r = Renderer(1000, 1000)
r.glInit()
r.glClearColor(0.3, 0.3, 0.3)
r.glClear()
# r.glLine(-1, -1, 1, 1)

# r.load('./models/face.obj', (25, 5), (15, 15))

a = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330),
     (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]

for i in range(len(a) - 1):
    r.glLine(a[i][0], a[i][1], a[i+1][0], a[i+1][1])
    if i == len(a) - 2:
        last_item = len(a) - 2
        r.glLine(a[last_item+1][0], a[last_item+1][1], a[0][0], a[0][1])

# r.glLine(0, 0, -1, -1)
# r.line(165, 380, 185, 360)
# r.line(180, 330, 207, 345)
# r.line(180, 330, 207, 345)
r.glFinish()
