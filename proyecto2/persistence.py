class V3(object):
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

def add(A, B):
    try:
        return V3(
            A.x + B.x,
            A.y + B.y,
            A.z + B.z
        )
    except:
        return V3(
            A.x + B,
            A.y + B,
            A.z + B
        )

def sub(A, B):
    return V3(
        A.x - B.x,
        A.y - B.y,
        A.z - B.z
    )

def div(A, c):
    return V3(A.x / c, A.y / c, A.z / c)

def mul(A, c):
    return V3(A.x * c, A.y * c, A.z *c)

def length(A):
    return (A.x**2 + A.y**2 + A.z**2)**0.5

def norm(A):
    q = length(A)

    if q == 0:
        return V3(0, 0, 0)

    return V3(
        A.x / q,
        A.y / q,
        A.z / q
    )

def cross(A, B):
    cx = (A.y * B.z) - (A.z * B.y)
    cy = (A.z * B.x) - (A.x * B.z)
    cz = (A.x * B.y) - (A.y * B.x)
    return cx, cy, cz

def dot(A, B):
    return ((A.x * B.x) + (A.y * B.y) + (A.z * B.z))

def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(C.x - A.x, B.x - A.x, A.x - P.x),
        V3(C.y - A.y, B.y - A.y, A.y - P.y)
    )

    if cz == 0:
        return -1, -1, -1

    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)

    return w, v, u

def normal(A, B, C):
    cx, cy, cz = cross(
        sub(B, A),
        sub(C, A)
    )
    return V3(cx, cy, cz)

def direction(A, B, C):
    return norm(normal(A, B, C))

def reflect(I, N):
    return norm(sub(I, mul(N, dot(I, N)*2)))

def refract(I, N, refractive_index):
    cosi = -max(-1, min(1, dot(I, N)))
    etai = 1
    etat = refractive_index

    if cosi < 0: 
        cosi = -cosi
        etai, etat = etat, etai
        N = mul(N, -1)

    eta = etai/etat
    k = 1 - eta**2 * (1 - cosi**2)
    if (k < 0):
        return V3(1, 0, 0)
    
    return norm(add(mul(I, eta), mul(N, eta * cosi - k**(1/2))))
