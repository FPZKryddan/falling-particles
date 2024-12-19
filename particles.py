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
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

class Void(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)

class Sand(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (194,178,128)
        self.static = False
        self.solid = True
        self.rand_color(1)

    def rand_color(self, offset):
        colors = [(246,215,176), (242,210,169), (236,204,162), (231,196,150), (225,191,146)]
        self.color = random.choice(colors)
        
    def set_color(self, color):
        self.color = color

    def update(self, world, newWorld, x, y):
        cols = len(world)
        rows = len(world[0])
        if y == rows - 1: # if at bottom
            s = Sand(x, y)
            s.set_color(self.color)
            newWorld[x][y] = s
            return newWorld
        
        belowParticle = world[x][y+1]
        belowParticleNew = newWorld[x][y+1]

        if isinstance(belowParticle, Void):
            newWorld[x][y+1] = Sand(x, y+1)
        elif belowParticle.isSolid():
            s = Sand(x, y)
            s.set_color(self.color)

            left = x-1 > 0 and isinstance(world[x-1][y], Void)
            right = x+1 < cols - 1 and isinstance(world[x+1][y], Void)
            down_left = left and isinstance(world[x-1][y+1], Void)
            down_right = right and isinstance(world[x+1][y+1], Void)
            if down_left or down_right:
                if down_left and down_left:
                    spread = random.choice([(x-1, y+1), (x+1, y+1)])
                    _x, _y = spread
                    s.set_position(_x, _y)
                    newWorld[_x][_y] = s
                elif down_left:
                    s.set_position(x-1, y+1)
                    newWorld[x-1][y+1] = s
                elif down_right:
                    s.set_position(x+1, y+1)
                    newWorld[x+1][y+1] = s
                return newWorld
            newWorld[x][y] = s
        elif isinstance(belowParticle, Water) and isinstance(belowParticleNew, Water):
            newWorld[x][y+1] = Sand(x, y+1)
            newWorld[x][y] = Water(x, y)
            pass
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
        if y == rows - 1: 
            newWorld[x][y] = Water(x, y)
            return newWorld
        
        belowParticle = world[x][y+1]
        belowParticleNew = newWorld[x][y+1]

        if isinstance(belowParticle, Void):
            newWorld[x][y+1] = Water(x, y+1)
            return newWorld
        
        if isinstance(belowParticle, Water) and isinstance(belowParticleNew, Void):
            newWorld[x][y+1] = Water(x, y+1)
            return newWorld

        if belowParticle.isSolid():
            left = x-1 > 0 and isinstance(world[x-1][y], Void)
            right = x+1 < cols - 1 and isinstance(world[x+1][y], Void)
            down_left = left and isinstance(world[x-1][y+1], Void)
            down_right = right and isinstance(world[x+1][y+1], Void)
            if down_left or down_right:
                if down_left and down_left:
                    spread = random.choice([(x-1, y+1), (x+1, y+1)])
                    _x, _y = spread
                    newWorld[_x][_y] = Water(_x, _y)
                elif down_left:
                    newWorld[x-1][y+1] = Water(x-1, y+1)
                elif down_right:
                    newWorld[x+1][y+1] = Water(x+1, y+1)
                return newWorld
            else:
                if left and right:
                    spread = random.choice([(x-1, y), (x+1, y)])
                    _x, _y = spread
                    newWorld[_x][_y] = Water(_x, _y)
                elif left:
                    newWorld[x-1][y] = Water(x-1, y)
                elif right:
                    newWorld[x+1][y] = Water(x+1, y)
                return newWorld
        newWorld[x][y] = Water(x,y)
        return newWorld
    