import pygame
import sys
import math
import time
import random
import numpy as np

class Entity:
    def __init__(self, position, velocity,size = 25):
        self.pos = pygame.Vector2(position)
        self.vel = pygame.Vector2(velocity)
        self.size = size
        self.speed = 1
        self.surface = pygame.Rect(self.pos.x+self.size/2, self.pos.y+self.size/2, self.size, self.size)
        self.color = (0,0,0)

    def update(self, bounds):
        # Avancer
        self.pos += (self.vel * self.speed)

        # Rebond contre les murs
        if self.pos.x <= 0 or self.pos.x + self.size >= bounds[0]:
            self.vel.x *= -1
            self.pos.x = max(0, min(self.pos.x, bounds[0] - self.size))

        if self.pos.y <= 0 or self.pos.y + self.size >= bounds[1]:
            self.vel.y *= -1
            self.pos.y = max(0, min(self.pos.y, bounds[1] - self.size))

        # Met à jour la position du Rect
        self.surface.topleft = self.pos + (self.size/2,self.size/2)

    def collide_with(self, other):
        return self.surface.colliderect(other.surface)

    def bounce_with(self, other):
            self.vel.x, other.vel.x = other.vel.x, self.vel.x
            self.vel.y, other.vel.y = other.vel.y, self.vel.y

    
class Spike(Entity):
    def __init__(self, position, velocity):
        super().__init__(position, velocity)
        self.speed=3

    
    


class Kirby(Entity):
    def __init__(self, position, velocity,size,speed,vision):
        super().__init__(position, velocity,size)
        self.color = (255,0,0)
        self.timeAlive = 0
        self.vision = vision
        self.speed = speed
        self.size = size
    
    def __str__(self):
        return "Kirby : size = %s, speed = %s, vision %s" % (self.size,self.speed,self.vision)

    def escape(self,spike: Spike):
        if self.pos.distance_to(spike.pos) <= self.vision*10:
            vecteur = pygame.Vector2(spike.pos.x - self.pos.x,spike.pos.y-self.pos.y)
            vecteurNorm = vecteur.normalize()
            self.vel= - vecteurNorm

    def update(self, bounds):
        self.timeAlive +=1
        return super().update(bounds)
    
    def mutate(self):
        gene = random.randint(0,2)
        idk = 1 if random.randint(0,1) == 1 else -1
        match gene:
            case 0:
                self.size+= random.randint(1,3) * idk
            case 1:
                self.speed+= 1 * idk
            case 2:
                self.vision += 1 * idk
        self.surface = pygame.Rect(self.pos.x+self.size/2, self.pos.y+self.size/2, self.size, self.size)
        

class Simulation:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = (800,600)
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption("EvolveWorld")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.kirbyGeneration:list[Kirby] = []
        self.generationRunning = True
        self.spikes:list[Spike] = []
        self.gen = 1
        self.kirbys : list[Kirby] = []
        self.history = []

    def generateRandomKirby(self):
        size = 25
        speed = 3
        vision = 4
        return Kirby((random.randint(0,self.width),random.randint(0,self.height)),(random.randint(-1,1),random.randint(-1,1)),size,speed,vision)

    def generateSpikes(self):
        return Spike((random.randint(0,self.width),random.randint(0,self.height)),(random.randint(-2,2),random.randint(-2,2)))

    def selection(self):
        def sorter(e):
            return e.timeAlive
        self.kirbyGeneration.sort(key=sorter,reverse=True)
    
    def reproduction(self,kirby1: Kirby,kirby2:Kirby):
        return Kirby((0,0),(0,0),int((kirby1.size+kirby2.size)/2),int((kirby1.speed+kirby2.speed)/2),int((kirby1.vision+kirby2.vision)/2))

    def evolution(self):
        self.selection()
        bestKirby = self.kirbyGeneration[0]
        print(bestKirby)
        self.history.append([self.gen, bestKirby.size, bestKirby.speed, bestKirby.vision, bestKirby.timeAlive])
        
        for i in range(1,int(len(self.kirbyGeneration))-1):
            newKirby = self.reproduction(bestKirby,self.kirbyGeneration[i])
            newKirby.mutate()
            self.kirbyGeneration[i] = newKirby
        self.gen += 1

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.generationRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    self.fps += 10
                if event.key == pygame.K_j:
                    self.fps -= 10
                

    def initKirbys(self):
        listPos = [(100,100),(300,100),(500,100),(700,100),(100,300),(700,300),(100,500),(300,500),(500,500),(700,500)]
        random.shuffle(listPos)
        listVel = [(1,0),(-1,0),(1,1),(-1,1),(-1,-1),(1,-1),(0,1),(0,-1)]
        for i in range(0,9):
            self.kirbyGeneration[i].pos = pygame.Vector2(listPos[i])
            self.kirbyGeneration[i].vel = pygame.Vector2(listVel[random.randint(0,len(listVel)-1)])
            self.kirbyGeneration[i].timeAlive = 0
            self.kirbys.append(self.kirbyGeneration[i])

    def initSpikes(self):
        listPos = [(200,200),(400,200),(600,200),(200,400),(600,400),(200,600),(400,600),(600,600),(400,400),(500,300)]
        random.shuffle(listPos)
        listVel = [(1,0),(-1,0),(1,1),(-1,1),(-1,-1),(1,-1),(0,1),(0,-1)]
        self.spikes = []
        for i in range(0,10):
            spike = self.generateSpikes()
            spike.pos = pygame.Vector2(listPos[i])
            spike.vel = pygame.Vector2(listVel[random.randint(0,len(listVel)-1)])
            self.spikes.append(spike)
    def update(self):
        for spike in self.spikes:
            spike.update(self.size)

        # Collision entre dots
        for i in range(len(self.spikes)):
            for j in range(i + 1, len(self.spikes)):
                a = self.spikes[i]
                b = self.spikes[j]
                if a.collide_with(b):
                    a.bounce_with(b)

        for kirby in self.kirbys:
            for spike in self.spikes:
                if kirby.collide_with(spike):
                    self.kirbys.remove(kirby)
                    break
                kirby.escape(spike)

            for otherKirby in self.kirbys:
                if kirby!=otherKirby and kirby.collide_with(otherKirby):
                    kirby.bounce_with(otherKirby)

            kirby.update(self.size)

    def render(self):
        self.window.fill((255, 255, 255))
        
        for spike in self.spikes:
            pygame.draw.rect(self.window, spike.color, spike.surface)
        for kirby in self.kirbys:
            pygame.draw.rect(self.window,kirby.color,kirby.surface)
        
        pygame.display.update()

    def generationRun(self):
        while self.generationRunning:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(self.fps)
            if len(self.kirbys)==0 :
                self.generationRunning = False

    def run(self):
        for i in range(0,10):
            self.kirbyGeneration.append(self.generateRandomKirby())
        for i in range(0,10):
            self.spikes.append(self.generateSpikes())
        i = 0
        while self.running:
            self.generationRunning = True
            self.initKirbys()
            self.initSpikes()
            print("Generation %s" % i)
            i += 1
            self.generationRun()
            self.evolution()
            

sim = Simulation()
sim.run()
np.save("history.npy", sim.history)
pygame.quit()   

