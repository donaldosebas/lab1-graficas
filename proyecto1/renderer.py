from math import sin, cos
from obj import *
from persistence import *
import random

class Renderer(object):
    def __init__(self, width: int = 0, height: int = 0):
        self.initial_width = width
        self.initial_height = height

        # Para texturas
        self.texture = None
        self.normalmap = None
        self.activeShader = None

        # Modelos en 3d
        self.light = V3(0, 0, 1)

    # (05 puntos) Deben crear una función glInit() que inicialice cualquier objeto interno que requiera su software renderer
    def glInit(self, curr_color=None, clear_color=None):
        self.curr_color = curr_color or color(125, 125, 125)
        self.clear_color = clear_color or color(255, 255, 255)
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

    # (20 puntos) Deben crear una función glClear() que llene el mapa de bits con un solo color
    def glClear(self):
        self.framebuffer = [[BLACK for y in range(
            self.height)] for x in range(self.width)]

        self.zbuffer = [
            [-99999 for x in range(self.width)]
            for y in range(self.height)
        ]

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

        for dot in points:
            self.dot(
                *dot,
                save_points
            )


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



    def dot(self, x, y, color=None):
        self.framebuffer[y][x] = color or WHITE


    def loadViewMatrix(self, x, y, z, center):
        M = Matrix([
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1]
        ])

        O = Matrix([
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]
        ])

        self.View = M * O


    def loadProjectionMatrix(self, coeff):
        self.Projection = Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coeff, 1]
        ])


    def loadViewPortMatrix(self, x=0, y=0):
        self.ViewPort = Matrix([
            [self.width/2, 0, 0, x + self.width/2],
            [0, self.height/2, 0, y + self.height/2],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ])


    def lookAt(self, eye, center, up):
        z = norm(sub(eye, center))
        x = norm(V3(*cross(up, z)))
        y = norm(V3(*cross(z, x)))
        
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(
            -1/length(sub(eye, center))
        )
        self.loadViewPortMatrix(0, 0)


    def loadTransformMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        Translation = Matrix([
            [1, 0, 0, translate[0]],
            [0, 1, 0, translate[1]],
            [0, 0, 1, translate[2]],
            [0, 0, 0, 1]
        ])

        # Para rotar el modelo
        a = rotate[0]
        Rotationx = Matrix([
            [1, 0, 0, 0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a), cos(a), 0],
            [0, 0, 0, 1]
        ])

        a = rotate[1]
        Rotationy = Matrix([
            [cos(a), 0, sin(a), 0],
            [0, 1, 0, 0],
            [-sin(a), 0, cos(a), 0],
            [0, 0, 0, 1]
        ])

        a = rotate[2]
        Rotationz = Matrix([
            [cos(a), -sin(a), 0, 0],
            [sin(a), cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        Rotation = Rotationx * Rotationy * Rotationz

        # La escala se modifica
        Scale = Matrix([
            [scale[0], 0, 0, 0],
            [0, scale[1], 0, 0],
            [0, 0, scale[2], 0],
            [0, 0, 0, 1]
        ])

        Model = Translation * Rotation * Scale

        self.Matrix = self.ViewPort * self.Projection * self.View * Model


    def transform(self, vector):
        temp = Matrix([
            [vector.x],
            [vector.y],
            [vector.z],
            [1]
        ])
        # Se realizan las transformaciones
        transformed = self.Matrix * temp 
        result = transformed.matrix
        x = round(result[0][0]/result[3][0])
        y = round(result[1][0]/result[3][0])
        z = round(result[2][0]/result[3][0])
        return V3(x, y, z)


    def loads(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0), texturename=None, normalmap=None):
        model = Obj(filename)
        if texturename: self.texture = Texture(texturename)
        if normalmap: self.normalmap = Texture(normalmap)
        self.loadTransformMatrix(translate, scale, rotate)
        hasTexture = len(model.tvertices) > 0
        hasNormal = len(model.normal) > 0
        for face in model.faces:
            size = len(face)

            # Points of every face
            f = face[0][0] - 1
            dot = model.vertices[f]
            A = self.transform(V3(*dot))

            f = face[1][0] - 1
            dot = model.vertices[f]
            B = self.transform(V3(*dot))

            f = face[2][0] - 1
            dot = model.vertices[f]
            C = self.transform(V3(*dot))

            # Textures
            if hasTexture:
                tf = face[0][1] - 1
                tpoint = model.tvertices[tf]       
                tA = V3(*tpoint)
                
                tf = face[1][1] - 1
                tpoint = model.tvertices[tf]       
                tB = V3(*tpoint)

                tf = face[2][1] - 1
                tpoint = model.tvertices[tf]       
                tC = V3(*tpoint)
                textures=(tA, tB, tC)
            else:
                textures=None
            
            # Normals
            if hasNormal:
                tn = face[0][2] - 1
                normal = model.normal[tn]      
                nA = V3(*normal)

                tn = face[1][2] - 1
                normal = model.normal[tn]      
                nB = V3(*normal)

                tn = face[2][2] - 1
                normal = model.normal[tn]      
                nC = V3(*normal)
                normals=(nA, nB, nC)
            else:
                normals=None

            self.triangle(points=(A, B, C), texture=textures, normal=normals)

            if size == 4:
                f = face[3][0] - 1
                dot = model.vertices[f]
                D = self.transform(V3(*dot))
                
                if hasTexture:
                    tf = face[3][1] - 1
                    tpoint = model.tvertices[tf]       
                    tD = V3(*tpoint)
                    textures=(tA, tC, tD)
                else:
                    textures=None

                if hasNormal:
                    tn = face[0][2] - 1
                    normal = model.normal[tn]      
                    nD = V3(*normal)
                    normals=(nA, nC, nD)
                else:
                    normals=None

                self.triangle(points=(A, C, D), texture=textures, normal=normals)


    def defaultShader(self, A, B, C):
        normal = getNormalDirection(A, B, C)
        # Luego la intensidad con la que se pinta
        return dot(normal, self.light)


    def shader(self, **kwargs):
        w, v, u = kwargs['bar']
        tx, ty = kwargs['tcords']
        nA, nB, nC = kwargs['normals']
        tcolor = self.texture.get_color(tx, ty)
        iA, iB, iC = [dot(n, self.light) for n in (nA, nB, nC)]
        intensity = w*iA + v*iB + u*iC
        b, g, r = [int(c * intensity) if intensity > 0 else 0 for c in tcolor]
        return color(r, g, b)


    def fragmentI(self, **kwargs):
        w, v, u = kwargs['bar']
        tx, ty = kwargs['tcords']
        nA, nB, nC = kwargs['normals']

        grey = int(tx * 150)
        tcolor = color(grey, 100, 100)

        iA, iB, iC = [dot(n, self.light) for n in (nA, nB, nC)]
        intensity = w*iA + v*iB + u*iC

        if intensity > 0.85:
            intensity = 0
        elif intensity > 0.60:
            intensity = 0.30
        elif intensity > 0.45:
            intensity = 0.45
        elif intensity > 0.30:
            intensity = 0.60
        elif intensity > 0.15:
            intensity = 0.80
        else:
            intensity = 1

        b, g, r = [int(c * intensity) if intensity > 0 else 0 for c in tcolor]

        return color(r, g, b)


    def fragment(self, **kwargs):
        w, v, u = kwargs['bar']
        _, ty = kwargs['tcords']
        nA, nB, nC = kwargs['normals']

        grey = int(ty * 256)
        tcolor = color(grey, 100, 100)

        iA, iB, iC = [dot(n, self.light) for n in (nA, nB, nC)]
        intensity = w*iA + v*iB + u*iC

        if intensity > 0.85: intensity = 1
        elif intensity > 0.60: intensity = 0.80
        elif intensity > 0.45: intensity = 0.60
        elif intensity > 0.30: intensity = 0.45
        elif intensity > 0.15: intensity = 0.30
        else: intensity = 0

        b, g, r = [int(c * intensity) if intensity > 0 else 0 for c in tcolor]

        return color(r, g, b)


    def normalShader(self, tx, ty, intensity):
        tcolor = self.texture.get_color(tx, ty)
        b, g, r = [int(c * intensity) if intensity > 0 else 0 for c in tcolor]
        return color(r, g, b)


    def dark(self, **kwargs):
        w, v, u = kwargs['bar']
        tx, ty = kwargs['tcords']
        nA, nB, nC = kwargs['normals']

        iA, iB, iC = [dot(n, self.light) for n in (nA, nB, nC)]
        intensity = (w*iA + v*iB + u*iC)*tx*ty

        tcolor = color(200, 200, 200)

        b, g, r = [int(c * intensity) if intensity > 0 else 0 for c in tcolor]

        return color(r, g, b)


    def mapshader(self, **kwargs):
        tx, ty = kwargs['tcords']
        tcolor = self.texture.get_color(tx, ty)
        ncolor = self.normalmap.get_color(tx, ty)
        z, y, x = [int(c)/255 for c in (ncolor)]
        ncolor = V3(x, y, z)
        intensity = dot(ncolor, self.light)
        
        b, g, r = [int(c * intensity) if intensity > 0 else 0 for c in tcolor]
        return color(r, g, b)


    def triangle(self, points, texture=None, normal=None):
        # Inofrmation of triangle
        A, B, C = points
        if texture: tA, tB, tC = texture
        if normal: nA, nB, nC = normal
        xmin, xmax, ymin, ymax = bbox(A, B, C)
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                w, v, u = barycentric(A, B, C, V3(x, y))
                if w < 0 or v < 0 or u < 0: continue
                
                if self.texture:
                    tx = (tA.x * w + tB.x * v + tC.x * u)
                    ty = (tA.y * w + tB.y * v + tC.y * u)

                    tx = tx if tx <= 1 else 1
                    ty = ty if ty <= 1 else 1
                    if normal:
                        paint = self.activeShader(
                            bar=(w, v, u),
                            tcords=(tx, ty),
                            normals=(nA, nB, nC)
                        )
                    
                    else:
                        intensity = self.defaultShader(A, B, C)
                        paint = self.normalShader(tx, ty, intensity)

                else:

                    if normal and texture:
                        tx = ((A.x * w) + (B.x * v) + (C.x * u))/self.width
                        ty = ((A.y * w) + (B.y * v) + (C.y * u))/self.height
                        
                        paint = self.activeShader(
                            bar=(w, v, u),
                            tcords=(tx, ty),
                            normals=(nA, nB, nC)
                        )
                    else:
                        # Esta dentro del triangulo
                        intensity = self.defaultShader(A, B, C)
                        base = round(200*intensity)

                        if (base < 0):
                            continue
                        elif (base > 255):
                            base = 255
                            
                        paint = color(base, base, base)

                z = (A.z * w) + (B.z * v) + (C.z * u)

                try:
                    if z > self.zbuffer[y][x]:
                        self.dot(x, y, paint)
                        self.zbuffer[y][x] = z
                except: pass


    def glFinish(self, filename: str = 'output.bmp'):
        with open(filename, "wb") as file:
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(
                14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.framebuffer[y][x])

back = Texture('./models/back.bmp')
r = Renderer(back.width, back.height)
r.glCreateWindow(back.width, back.height)
r.framebuffer = back.pixels
r.activeShader = r.shader
r.lookAt(V3(0, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
pi = 3.14

r.activeShader = r.fragmentI
r.loads(
    './models/star.obj', 
    (0, 0, 0), 
    (1/8, 1/8, 1/2),
    (0, 0, 0))

r.activeShader = r.dark
r.loads(
    './models/alien.obj', 
    (2/3, 1/4, 0), 
    (1/16, 1/4, 1/2),
    (0, 0, 0))

r.activeShader = r.fragment
r.loads(
    './models/planet/sphere.obj', 
    (-1/2, 2/3, 0), 
    (1/2, 1/2, 1/10),
    (pi/4, pi/10, 0),
    './models/planet/planet.bmp')

r.activeShader = r.mapshader
r.loads(
    './models/box/box.obj', 
    (2/3, -2/3, 0), 
    (1/2, 1/2, 1/2),
    (pi/8, pi/2, 0),
    './models/box/texture.bmp',
    './models/box/normal.bmp'
    )
r.texture = None

r.activeShader = r.fragment
r.loads(
    './models/20facestar.obj', 
    (-2/3, -5/6, -2), 
    (1/16, 1/84, 1/4),
    (pi/8, 0, 0)
    )

r.glFinish()
