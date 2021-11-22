import struct

def char(c): return struct.pack('=c', c.encode('ascii'))

def word(w): return struct.pack('=h', w)

def dword(dw): return struct.pack('=l', dw)

class Material(object):
    def __init__(self, diffuse, albedo, spec, refractiveI=0):
        self.diffuse = diffuse
        self.albedo = albedo
        self.spec = spec
        self.refractiveI = refractiveI

class Intersect(object):
    def __init__(self,  distance, normal, point):
        self.distance = distance
        self.normal = normal
        self.point = point

class Light(object):
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other_color):
        r = self.r + other_color.r
        g = self.g + other_color.g
        b = self.b + other_color.b

        return color(r, g, b)

    def __mul__(self, other):
        r = self.r * other
        g = self.g * other
        b = self.b * other
        return color(r, g, b)

    def __repr__(self):
        return "color(%s, %s, %s)" % (self.r, self.g, self.b)

    def toBytes(self):
        self.r = int(max(min(self.r, 255), 0))
        self.g = int(max(min(self.g, 255), 0))
        self.b = int(max(min(self.b, 255), 0))
        return bytes([self.b, self.g, self.r])

    __rmul__ = __mul__

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f: self.lines = f.read().splitlines()
        self.vertices = []
        self.faces = []
        self.read()

    def read(self):
        for line in  self.lines:
            try:
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(
                        list(map(float, value.split(' ')))
                    )
                elif prefix == 'f':
                    self.faces.append(
                        [list(map(int, face.split('/'))) for face in value.split(' ')]
                    )
            except: pass

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

def glFinish(width, height, pixels, filename):
    with open(filename, "wb") as file:
        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))
        file.write(dword(
            14 + 40 + (width * height * 3)))
        file.write(dword(0))
        file.write(dword(54))
        file.write(dword(40))
        file.write(dword(width))
        file.write(dword(height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(width * height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        for y in range(height):
            for x in range(width):
                file.write(pixels[y][x].toBytes())
        file.close()
