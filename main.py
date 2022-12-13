import pygame
import random
import sys
from pygame.math import Vector2  # um nicht immer pygame.math zu schreiben


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # startgrösse
        self.direction = Vector2(1, 0)
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
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')  # mit diesem code wird der Sound importiert

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):  # alle blocke im schlangenkörper schauen auch die davor und hinter
            x_pos = int(block.x * cell_size)  # Positionierung Blöcke
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:  # schauen auf vorherigen und nächsten block und wie sie in relation sind
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):  # ein vektor vom anderen subtrahieren um relation herausfinden
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:  # wenn wahr dann block hinzufügen
            body_copy = self.body[:]  # copy von schlange
            body_copy.insert(0, body_copy[0] + self.direction)  # richtung des ersten elements der liste
            self.body = body_copy[:]
            self.new_block = False  # damit sich schlange unendlich verlängert
        else:
            body_copy = self.body[:-1]  # copy von schlange, letztes item entfernt
            body_copy.insert(0, body_copy[0] + self.direction)  # richtung des ersten elements der liste
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

class FRUIT:  # Frucht erstellen
    def __init__(self):  # x und y position erstellen
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)  # viereck erstellen (x,y,w,h)
        screen.blit(apple, fruit_rect)

    # pygame.draw.rect(screen,(126,166,114),fruit_rect) # viereck zeichnen (öberfläche, farbe, viereck) # man braucht jetzt rec nicht mehr

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)  # damit frucht random spawned
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)  # x und y in vektor für übersicht


class MAIN:
    def __init__(self):
        self.snake = SNAKE()  # wenn class main gemacht wird werden auch class snake und class fruit gemacht
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:  # wenn frucht = auf schlangenkopf
            self.fruit.randomize()  # fruch umpositionieren
            self.snake.add_block()  # block an schlange hinzufügen
            self.snake.play_crunch_sound() # sobald schlangenkopf stelle mit object berührt = sound

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:  # schauen ob schlange aus map, 0 ist kopf
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:  # wenn schlangenkopf körper berührt
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (160, 220, 50)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:  # jede zweite reihe
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:  # jede zweite reihe
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))  # damit apfel nebem score angezeigt wird
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width, apple_rect.height)  # Zahl zu nah am Rahmen nach score_rect.width eig. + zahl (funktioniert nicht)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)  # Rahmen

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 38
cell_number = 19
screen = pygame.display.set_mode((cell_number * cell_size,
                                  cell_number * cell_size))  # Breite und Höhe (400x400 pixel) (display surface) gibt nur eins
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple-min.png').convert_alpha()  # Apfel der in Dateien gespeichert ist soll eigefügt werden
game_font = pygame.font.Font(None, 30)  # TTF file herunterladen oder None schreiben (30=grösse)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # alle 150 millisek. wird timer ausgelöst

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # sichergehen dass code geschlossen wird
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:  # triger für tastatur
            if event.key == pygame.K_UP:  # pfeil oben
                if main_game.snake.direction.y != 1:  # solange nicht nach unten beewegen
                    main_game.snake.direction = Vector2(0, -1)  # pfeil oben = hoch
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((150, 200, 0))  # Farbe
    main_game.draw_elements()
    pygame.display.update()  # in dieser while loop alle unsere Elemente Zeichnen
    clock.tick(60)  # wie schnell die while loop pro Sekunde max rennen kann (max 60 frames pro Sekunde)

