import pygame
import math
from particles import *

pygame.init()
pygame.font.init()

# screen
WIDTH, HEIGHT = 1000, 1000
OFFSET_X, OFFSET_Y = 200, 0
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH + OFFSET_X, HEIGHT + OFFSET_Y
ZOOM = 10
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption("Falling particles")
        

class Simulation():
    def __init__(self):
        self.cols = int(WIDTH / ZOOM)
        self.rows = int(HEIGHT / ZOOM)
        self.world = self.init_world()
        self.place_mode = "Sand"
        self.place_callback = self.place_sand
        self.brush_size = 1
        self.mouse_x = 0
        self.mouse_y = 0

    def init_world(self):
        world = [[Void(_x, _y) for _x in range(self.cols)] for _y in range(self.rows)]
        return world

    def updateWorld(self):
        newWorld = [[Void(_x, _y) for _x in range(self.cols)] for _y in range(self.rows)]
        for x in reversed(range(self.cols)):
            for y in reversed(range(self.rows)):
                particle = self.world[x][y]
                if not isinstance(particle, Void):
                    newWorld = particle.update(self.world, newWorld, x, y)
        return newWorld

    def draw_world(self):
        canvas.fill((0, 0, 0))  
        for x in range(self.cols ):
            for y in range(self.rows):
                particle = self.world[x][y]
                if not isinstance(particle, Void):
                    particle.draw(canvas, ZOOM)

    def draw_ui(self):
        pygame.draw.rect(screen, (255,255,255), (0+OFFSET_X-1, 0-1, WIDTH+1, HEIGHT+1), 1)
        pygame.draw.circle(screen, (255,255,255), (self.mouse_x, self.mouse_y), (self.brush_size // 2) * ZOOM, 1)
        font = pygame.font.Font(pygame.font.match_font('arial'), 32)
        text = font.render(self.place_mode, True, (255,255,255))
        toggle_info_text = font.render("RMB(SWAP)", True, (255,255,255))
        brush_size_text = font.render(f"Brush: {self.brush_size}", True, (255,255,255))
        screen.blit(text, (25,25))
        screen.blit(toggle_info_text, (25,75))
        screen.blit(brush_size_text, (25,135))

    def place_water(self, x, y):
        self.world[x][y] = Water(x,y)

    def place_sand(self, x, y):
        self.world[x][y] = Sand(x, y)
        
    def place(self, x, y):
        if self.brush_size == 1:
            self.place_callback(x, y)
            return
        center = (x,y)
        radius = math.ceil(self.brush_size / 2)
        for _x in range(center[0]-radius, center[0]+radius):
            for _y in range(center[1]-radius, center[1]+radius):
                distance_squared = (_x - center[0]) ** 2 + (_y - center[1]) ** 2
                if distance_squared <= radius ** 2:
                    if _x <= self.cols - 1 and _x >= 0:
                        if _y <= self.rows - 1 and _y >= 0:
                            self.place_callback(_x, _y)

    def on_mouse_down(self, mouse_pos, code):
        x, y = mouse_pos
        x -= OFFSET_X
        y -= OFFSET_Y
        x = x // ZOOM
        y = y // ZOOM
        if x < self.cols and x >= 0:
            if y < self.rows and y >= 0:
                self.place(x, y)

    def toggle_place_mode(self):
        if self.place_mode == "Sand":
            self.place_mode = "Water"
            self.place_callback = self.place_water
        else:
            self.place_mode = "Sand"
            self.place_callback = self.place_sand

    def alter_brush_size(self, direction):
        self.brush_size += direction
        if self.brush_size < 1:
            self.brush_size = 1

    def clear_world(self):
        self.world = self.init_world()

    def start_simulation(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.toggle_place_mode()
                if event.type == pygame.MOUSEWHEEL:
                    self.alter_brush_size(event.y)
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_x, self.mouse_y = event.pos
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.clear_world()


                    
            if pygame.mouse.get_pressed()[0]:
                self.on_mouse_down(pygame.mouse.get_pos(), 0)


            screen.fill((0,0,0))
            self.world = self.updateWorld()
            self.draw_world()
            screen.blit(canvas, (OFFSET_X, OFFSET_Y))
            self.draw_ui()
            pygame.display.flip()
            clock.tick(60)


if __name__ == '__main__':
    sim = Simulation()
    sim.start_simulation()
    pygame.quit()