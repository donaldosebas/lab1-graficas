from persistence.persistence import Persistence
from obj import Obj, Texture
import random
import math

persistenceRepo = Persistence()


class Renderer(object):
    # Constructor
    def __init__(self, width: int = 0, height: int = 0):
        self.initial_width = width
        self.initial_height = height
        self.pointsVisited = {}
        self.light = persistenceRepo.V3(0, 0, 1)

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

        self.zbuffer = [
            [-99999 for x in range(self.width)]
            for y in range(self.height)
        ]

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

    def points(self, x, y):
        self.pointsVisited[f'{x},{y}'] = (x, y)

    def clear_point(self):
        self.pointsVisited.clear()

    def point(self, x, y, is_save: bool, color):
        if is_save:
            self.points(x, y)
        self.framebuffer[y][x] = color or self.curr_color

    def shader(self, x, y):
        color = [55, 102, 172]
        point = [660, 460]
        if y < 1080 and y > 1080 - 240 - random.randint(0, 5):
            color = [23, 25, 47]
        if y < 1080 - 234 + random.randint(0, 20) and y > 1080 - 253 - random.randint(0, 5):
            color = [31, 47, 73]
        if y < 1080 - 255 + random.randint(0, 5) and y > 1080 - 262 - random.randint(0, 5):
            color = [24, 39, 62]
        if y < 1080 - 265 + random.randint(0, 5) and y > 1080 - 265 - random.randint(0, 5):
            color = [102, 138, 188]
        if y < 1080 - 275 + random.randint(0, 5) and y > 1080 - 275 - random.randint(0, 5):
            color = [54, 81, 124]

        if y < 1080 - 335 + random.randint(0, 10) and y > 1080 - 365 - random.randint(0, 5):
            color = [50, 83, 147]
        if y < 1080 - 395 + random.randint(0, 10) and y > 1080 - 425 - random.randint(0, 10):
            color = [95, 156, 236]
        if y < 1080 - 465 + random.randint(0, 10) and y > 1080 - 465 - random.randint(0, 10):
            color = [95, 156, 236]

        if y < 1080 - 535 + random.randint(0, 5) and y > 1080 - 555 - random.randint(0, 5):
            color = [133, 182, 254]

        if y < 1080 - 575 + random.randint(0, 10) and y > 1080 - 618 - random.randint(0, 10):
            color = [180, 224, 254]

        if y < 1080 - 715 + random.randint(0, 10) and y > 1080 - 745 - random.randint(0, 10):
            color = [93, 151, 224]
        if y < 1080 - 805 + random.randint(0, 10) and y > 1080 - 865 - random.randint(0, 10):
            color = [78, 112, 161]
        if y < 1080 - 865 + random.randint(0, 10) and y > 1080 - 877 - random.randint(0, 10):
            color = [104, 159, 202]
        if y < 1080 - 885 + random.randint(0, 10) and y > 1080 - 905 - random.randint(0, 10):
            color = [104, 155, 205]
        d = math.dist([point[0], point[1]], [x, y]) / 720
        d = 1-d
        color = [c*d for c in color]
        return self.glColor(color[0]/255, color[1]/255, color[2]/255)

    def load(self, filename, translate, scale):
        model = Obj(filename)

        for face in model.faces:
            vcount = len(face)
            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j + 1) % vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]

                x1 = round((v1[0] + translate[0]) * scale[0])
                y1 = round((v1[1] + translate[1]) * scale[1])
                x2 = round((v2[0] + translate[0]) * scale[0])
                y2 = round((v2[1] + translate[1]) * scale[1])
                self.glLine(x1, y1, x2, y2)

    # (100 puntos) Deben crear una función glLine(x0, y0, x1, y1) que se utilice para dibujar una línea recta de (x0, y0) a (x1, y1)
    def glLine(self, x0, y0, x1, y1, save_points: bool = False):

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

            dy = abs(y1 - y0)
            dx = abs(x1 - x0)

        offset = 0 * 2 * dx
        threshold = 0.5 * 2 * dx

        if x1 < x0:
            y = y1
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        else:
            y = y0
        points = []
        for x in range(x0, x1):
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))

            offset += (dy/dx) * 2 * dx
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * 2 * dx

        for point in points:
            self.point(
                *point,
                save_points
            )

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

    def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
        return persistenceRepo.V3(
            round((vertex[0] + translate[0]) * scale[0]),
            round((vertex[1] + translate[1]) * scale[1]),
            round((vertex[2] + translate[2]) * scale[2])
        )

    def triangle(self, A, B, C, color=None):
        xmin, xmax, ymin, ymax = persistenceRepo.bbox(A, B, C)
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                P = persistenceRepo.V2(x, y)
                w, v, u = persistenceRepo.barycentric(A, B, C, P)
                if w < 0 or v < 0 or u < 0:
                    continue
                color = self.shader(x, y)
                z = A.z * w + B.z * v + C.z * u
                try:
                    if z > self.zbuffer[x][y]:
                        self.point(y, x, False, color)
                        self.zbuffer[x][y] = z
                except:
                    pass

    def loads(self, filename, translate=(0, 0, 0), scale=(1, 1, 1)):
        model = Obj(filename)
        light = persistenceRepo.V3(0, 0, 1)

        for face in model.faces:
            vcount = len(face)

            if vcount == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                a = self.transform(model.vertices[f1], translate, scale)
                b = self.transform(model.vertices[f2], translate, scale)
                c = self.transform(model.vertices[f3], translate, scale)

                normal = persistenceRepo.norm(persistenceRepo.cross(
                    persistenceRepo.sub(b, a), persistenceRepo.sub(c, a)))
                intensity = persistenceRepo.dot(normal, self.light)
                grey = round(255 * intensity)

                if intensity < 0:
                    continue

                self.triangle(
                    a, b, c, persistenceRepo.ncolor(grey, grey, grey))

            else:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                vertices = [
                    self.transform(model.vertices[f1], translate, scale),
                    self.transform(model.vertices[f2], translate, scale),
                    self.transform(model.vertices[f3], translate, scale),
                    self.transform(model.vertices[f4], translate, scale),
                ]

                normal = persistenceRepo.norm(
                    persistenceRepo.cross(
                        persistenceRepo.sub(
                            vertices[0], vertices[1]
                        ),
                        persistenceRepo.sub(vertices[1], vertices[2])
                    )
                )

                intensity = persistenceRepo.dot(normal, light)
                grey = round(255 * intensity)

                if grey < 0:
                    continue

                A, B, C, D = vertices
                self.triangle(
                    A, B, C, persistenceRepo.ncolor(grey, grey, grey))
                self.triangle(
                    A, C, D, persistenceRepo.ncolor(grey, grey, grey))
