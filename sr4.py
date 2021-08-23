from renderer import Renderer

r = Renderer(800, 600)
r.glInit()
r.glClearColor(0, 0, 0)
r.glClear()
r.load('./models/face.obj', (25, 5, 0), (15, 15, 15))
r.glFinish('./sr4.bmp')
