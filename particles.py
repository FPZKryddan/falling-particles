import pygame

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
        belowParticle = None
        if y < rows - 1: # check for ground
            belowParticle = world[x][y+1]
        else:
            newWorld[x][y] = Water(x,y)
            return newWorld
            

        # if not isinstance(belowParticle, Void) or y == rows - 1:
        #     if x + 1 < cols - 1:
        #         if isinstance(world[x+1][y+1], Void):
        #             newWorld[x+1][y+1] = Water(x+1, y+1)
        #             return newWorld
        #     if x - 1 >= 0:
        #         if isinstance(world[x-1][y+1], Void):
        #             newWorld[x-1][y+1] = Water(x-1, y+1)
        #             return newWorld

        if isinstance(belowParticle, Void) and y < rows - 1:
            newWorld[x][y+1] = Water(x, y+1)
            return newWorld
        
        newWorld[x][y] = Water(x, y)
        return newWorld