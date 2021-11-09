class V3(object):
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

class Matrix(object):
    # Las matrices se leen m x n
    def __init__(self, matrix):
        self.matrix = matrix
        self.m = len(matrix)
        self.n = len(matrix[0]) if self.m > 0 else 0

    def __add__(self, o):
        if (self.n != o.n) or (self.m != o.m):
            return None
        
        result = []
        # Se restan las coordenadas
        for m in range(self.m):
            result.append([])
            for n in range(self.n):
                result[m].append(self.matrix[m][n] + o.matrix[m][n])
        return Matrix(result)
    
    def __sub__(self, o):
        if (self.n != o.n) or (self.m != o.m):
            return None
        
        result = []
        # Se restan las coordenadas
        for m in range(self.m):
            result.append([])
            for n in range(self.n):
                result[m].append(self.matrix[m][n] - o.matrix[m][n])
        return Matrix(result)

    def __mul__(self, o):
        if (self.n != o.m):
            return None
        
        result = []
        for _ in range(self.m):    # Estableciendo filas
            result.append([])

        # Obteniendo los multiplicadores
        mult = []
        for on in range(o.n):
            mult.append([])
            for om in range(o.m):
                mult[on].append(o.matrix[om][on])

        # Realizando la multiplicacion
        j = 0
        for mm in range(len(mult)): # Selecciono el vector a mult
            for sm in range(self.m): # Selecciono la fila
                temp = 0
                for i in range(self.n): # Elementos de cada fila
                    temp += self.matrix[sm][i] * mult[mm][i]
                result[j].append(temp)
                j = (j + 1) % (self.m) 

        return Matrix(result)

def sub(A, B):
    return V3(
        A.x - B.x,
        A.y - B.y,
        A.z - B.z
    )

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

def getNormal(A, B, C):
    cx, cy, cz = cross(
        sub(B, A),
        sub(C, A)
    )
    return V3(cx, cy, cz)

def getNormalDirection(A, B, C):
    return norm(getNormal(A, B, C))

def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    ys = [A.y, B.y, C.y]
    xs.sort()
    ys.sort()
    return xs[0], xs[-1], ys[0], ys[-1]
