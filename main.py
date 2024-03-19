from mcts import *
from node import Node
from board import Board

clock = pygame.time.Clock()
pygame.init()

#initial setup: screen size, game caption, predetermined speed, font
screen_width = 300
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60

font_name = 'freesansbold.ttf'
font_size = 24
font = pygame.font.Font(font_name, font_size)

#Initializing a board and root node of the game which state is identical to initial board values.
board = Board()
time = 2 #this is a variable for controlling display speed of AI solution below

ai_play = False

# Main loop of the game
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    board.draw_board(screen,screen_width,screen_height)
    board.draw_pieces(board.board_values,font_name,screen,screen_height)

    if board.init_count==2:
        node = Node(board.board_values, score=board.score) #initializing root node of the game when first two tiles are added to the board
        board.init_count +=1

    #getting new tiles(relevan only for when user plays a game)
    if board.get_new or board.init_count < 2:
        board_values = board.get_new_tiles()
        board.get_new = False
        board.init_count +=1

    #quitting main loop if the board is full
    if board.board_is_full():
        max_value = 0
        for row in range(4):
            for col in range(4):
                if board.board_values[row][col] > max_value:
                    max_value = board.board_values[row][col]

        print("Game final score:", board.score)
        print("Max value:", max_value)
        run = False

    #event handeling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                board_temp = tuple(map(tuple, board.board_values))
                board_values = board.turn_up(board.board_values)
                key_direction = ''
                if tuple(map(tuple, board_values)) != board_temp:
                    board.get_new = True

            if event.key == pygame.K_DOWN:
                board_temp = tuple(map(tuple, board.board_values))
                board_values = board.turn_down(board.board_values)
                key_direction = ''
                if tuple(map(tuple, board_values)) != board_temp:
                    board.get_new = True

            elif event.key == pygame.K_LEFT:
                board_temp = tuple(map(tuple, board.board_values))
                board_values = board.turn_left(board.board_values)
                key_direction = ''
                if tuple(map(tuple, board_values)) != board_temp:
                    board.get_new = True


            elif event.key == pygame.K_RIGHT:
                board_temp = tuple(map(tuple, board.board_values))
                board_values = board.turn_right(board.board_values)
                key_direction = ''
                if tuple(map(tuple, board_values)) != board_temp:
                    board.get_new = True



    ai_play = True # comment out if you want to play the game yourself using arrow keys

    # This block is responsible for calling monte carlo tree search.
    if ai_play:
        dt = clock.tick(60) / 1000
        time -= dt
        if time <= 0:
            time = 0.2
            node = mcts_search(node, 1, board) #change second parameter to chose number of simulations
            board = apply_move(board, node, node.score)
            board.get_new = True
            if board.get_new:
                board.get_new_tiles()
                board.get_new = False


    pygame.display.flip()



pygame.quit()
