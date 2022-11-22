import pygame,sys,random
from pygame.math import Vector2  # um nicht immer pygame.math zu schreiben

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)] # startgrösse
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):











    def move_snake(self):
        if self.new_block == True: # wenn wahr dann block hinzufügen
            body_copy = self.body[:] # copy von schlange
            body_copy.insert(0,body_copy[0] + self.direction) # richtung des ersten elements der liste
            self.body = body_copy[:]
            self.new_block = False # damit sich schlange unendlich verlängert
        else:
            body_copy = self.body[:-1] # copy von schlange, letztes item entfernt
            body_copy.insert(0,body_copy[0] + self.direction) # richtung des ersten elements der liste
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class FRUIT: # Frucht erstellen
    def __init__(self):  # x und y position erstellen
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size) # viereck erstellen (x,y,w,h)
        screen.blit(apple,fruit_rect)
       # pygame.draw.rect(screen,(126,166,114),fruit_rect) # viereck zeichnen (öberfläche, farbe, viereck) # man braucht jetzt rec nicht mehr

    def randomize(self):
        self.x = random.randint(0,cell_number - 1) # damit frucht random spawned
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y) # x und y in vektor für übersicht

class MAIN:
    def __init__(self):
        self.snake = SNAKE() # wenn class main gemacht wird werden auch class snake und class fruit gemacht
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]: # wenn frucht = auf schlangenkopf
            self.fruit.randomize() # fruch umpositionieren
            self.snake.add_block() # block an schlange hinzufügen

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: # schauen ob schlange aus map, 0 ist kopf
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]: # wenn schlangenkopf körper berührt
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

pygame.init()
cell_size = 40
cell_number = 18
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size)) # Breite und Höhe (400x400 pixel) (display surface) gibt nur eins
clock = pygame.time.Clock()
apple = pygame.image.load('Graphic/apple-min.png').convert_alpha() # Apfel der in Dateien gespeichert ist soll eigefügt werden

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150) # alle 150 millisek. wird timer ausgelöst

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # sichergehen dass code geschlossen wird
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN: # triger für tastatur
            if event.key == pygame.K_UP: # pfeil oben
                if main_game.snake.direction.y != 1: # solange nicht nach unten beewegen
                    main_game.snake.direction = Vector2(0,-1) # pfeil oben = hoch
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)

    screen.fill((150,200,0)) # Farbe
    main_game.draw_elements()
    pygame.display.update() # in dieser while loop alle unsere Elemente Zeichnen
    clock.tick(60) # wie schnell die while loop pro Sekunde max rennen kann (max 60 frames pro Sekunde)
