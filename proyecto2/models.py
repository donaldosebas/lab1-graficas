from persistence import *
from obj import *

class Shpere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, origin, direction):
        L = sub(self.center, origin)
        tca = dot(L, direction)
        l = length(L)
        d2 = l**2 - tca**2
        if d2 > self.radius**2: return None
        thc = (self.radius**2 - d2)**1/2
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0: t0 = t1
        if t0 < 0: return None

        hit = add(origin, mul(direction, t0))
        normal = norm(sub(hit, self.center))

        return Intersect(
            distance=t0,
            point=hit,
            normal=normal
        )

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normal
        self.material = material

    def ray_intersect(self, origin, direction):
        ln = dot(direction, self.normal)
        if abs(ln) > 0.01:
            d = dot(self.normal, sub(self.position, origin)) / ln
            if d > 0:
                hit = add(origin, mul(direction, d))
                return Intersect(
                    distance=d,
                    point=hit,
                    normal=self.normal
                )

class Quadrilateral(object):
    def __init__(self, center, dimensions, material):
        self.center = center
        self.material = material
        self.faces = []

        self.max = add(center, add(div(dimensions, 2), 0.0001))
        self.min = sub(center, add(div(dimensions, 2), 0.0001))
        
        x2 = dimensions.x/2
        y2 = dimensions.y/2
        z2 = dimensions.z/2

        self.faces.append(Plane(add(center, V3(x2, 0, 0)), V3(1, 0, 0), material))
        self.faces.append(Plane(sub(center, V3(x2, 0, 0)), V3(-1, 0, 0), material))
        self.faces.append(Plane(add(center, V3(0, y2, 0)), V3(0, 1, 0), material))
        self.faces.append(Plane(sub(center, V3(0, y2, 0)), V3(0, -1, 0), material))
        self.faces.append(Plane(add(center, V3(0, 0, z2)), V3(0, 0, 1), material))
        self.faces.append(Plane(sub(center, V3(0, 0, z2)), V3(0, 0, -1), material))
    
    def ray_intersect(self, orig, dir):
        intersect, d = None, float('inf')
        for face in self.faces:
            hited = face.ray_intersect(orig, dir)
            if hited:
                enter = 0
                if self.min.x <= hited.point.x <= self.max.x: enter+=1
                if self.min.y <= hited.point.y <= self.max.y: enter+=1
                if self.min.z <= hited.point.z <= self.max.z: enter+=1
                
                if enter == 3 and hited.distance < d:
                    d = hited.distance
                    intersect = Intersect(
                        distance = d,
                        point = hited.point,
                        normal = hited.normal
                    )
        return intersect

class Triangle(object):
    def __init__(self, points, material):
        self.A, self.B, self.C = points
        self.center = div(add(add(points[0], points[1]), points[2]), 3)
        self.normal = norm(V3(*cross(sub(self.B, self.A), sub(self.C, self.A))))
        self.material = material
    

    def ray_intersect(self, origin, direction):
        ln = dot(direction, self.normal)
        if abs(ln) > 0.01:
            d = dot(self.normal, sub(self.center, origin)) / ln
            if d > 0:
                hit = add(origin, mul(direction, d))
                w, v, u = barycentric(self.A, self.B, self.C, hit)
                if w < 0 or v < 0 or u < 0: return None
                return Intersect(
                    distance=d,
                    point=hit,
                    normal=self.normal
                )
