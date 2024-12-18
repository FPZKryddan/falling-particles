import pygame
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

    def init_world(self):
        world = [[Void(_x, _y) for _x in range(self.cols)] for _y in range(self.rows)]
        return world

    def updateWorld(self):
        newWorld = [[Void(_x, _y) for _x in range(self.cols)] for _y in range(self.rows)]
        for x in range(self.cols):
            for y in range(self.rows):
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
        font = pygame.font.Font(pygame.font.match_font('arial'), 32)
        text = font.render(self.place_mode, True, (255,255,255))
        toggle_info_text = font.render("RMB(SWAP)", True, (255,255,255))
        screen.blit(text, (25,25))
        screen.blit(toggle_info_text, (25,75))

    def place_water(self, x, y):
        self.world[x][y] = Water(x,y)

    def place_sand(self, x, y):
        print(x,y)
        self.world[x][y] = Sand(x,y)

    def on_mouse_down(self, mouse_pos, code):
        x, y = mouse_pos
        x -= OFFSET_X
        y -= OFFSET_Y
        x = x // ZOOM
        y = y // ZOOM
        if x < self.cols and x >= 0:
            if y < self.rows and y >= 0:
                self.place_callback(x, y)

    def toggle_place_mode(self):
        if self.place_mode == "Sand":
            self.place_mode = "Water"
            self.place_callback = self.place_water
        else:
            self.place_mode = "Sand"
            self.place_callback = self.place_sand

    def start_simulation(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.toggle_place_mode()
                    
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