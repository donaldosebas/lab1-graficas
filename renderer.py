from persistence.persistence import Persistence

persistenceRepo = Persistence()


class Renderer(object):
    # Constructor
    def __init__(self, width: int = 0, height: int = 0):
        self.initial_width = width
        self.initial_height = height

    # (05 puntos) Deben crear una función glInit() que inicialice cualquier objeto interno que requiera su software renderer
    def glInit(self, curr_color=None, clear_color=None):
        self.curr_color = curr_color or persistenceRepo.color(0.5, 0.5, 0.3)
        self.clear_color = clear_color or persistenceRepo.color(1, 1, 1)
        self.glCreateWindow(self.initial_width, self.initial_height)

    # (05 puntos) Deben crear una función glCreateWindow(width, height) que inicialice su framebuffer con un tamaño (la imagen resultante va a ser de este tamaño
    def glCreateWindow(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0, 0, width, height)

    # (10 puntos)  Deben crear una función glViewPort(x, y, width, height) que defina el área de la imagen sobre la que se va a poder dibujar (hint)
    def glViewport(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

    # (10 puntos) Deben crear una función glClearColor(r, g, b) con la que se pueda cambiar el color con el que funciona glClear(). Los parámetros deben ser números en el rango de 0 a 1.
    def glClearColor(self, r: int = 0, g: int = 0, b: int = 0):
        self.clear_color = persistenceRepo.color(r, g, b)

    # (20 puntos) Deben crear una función glClear() que llene el mapa de bits con un solo color
    def glClear(self):
        self.framebuffer = [[self.clear_color for y in range(
            self.height)] for x in range(self.width)]

    # (15 puntos) Deben crear una función glColor(r, g, b) con la que se pueda cambiar el color con el que funciona glVertex(). Los parámetros deben ser números en el rango de 0 a 1.
    def glColor(self, r: int = 0, g: int = 0, b: int = 0):
        self.curr_color = persistenceRepo.color(r, g, b)

    # (30 puntos) Deben crear una función glVertex(x, y) que pueda cambiar el color de un punto de la pantalla. Las coordenadas x, y son relativas al viewport que definieron con glViewPort.
    def glVertex(self, x: int = 0, y: int = 0, color=None):
        x = int((x + 1) * (self.vpWidth / 2) + self.vpX)
        y = int((y + 1) * (self.vpHeight / 2) + self.vpY)

        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            pass

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.framebuffer[int(x)][int(y)] = color or self.curr_color

    # (05 puntos) Deben crear una función glFinish() que escriba el archivo de imagen
    def glFinish(self, filename: str = 'output.bmp'):
        with open(filename, "wb") as file:
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(persistenceRepo.dword(
                14 + 40 + (self.width * self.height * 3)))
            file.write(persistenceRepo.dword(0))
            file.write(persistenceRepo.dword(14 + 40))
            file.write(persistenceRepo.dword(40))
            file.write(persistenceRepo.dword(self.width))
            file.write(persistenceRepo.dword(self.height))
            file.write(persistenceRepo.word(1))
            file.write(persistenceRepo.word(24))
            file.write(persistenceRepo.dword(0))
            file.write(persistenceRepo.dword(self.width * self.height * 3))
            file.write(persistenceRepo.dword(0))
            file.write(persistenceRepo.dword(0))
            file.write(persistenceRepo.dword(0))
            file.write(persistenceRepo.dword(0))

            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.framebuffer[x][y])


r = Renderer(1024, 768)
r.glInit()
r.glClearColor(0.3, 0.3, 0.3)
r.glClear()
r.glVertex(0, 0)
r.glFinish()
