import pygame,sys,random
from pygame.math import Vector2  # um nicht immer pygame.math zu schreiben

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(6,10),Vector2(7,10)] # startgrösse

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)  # viereck erstellen
            pygame.draw.rect(screen,(183,111,122),block_rect) # viereck zeichnen

class FRUIT: # Frucht erstellen
    def __init__(self):  # x und y position erstellen
        self.x = random.randint(0,cell_number - 1) # damit frucht random spawned
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y) # x und y in vektor für übersicht

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size) # viereck erstellen (x,y,w,h)
        pygame.draw.rect(screen,(126,166,114),fruit_rect) # viereck zeichnen (öberfläche, farbe, viereck)

pygame.init()
cell_size = 40
cell_number = 18
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size)) # Breite und Höhe (400x400 pixel) (display surface) gibt nur eins
clock = pygame.time.Clock()

fruit = FRUIT()
snake = SNAKE()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # sichergehen dass code geschlossen wird

    screen.fill((150,200,0)) # Farbe
    fruit.draw_fruit()
    snake.draw_snake()
    pygame.display.update() # in dieser while loop alle unsere Elemente Zeichnen
    clock.tick(60) # wie schnell die while loop pro Sekunde max rennen kann (max 60 frames pro Sekunde)
