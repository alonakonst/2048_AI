import pygame
import random
from mcts import *
from node import Node
from board import Board

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


board = Board()

#define a button
button = pygame.Rect(10, 10, 200, 50)
def draw_button():
    button_font = pygame.font.Font(font_name, 12)
    button_color_default = board.colors['bg']
    button_color_pressed = board.colors[0]
    button_pressed = False
    button_color = button_color_pressed if button_pressed else button_color_default
    pygame.draw.rect(screen, button_color, button, border_radius=10)
    button_text = button_font.render('Press for AI to play', True, (255, 255, 255))  # Render the text
    text_rect = button_text.get_rect(center=(110, 35))  # Position the text in the center of the button
    screen.blit(button_text, text_rect)  # Draw the text on th


# Main loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    board.draw_board(screen,screen_width,screen_height)
    board.draw_pieces(board.board_values,font_name,screen,screen_height)


    if board.get_new or board.init_count < 2:
        board_values = board.get_new_tiles()
        board.get_new = False
        board.init_count +=1

    if board.board_is_full():
        print('its full, you lost')
        run = False

    if board.winning_condition():
        print('you won')
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                board_temp = tuple(map(tuple, board.board_values))  # Convert to tuple for comparison
                board_values = board.turn_up(board.board_values)
                key_direction = ''
                if tuple(map(tuple, board_values)) != board_temp:  # Compare tuples instead of lists
                    board.get_new = True

            if event.key == pygame.K_DOWN:
                board_temp = tuple(map(tuple, board.board_values))
                board_values = board.turn_down(board.board_values)
                key_direction = ''
                if tuple(map(tuple, board_values)) != board_temp:  # Compare tuples instead of lists
                    board.get_new = True


            elif event.key == pygame.K_LEFT:
                board_temp = tuple(map(tuple, board.board_values))  # Convert to tuple for comparison
                board_values = board.turn_left(board.board_values)
                key_direction = ''
                if tuple(map(tuple, board_values)) != board_temp:  # Compare tuples instead of lists
                    board.get_new = True


            elif event.key == pygame.K_RIGHT:
                board_temp = tuple(map(tuple, board.board_values))  # Convert to tuple for comparison
                board_values = board.turn_right(board.board_values)
                key_direction = ''
                if tuple(map(tuple, board_values)) != board_temp:  # Compare tuples instead of lists
                    board.get_new = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if button.collidepoint(event.pos):  # Check if the mouse click is within the button
                    button_pressed = True
                    #mcts_search(1, 2)
                    current_node = Node(board_values)
                    print(current_node.state)
                    current_node.children = board.create_children_set()
                    print(current_node.children)
                    print(getBoardCopy(board_values))

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                button_pressed = False

    draw_button()

    pygame.display.flip()


pygame.quit()

