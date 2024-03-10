import pygame
import random


class Board:
    def __init__(self):
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]
        self.get_new = True
        self.game_over = False
        self.init_count = 0
        self.key_direction = ''

        # 2048 game colour library (taking from this tutorial: https://www.youtube.com/watch?v=rp9s1O3iSEQ)
        self.colors = {0: (204, 192, 179),
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

    def turn_up(self,board_values):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for row in range(4):
            for col in range(4):
                shift = 0
                if row > 0:
                    # detect how much shift has to happen
                    for element in range(row):
                        if board_values[element][col] == 0:
                            shift += 1
                    if shift > 0:
                        board_values[row - shift][col] = board_values[row][col]
                        board_values[row][col] = 0
                    if board_values[row - shift - 1][col] == board_values[row - shift][col] and not merged[row - shift][col] \
                            and not merged[row - shift - 1][col]:
                        board_values[row - shift - 1][col] *= 2
                        board_values[row - shift][col] = 0
                        merged[row - shift - 1][col] = True

        return board_values

    def turn_down(self,board_values):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for row in range(3):
            for col in range(4):
                shift = 0
                for element in range(row + 1):
                    if board_values[3 - element][col] == 0:
                        shift += 1
                if shift > 0:
                    board_values[2 - row + shift][col] = board_values[2 - row][col]
                    board_values[2 - row][col] = 0
                if 3 - row + shift <= 3:
                    if board_values[2 - row + shift][col] == board_values[3 - row + shift][col] and not merged[3 - row + shift][col] \
                            and not merged[2 - row + shift][col]:
                        board_values[3 - row + shift][col] *= 2
                        board_values[2 - row + shift][col] = 0
                        merged[3 - row + shift][col] = True
        return board_values

    def turn_right(self, board_values):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for row in range(4):
            for col in range(4):
                shift = 0
                for element in range(col):
                    if board_values[row][3 - element] == 0:
                        shift += 1
                if shift > 0:
                    board_values[row][3 - col + shift] = board_values[row][3 - col]
                    board_values[row][3 - col] = 0
                if 4 - col + shift <= 3:
                    if board_values[row][4 - col + shift] == board_values[row][3 - col + shift] and not merged[row][4 - col + shift] \
                            and not merged[row][3 - col + shift]:
                        board_values[row][4 - col + shift] *= 2
                        board_values[row][3 - col + shift] = 0
                        merged[row][4 - col + shift] = True
        return board_values

    def turn_left(self, board_values):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for row in range(4):
            for col in range(4):
                shift = 0
                for element in range(col):
                    if board_values[row][element] == 0:
                        shift += 1
                if shift > 0:
                    board_values[row][col - shift] = board_values[row][col]
                    board_values[row][col] = 0
                if board_values[row][col - shift] == board_values[row][col - shift - 1] and not merged[row][col - shift - 1] \
                        and not merged[row][col - shift]:
                    board_values[row][col - shift - 1] *= 2
                    board_values[row][col - shift] = 0
                    merged[row][col - shift - 1] = True

        return board_values

    # get new pieces randomly. There is 1 out of 10 chance to get 4, otherwise is 2
    def get_new_tiles(self):
        empty_cells = []
        for row in range(4):
            for col in range(4):
                if self.board_values[row][col] == 0:
                    empty_cells.append((row, col))
        random_empty_cell = random.choice(empty_cells)

        if len(empty_cells) == 0:
            self.game_over = True

        if random.randint(1, 10) == 10:
            self.board_values[random_empty_cell[0]][random_empty_cell[1]] = 4
        else:
            self.board_values[random_empty_cell[0]][random_empty_cell[1]] = 2
        return self.board_values

    # draw background for the board
    def draw_board(self, screen, screen_width, screen_height):
        pygame.draw.rect(screen, self.colors['bg'], [0, screen_height * 0.25, screen_width, screen_height * 0.75], 0, 10)

    # draw current pieces on the board
    def draw_pieces(self,board,font_name,screen,screen_height):
        for i in range(4):
            for j in range(4):
                value = board[i][j]
                if value > 8:
                    value_color = self.colors['light text']
                else:
                    value_color = self.colors['dark text']
                if value <= 2048:
                    color = self.colors[value]
                else:
                    color = self.colors['other']
                pygame.draw.rect(screen, color, [j * 70 + 20, i * 70 + 20 + (screen_height * 0.25), 56.25, 56.25], 0, 5)
                if value > 0:
                    value_len = len(str(value))
                    font = pygame.font.Font(font_name, 40 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * 70 + 48.125, (screen_height * 0.25) + i * 70 + 48.125))
                    screen.blit(value_text, text_rect)

    def create_children_set(self):
        # Create copies of the current board state
        board_values_up = [row[:] for row in self.board_values]
        board_values_down = [row[:] for row in self.board_values]
        board_values_right = [row[:] for row in self.board_values]
        board_values_left = [row[:] for row in self.board_values]

        # Create a list of resulting states
        current_children = [self.turn_up(board_values_up),
                            self.turn_down(board_values_down),
                            self.turn_right(board_values_right),
                            self.turn_left(board_values_left)]

        return current_children

    def board_is_full(self):
        for row in range(4):
            for col in range(4):
                if self.board_values[row][col] == 0:
                    return False

        for element in self.create_children_set():
            if element != self.create_children_set()[0]:
                return False

        return True
    def winning_condition(self):
        for row in range(4):
            for col in range(4):
                if self.board_values[row][col] == 2048:
                    return True
        return False