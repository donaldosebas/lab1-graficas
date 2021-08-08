from renderer import *


r = Renderer(1000, 1000)
r.glInit()
r.glClearColor(0, 0, 0)
r.glClear()

r.load('./models/sword.obj', (25, 5), (20, 20))
r.glFinish('sword.bmp')
