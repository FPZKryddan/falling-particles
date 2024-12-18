import pygame
import random

class Particle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0,0,0)
        self.static = True
        self.solid = False

    def draw(self, screen, scale):
        pygame.draw.rect(screen, self.color, (self.x*scale, self.y*scale, scale, scale))

    def __str__(self):
        return f"PARTICLE"
    
    def isStatic(self):
        return self.static

    def isSolid(self):
        return self.solid
    
    def isFalling(self):
        return self.falling

class Void(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)

class Sand(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (194,178,128)
        self.static = False
        self.solid = True

    def update(self, world, newWorld, x, y):
        rows = len(world[0])
        if y == rows - 1: # if at bottom
            newWorld[x][y] = Sand(x, y)
            return newWorld
        
        belowParticle = world[x][y+1]

        if isinstance(belowParticle, Void):
            newWorld[x][y+1] = Sand(x, y+1)
        elif belowParticle.isSolid():
            newWorld[x][y] = Sand(x, y)
        elif isinstance(belowParticle, Water):
            newWorld[x][y+1] = Sand(x, y+1)
            newWorld[x][y] = Water(x, y)
        return newWorld

class Water(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0,0,255)
        self.static = False
        self.solid = False

    def update(self, world, newWorld, x, y):
        cols = len(world)
        rows = len(world[0])
        if y == rows - 1: # if at bottom
            newWorld[x][y] = Water(x, y)
            return newWorld
        
        belowParticle = world[x][y+1]

        #if on void
        if isinstance(belowParticle, Void):
            newWorld[x][y+1] = Water(x, y+1)
            return newWorld

        # if on solid
        if belowParticle.isSolid():
            # no collisions
            left = x-1 > 0 and isinstance(world[x-1][y], Void)
            right = x+1 < cols - 1 and isinstance(world[x+1][y], Void)
            down_left = left and isinstance(world[x-1][y+1], Void)
            down_right = right and isinstance(world[x+1][y+1], Void)
            # if on hill spread randomly
            if down_left or down_right:
                if down_left and down_left:
                    spread = random.choice([(x-1, y+1), (x+1, y+1)])
                    _x, _y = spread
                    newWorld[_x][_y] = Water(_x, _y)
                elif down_left:
                    newWorld[x-1][y+1] = Water(x-1, y+1)
                elif down_right:
                    newWorld[x+1][y+1] = Water(x+1, y+1)
        newWorld[x][y] = Water(x,y)
        return newWorld
    