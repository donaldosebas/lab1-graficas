from renderer import Renderer
from persistence.persistence import Persistence


persistenceRepo = Persistence()

r = Renderer(800, 600)
r.glInit()
r.glClearColor(0, 0, 0)
r.glClear()
r.loads('./models/earth.obj', (800, 600, 0), (0.5, 0.5, 1))


r.glFinish('./lab2.bmp')
