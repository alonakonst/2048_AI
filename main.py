import pygame

pygame.init()

#initial setup: screen size, game caption, predetermined speed, font size
screen_width = 300
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60

font_name = 'freesansbold.ttf'
font_size = 24
font = pygame.font.Font(font_name, font_size)

#2048 game colour library (taking from this tutorial: https://www.youtube.com/watch?v=rp9s1O3iSEQ)
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

#initialization of board values, which is a 2D array:
board_values = [[0 for b_v in range(4)] for b_v in range(4)]


#draw background for the board
def draw_board():
    pygame.draw.rect(screen,colors['bg'],[0,screen_height*0.25,screen_width,screen_height*0.75],0,10)

#draw current pieces on the board
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j*70+20,i*70+20+(screen_height*0.25),56.25,56.25],0,5)

# Main loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()


pygame.quit()

