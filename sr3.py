from renderer import *


r = Renderer(1000, 1000)
r.glInit()
r.glClearColor(0.3, 0.3, 0.3)
r.glClear()

r.load('./models/test-plane.obj', (25, 5), (20, 20))
r.glFinish('test-plane.bmp')
