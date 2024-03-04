import pygame
import random


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
board_values = [[ 0 for b_v in range(4)] for b_v in range(4)]
get_new = True
game_over = False
init_count = 0
key_direction = ''

def turn_up(board):
    merged = [[False for _ in range(4)] for _ in range(4)]
    for row in range(4):
        for col in range(4):
            shift = 0
            if row > 0:
                #detect how much shift has to happen
                for element in range(row):
                    if board[element][col] == 0:
                        shift += 1
                if shift > 0:
                    board[row - shift][col] = board[row][col]
                    board[row][col] = 0
                if board[row - shift - 1][col] == board[row - shift][col] and not merged[row - shift][col] \
                        and not merged[row - shift - 1][col]:
                    board[row - shift - 1][col] *= 2
                    board[row - shift][col] = 0
                    merged[row - shift - 1][col] = True

    return board

def turn_down(board):
    merged = [[False for _ in range(4)] for _ in range(4)]
    for row in range(3):
        for col in range(4):
            shift = 0
            for element in range(row + 1):
                if board[3 - element][col] == 0:
                    shift += 1
            if shift > 0:
                board[2 - row + shift][col] = board[2 - row][col]
                board[2 - row][col] = 0
            if 3 - row + shift <= 3:
                if board[2 - row + shift][col] == board[3 - row + shift][col] and not merged[3 - row + shift][col] \
                        and not merged[2 - row + shift][col]:
                    board[3 - row + shift][col] *= 2
                    board[2 - row + shift][col] = 0
                    merged[3 - row + shift][col] = True
    return board

def turn_right(board):
   merged = [[False for _ in range(4)] for _ in range(4)]
   for row in range(4):
       for col in range(4):
           shift = 0
           for element in range(col):
               if board[row][3 - element] == 0:
                   shift += 1
           if shift > 0:
               board[row][3 - col + shift] = board[row][3 - col]
               board[row][3 - col] = 0
           if 4 - col + shift <= 3:
               if board[row][4 - col + shift] == board[row][3 - col + shift] and not merged[row][4 - col + shift] \
                       and not merged[row][3 - col + shift]:
                   board[row][4 - col + shift] *= 2
                   board[row][3 - col + shift] = 0
                   merged[row][4 - col + shift] = True
   return board

def turn_left(board):
   merged = [[False for _ in range(4)] for _ in range(4)]
   for row in range(4):
       for col in range(4):
           shift = 0
           for element in range(col):
               if board[row][element] == 0:
                   shift += 1
           if shift > 0:
               board[row][col - shift] = board[row][col]
               board[row][col] = 0
           if board[row][col - shift] == board[row][col - shift - 1] and not merged[row][col - shift - 1] \
                   and not merged[row][col - shift]:
               board[row][col - shift - 1] *= 2
               board[row][col - shift] = 0
               merged[row][col - shift - 1] = True

   return board


#get new pieces randomly. There is 1 out of 10 chance to get 4, otherwise is 2
def get_new_tiles(board):
    empty_cells=[]
    for row in range(4):
        for col in range(4):
            if board[row][col]==0:
                empty_cells.append((row,col))
    random_empty_cell = random.choice(empty_cells)

    if len(empty_cells)==0:
        game_over=True

    if random.randint(1, 10) == 10:
        board[random_empty_cell[0]][random_empty_cell[1]] = 4
    else:
        board[random_empty_cell[0]][random_empty_cell[1]] = 2
    print(random_empty_cell)
    return board

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
            if value > 0:
                value_len=len(str(value))
                font = pygame.font.Font(font_name, 40-(5*value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center = (j*70+48.125, (screen_height*0.25)+i*70+48.125))
                screen.blit(value_text,text_rect)


# Main loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)

    if get_new or init_count < 2:
        board_values = get_new_tiles(board_values)
        get_new = False
        init_count +=1

    if key_direction == 'UP':
        board_values = turn_up(board_values)
        key_direction = ''
        get_new = True

    if key_direction == 'DOWN':
        board_values = turn_down(board_values)
        key_direction = ''
        get_new = True

    if key_direction == 'RIGHT':
        board_values = turn_right(board_values)
        key_direction = ''
        get_new = True

    if key_direction == 'LEFT':
        board_values = turn_left(board_values)
        key_direction = ''
        get_new = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                key_direction = 'UP'
            elif event.key == pygame.K_DOWN:
                key_direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                key_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                key_direction = 'RIGHT'

    pygame.display.flip()


pygame.quit()

