from obj import *
from persistence import *
from models import *
from math import tan, pi
from random import random

MAX_RECURSION = 3

class Raytracer(object):
    def __init__(self, width, height, bgcolor=BLACK):
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.scene = []
        self.clear()
    
    def clear(self):
        self.pixels = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]
    
    def write(self, filename='output.bmp'):
        glFinish(self.width, self.height, self.pixels, filename)

    def point(self, x, y, color):
        self.pixels[y][x] = color

    def cast_ray(self, origin, direction, recursion=0):
        material, intersect = self.scene_intersect(origin, direction)
        
        if not material or recursion >= MAX_RECURSION: return self.bgcolor
        offset_normal = mul(intersect.normal, 1.1)

        # Albedos
        reflect_color = color(0, 0, 0)
        if material.albedo[2] > 0:
            reverse_direction = mul(direction, -1)
            reflect_dir = reflect(reverse_direction, intersect.normal)
            reflect_origin = sub(intersect.point, offset_normal) if dot(reflect_dir, intersect.normal) < 0 else add(intersect.point, offset_normal)
            reflect_color = self.cast_ray(reflect_origin, reflect_dir, recursion + 1)
            
        refract_color = color(0, 0, 0)
        if material.albedo[3] > 0:
            refract_dir = refract(direction, intersect.normal, material.refractiveI)
            refract_origin = sub(intersect.point, offset_normal) if dot(refract_dir, intersect.normal) < 0 else add(intersect.point, offset_normal)
            refract_color = self.cast_ray(refract_origin, refract_dir, recursion + 1)

        light_dir = norm(sub(self.light.position, intersect.point))
        light_distance = length(sub(self.light.position, intersect.point))

        shadow_origin = sub(intersect.point, offset_normal) if dot(light_dir, intersect.normal) < 0 else add(intersect.point, offset_normal)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_origin, light_dir)
        shadow_intensity = 0

        if shadow_material and length(sub(shadow_intersect.point, shadow_origin)) < light_distance:
            shadow_intensity = 0.9
        
        intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

        specular_reflection = reflect(light_dir, intersect.normal)
        specular_intensity = self.light.intensity * (
            max(0, -dot(specular_reflection, direction))**material.spec
        )

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
        reflection = reflect_color * material.albedo[2]
        refraction = refract_color * material.albedo[3]

        return diffuse + specular + reflection + refraction

    def scene_intersect(self, origin, direction):
        zbuffer = float('inf')
        material, intersect = None, None
        for figure in self.scene:
            hit = figure.ray_intersect(origin, direction)
            if hit and hit.distance < zbuffer:
                zbuffer = hit.distance
                material = figure.material
                intersect = hit
        return material, intersect

    def render(self):
        fov = int(pi/2)
        ar = self.width/self.height
        for y in range(self.height):
            for x in range(self.width):
                if random() > 0:
                    i =  (2*(x + 0.5)/self.width - 1) * tan(fov/2) * ar
                    j =  (2*(y + 0.5)/self.height - 1) * tan(fov/2)
                    self.point(x, y, self.cast_ray(V3(0, 0, 10), norm(V3(i, j, -1))))

    def loads(self, filename, material):
        model = Obj(filename)
        for face in model.faces:
            size = len(face)
            # Points of every face
            f = face[0][0] - 1
            dot = model.vertices[f]
            A = V3(*dot)
            f = face[1][0] - 1
            dot = model.vertices[f]
            B = V3(*dot)
            f = face[2][0] - 1
            dot = model.vertices[f]
            C = V3(*dot)

            self.scene.append(Triangle((A, B, C), material))

            if size == 4:
                f = face[3][0] - 1
                dot = model.vertices[f]
                D = V3(*dot)
                self.scene.append(Triangle((A, C, D), material))

# Materials
ivory = Material(color(100, 100, 80), albedo=[0.6, 0.3, 0.1, 0], spec=50)
rubber = Material(color(80, 0, 0), albedo=[0.9, 0.1, 0, 0], spec=10)
mirror = Material(color(255, 255, 255), albedo=[0, 10, 0.8, 0], spec=1425)
glass = Material(color(150, 180, 200), albedo=(0, 0.5, 0.1, 0.8), spec=125, refractiveI=1.5)
cloud = Material(color(243, 241, 231), albedo=(0.5, 0.3, 0, 0), spec=10)
moon = Material(color(237,199,30), albedo=(0.6, 0.12, 0, 0), spec=50)

r = Raytracer(200, 200, color(135, 206, 235))
r.light = Light(
    position=V3(2, 0, 10),
    intensity=1.5
)

r.scene = [
    # Moon
    Shpere(V3(-7, 9, -15), 3, moon),
    
    # Right corner cloud
    Quadrilateral(V3(8, 11, -13), V3(3.5, 2, 2.5), cloud),
    Quadrilateral(V3(8, 8, -13), V3(3, 3, 5), cloud),
    Quadrilateral(V3(8, 8, -13), V3(3, 3, 5), cloud),
    Quadrilateral(V3(8, 10, -15), V3(5, 2, 7), cloud),
    Quadrilateral(V3(7, 8, -15), V3(3, 2, 2), cloud),

    # Air plane
    Quadrilateral(V3(6, -7, -12), V3(2, 2, 8), glass),
    Quadrilateral(V3(1, -7, -12), V3(10, 3.5, 6), ivory),
    Quadrilateral(V3(-5, -7, -12), V3(3, 2, 2), ivory),

        # Wings
    Quadrilateral(V3(1.75, -6, -7), V3(4, 1, 4), ivory),
    Quadrilateral(V3(1.75, -6, -18), V3(4, 1, 4), ivory),

        # Up rectangles 
    Quadrilateral(V3(1.75, -4, -7), V3(1, 3, 1), ivory),  
    Quadrilateral(V3(1.75, -4, -18), V3(1, 3, 1), ivory),  

        # Up Wing
    Quadrilateral(V3(1.75, -2, -12.5), V3(6, 1, 12), ivory), 
]

r.loads('block.obj', rubber)
r.render()
r.write()