import struct
from collections import namedtuple


class Persistence(object):
    def __init__(self):
        self.V3 = namedtuple('Point3D', ['x', 'y', 'z'])
        self.V2 = namedtuple('Point2D', ['x', 'y'])

    def color(self, r: float = 0, g: float = 0, b: float = 0):
        return bytes([int(b * 255), int(g * 255), int(r * 255)])

    def word(self, w):
        return struct.pack('=h', w)

    def dword(self, w):
        return struct.pack('=l', w)

    def length(self, v0):
        return (v0.x ** 2 + v0.y ** 2 + v0.z ** 2) ** 0.5

    def dot(self, v0, v1):
        return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

    def sub(self, v0, v1):
        return self.V3(
            v0.x - v1.x,
            v0.y - v1.y,
            v0.z - v1.z
        )

    def ncolor(self, r, g, b):
        return bytes([b, g, r])

    def norm(self, v0):
        l = self.length(v0)

        if l == 0:
            return self.V3(0, 0, 0)

        return self.V3(
            v0.x/l,
            v0.y/l,
            v0.z/l
        )

    def bbox(self, A, B, C):
        xs = [A.x, B.x, C.x]
        xs.sort()
        ys = [A.y, B.y, C.y]
        ys.sort()
        return xs[0], xs[-1], ys[0], ys[-1]

    def barycentric(self, A, B, C, P):
        cx, cy, cz = self.cross(
            self.V3(B.x - A.x, C.x - A.x, A.x - P.x),
            self.V3(B.y - A.y, C.y - A.y, A.y - P.y)
        )

        if cz == 0:
            return -1, -1, -1
        u = cx/cz
        v = cy/cz
        w = 1 - (cx + cy) / cz
        return w, v, u

    def cross(self, v0, v1):
        cx = v0.y * v1.z - v0.z * v1.y
        cy = v0.z * v1.x - v0.x * v1.z
        cz = v0.x * v1.y - v0.y * v1.x
        return self.V3(cx, cy, cz)
