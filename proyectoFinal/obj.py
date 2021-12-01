import struct

def char(c): return struct.pack('=c', c.encode('ascii'))

def word(w): return struct.pack('=h', w)

def dword(dw): return struct.pack('=l', dw)

def color(r, g, b): 
    r = min(max(0, r), 255)
    b = min(max(0, b), 255)
    g = min(max(0, g), 255)
    return bytes([b, g, r])
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f: self.lines = f.read().splitlines()
        self.vertices = []
        self.tvertices = []
        self.normals = []
        self.faces = []
        self.read()

    def read(self):
        for line in  self.lines:
            try:
                if line:
                    prefix, value = line.split(' ', 1)
                    if prefix == 'v':
                        self.vertices.append(
                            list(map(float, value.split(' ')))
                        )
                    elif prefix == 'vt':
                        self.tvertices.append(
                            list(map(float, value.split(' ')))
                        )
                    elif prefix == 'vn':
                        self.normals.append(
                            list(map(float, value.split(' ')))
                        )
                    elif prefix == 'f':
                        self.faces.append(
                            [list(map(int, face.split('/'))) for face in value.split(' ')]
                        )
            except: pass


class Texture(object):
    def __init__(self, path):
        self.path = path
        self.pixels = []
        self.read()
    
    def read(self):
        image = open(self.path, 'rb')
        image.seek(10)
        header_size = struct.unpack('=l', image.read(4))[0]
        image.seek(18)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(header_size)
        for x in range(self.height):
            temp = []
            for y in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                temp.append(color(r, g, b))
            self.pixels.append(temp)
        image.close()

    def get_color(self, tx, ty):
        x = int(tx * self.width) -1
        y = int(ty * self.height) - 1

        return self.pixels[y][x]
