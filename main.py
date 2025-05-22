import pygame
import sys


class Kirby:
    def __init__(self, position):
        self.pos = pygame.Vector2(position)
        self.size = 50
        self.surface = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

    def update(self):
        # Met à jour la position du Rect
        self.surface.topleft = self.pos

    def move(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy
        self.update()

class Dot:
    def __init__(self, position, velocity):
        self.pos = pygame.Vector2(position)
        self.vel = pygame.Vector2(velocity)
        self.size = 25
        self.surface = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

    def update(self, bounds):
        # Avancer
        self.pos += self.vel

        # Rebond contre les murs
        if self.pos.x <= 0 or self.pos.x + self.size >= bounds[0]:
            self.vel.x *= -1
            self.pos.x = max(0, min(self.pos.x, bounds[0] - self.size))

        if self.pos.y <= 0 or self.pos.y + self.size >= bounds[1]:
            self.vel.y *= -1
            self.pos.y = max(0, min(self.pos.y, bounds[1] - self.size))

        # Met à jour la position du Rect
        self.surface.topleft = self.pos

    def collide_with(self, other):
        return self.surface.colliderect(other.surface)

    def bounce_with(self, other):
        self.vel.x, other.vel.x = other.vel.x, self.vel.x
        self.vel.y, other.vel.y = other.vel.y, self.vel.y

class Simulation:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = (1000,1000)
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption("EvolveWorld")
        self.clock = pygame.time.Clock()
        self.running = True

        self.items = [
            Dot((100, 100), (2, 1)),
            Dot((200, 200), (-2, -1)),
            Dot((300, 150), (1, -2)),
            Dot((400, 300), (-1, 2))
        ]

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        for dot in self.items:
            dot.update((self.width, self.height))

        # Collision entre dots
        for i in range(len(self.items)):
            for j in range(i + 1, len(self.items)):
                a = self.items[i]
                b = self.items[j]
                if a.collide_with(b):
                    a.bounce_with(b)

    def render(self):
        self.window.fill((0, 0, 0))
        for el in self.items:
            pygame.draw.rect(self.window, (255, 0, 0), el.surface)
        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(140)

sim = Simulation()
sim.run()
