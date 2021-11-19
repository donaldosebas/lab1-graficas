import pygame

class Life(object):
    def __init__(self, screen, init):
        self.screen = screen
        self.points = []
        for point in init: self.pixel(*point)

    def clear(self):
        self.points = []
        self.screen.fill((0, 0, 0))

    def pixel(self, x, y):
        try: self.screen.set_at((x, y), (255, 255, 255))
        except: pass

    def copy(self):
        self.prev_turn = self.screen.copy()

    def render(self):
        for x in range(100):
            for y in range(100):
                is_alive = self.prev_turn.get_at((x, y))[0] == 255
                neighbors_count = 0
                
                for i in range(max(0, x-1), min(x+2, 100)):
                    for j in range(max(0, y-1), min(y+2, 100)):
                        if self.prev_turn.get_at((i, j))[0] == 255: neighbors_count += 1

                # Checks conditions
                if is_alive:
                    neighbors_count -= 1
                    if (2 <= neighbors_count <= 3): self.points.append((x, y))
                else:
                    if neighbors_count == 3: 
                        self.points.append((x, y))

        for point in self.points:
            self.pixel(*point)

pygame.init()
screen = pygame.display.set_mode((100, 100))

def ring(x, y):
    return [
        (x, y),
        ((x+1), y),
        ((x+2), y),
        ((x+4), y),
        ((x+5), y),
        ((x+6), y),

        (x, (y+1)),
        ((x+2), (y+1)),
        ((x+4), (y+1)),
        ((x+6), (y+1)),

        (x, (y+2)),
        ((x+1), (y+2)),
        ((x+2), (y+2)),
        ((x+4), (y+2)),
        ((x+5), (y+2)),
        ((x+6), (y+2))
    ]

def leaf(x, y):
    return [
        ((x+3), y),
        ((x+5), y),
        ((x+1), (y+1)),
        ((x+2), (y+1)),
        ((x+3), (y+1)),
        ((x+5), (y+1)),
        ((x+6), (y+1)),
        ((x+7), (y+1)),
        (x, (y+2)),
        ((x+4), (y+2)),
        ((x+8), (y+2)),
        (x, (y+3)),
        ((x+2), (y+3)),
        ((x+6), (y+3)),
        ((x+8), (y+3)),
        ((x+1), (y+4)),
        ((x+2), (y+4)),
        ((x+4), (y+4)),
        ((x+6), (y+4)),
        ((x+7), (y+4)),

        ((x+1), (y+6)),
        ((x+2), (y+6)),
        ((x+4), (y+6)),
        ((x+6), (y+6)),
        ((x+7), (y+6)),
        (x, (y+7)),
        ((x+2), (y+7)),
        ((x+6), (y+7)),
        ((x+8), (y+7)),
        (x, (y+8)),
        ((x+4), (y+8)),
        ((x+8), (y+8)),
        ((x+1), (y+9)),
        ((x+2), (y+9)),
        ((x+3), (y+9)),
        ((x+5), (y+9)),
        ((x+6), (y+9)),
        ((x+7), (y+9)),
        ((x+3), (y+10)),
        ((x+5), (y+10)),
    ]

def glider(x, y):
    return [
        ((x+2), y),
        (x, (y+1)),
        ((x+2), (y+1)),
        ((x+1), (y+2)),
        ((x+2), (y+2)),
    ]

def lwss(x, y):
    return [
        (x+1, y),
        (x+2, y),
        (x, y+1),
        (x+1, y+1),
        (x+2, y+1),
        (x+3, y+1),
        (x, y+2),
        (x+1, y+2),
        (x+3, y+2),
        (x+4, y+2),
        (x+2, y+3),
        (x+3, y+3), 
    ]


states = [
    ring(10, 10),
    ring(90, 90),
    ring(10, 90),
    ring(90, 10),
    leaf(50, 50),
    leaf(20, 20),
    leaf(80, 80),
    glider(45, 45),
    glider(70, 70),
    glider(50, 0),
    glider(80, 80),
    lwss(80, 50)
]

points = []
for state in states:
    for cell in state:
        points.append(cell)

r = Life(screen, points)

reps = 0
while reps < 500:
    pygame.time.delay(10)
    r.copy()
    r.clear()
    r.render()
    reps += 1
    pygame.display.flip()