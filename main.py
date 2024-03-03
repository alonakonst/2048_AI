import pygame

pygame.init()

screen_width = 300
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))


# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False




pygame.quit()

