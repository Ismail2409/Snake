import pygame, sys

pygame.init()
screen = pygame.display.set_mode((400, 500)) # Breite und Höhe
clock = pygame.time.Clock()

while True:
    screen.fill((100,200,50)) #Farbfeld im Hintergund ändern
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # sichergehen dass code geschlossen wird
    pygame.display.update() # in dieser while loop alle unsere Elemente Zeichnen
    clock.tick(60) # wie schnell die while loop pro Sekunde max rennen kann (max 60 frames pro Sekunde)
