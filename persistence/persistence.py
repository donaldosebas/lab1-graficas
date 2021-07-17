import struct


class Persistence(object):
    def color(self, r: float = 0, g: float = 0, b: float = 0):
        return bytes([int(b * 255), int(g * 255), int(r * 255)])

    def word(self, w):
        return struct.pack('=h', w)

    def dword(self, w):
        return struct.pack('=l', w)
