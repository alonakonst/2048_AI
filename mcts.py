import random
import time
import pygame
import copy
from node import Node
import math
from reward import *

def select_action(node):
    best_action = None
    best_ucb_value = float('-inf')

    for child in node.children:
        exploitation_term = child.reward / child.visits if child.visits > 0 else 0
        exploration_term = math.sqrt(2*(math.log(node.visits)) / child.visits) if child.visits > 0 else float('inf')
        ucb_value = exploitation_term +  exploration_term + child.heuristic_score

        if ucb_value > best_ucb_value:
            best_ucb_value = ucb_value
            best_action = child

    return best_action


def apply_move(board, move):
    board.board_values = move

    return board

def expand_node(node, board):
    all_chidren = []
    for row in range(4):
        for col in range(4):
            if board.board_values[row][col] == 0:
                board_copy = copy.deepcopy(board)
                if random.randint(1, 10) == 10:
                    board_copy.board_values[row][col] = 4
                else:
                    board_copy.board_values[row][col] = 2

                child = Node(board_copy.board_values, parent=node)
                all_chidren.append(child)

    random_child = random.choice(all_chidren)

    node.add_child(random_child)
    reward = simulate(random_child, board_copy)

    backpropagate(random_child, reward)

    return random_child


def simulate(node, board):
    board_copy = copy.deepcopy(board)
    reward = 0
    game_state = node.state
    while not board_copy.game_over():
        game_moves = board_copy.generate_move_options_user()
        move = random.choice(game_moves)
        board_copy=apply_move(board_copy, move)
        reward = calculate_reward(board_copy.board_values)
        board_copy.get_new = True

        if board_copy.get_new:
            board_copy.get_new_tiles()
            board_copy.get_new = False
    return reward




def backpropagate(node, reward):
    # Update visit counts and rewards of nodes along the path from the node to the root
    while node is not None:
        node.visits += 1
        node.reward += reward
        node = node.parent

def children_heuristics(node, board_copy):

    for i in board_copy.generate_move_options_user():
        i = Node(i, parent = node)
        node.add_child(i)
    for child in node.children:
        child.heuristic_score = heuristic(child.state)

def initial_children_rewards(node, board_copy):

    for child in node.children:
        child.reward = heuristic(child.state)
        child.visits += 1
        node.visits += 1

def heuristic(board):
    heuristic_score = 0
    #heuristic has 5 components, each has max weight of 10, so max heuristic value is 50

    max_value = 0
    count_of_max = 0
    count_of_2nd_max = 0
    count_of_3rd_max = 0
    count_of_zero = 0

    for row in range(4):
        for col in range(4):
            if board[row][col]==max_value:
                count_of_max += 1
            if board[row][col]>max_value:
                count_of_max = 1
                max_value=board[row][col]
    #first component is max value, closer to 2048 is better
    heuristic_score += max_value/10

    #second component is location of max value, if it is in the corner, heuristic score is plus 10, is it is in outside
    #row or column, it  is 5, otherwise it is 0
    if board[3][3] or board[0][0] or board[0][3] or board[3][0] == max_value:
        heuristic_score += 50

    elif board[1][1] or board[1][2] or board[2][1] or board[2][2] == max_value:
        heuristic_score -= 50

    else: heuristic_score += -25



    #third component is monoticity, increasing and decreasing of outside columns and rows
    monoticity_row_zero = monoticity_calculation(board[0])
    monoticity_row_three = monoticity_calculation(board[3])
    monoticity_col_zero = monoticity_calculation([row[0] for row in board])
    monoticity_col_four = monoticity_calculation([row[3] for row in board])
    heuristic_score += max(monoticity_row_zero, monoticity_row_three, monoticity_col_zero, monoticity_col_four)


    count_of_small = 0
    #fourth component is concentration of second and third best components
    for row in range(4):
        for col in range(4):
            if board[row][col]==max_value/2:
                count_of_2nd_max += 1
            if board[row][col]==max_value/4:
                count_of_3rd_max += 1
            if board[row][col] == 0:
                count_of_zero += 1
            if board[row][col]== 2 or 4 or 8 or 16 or 32:
                count_of_small += 1


        heuristic_score -= count_of_small*5


    heuristic_score = (count_of_2nd_max+count_of_3rd_max)/(17-count_of_zero-count_of_max)*10

    #fifth compont: concentration of zeroes:
    heuristic_score += (count_of_zero/16)*10

    return heuristic_score
def mcts_search(root_node, num_iterations, board):
    board_copy = copy.deepcopy(board)
    children_heuristics(root_node, board_copy)
    initial_children_rewards(root_node, board_copy)

    for _ in range(num_iterations):
        node = root_node

        while not board_copy.game_over:
            #strategy to get to a leaf of the tree
            while node.children:
                node = select_action(node)
                board_copy = apply_move(board_copy, node.state)

            #Expansion phase: Expand the selected node if it's not a terminal state and not fully expanded
            #It is a chance turn
            if not node.is_terminal(board_copy) and not node.is_fully_expanded():
                node=expand_node(node, board_copy)
                board_copy = apply_move(board_copy, node.state)

            reward = simulate(node, board_copy)
            # Backpropagation phase: Update statistics of nodes back to the root
            backpropagate(node, reward)
            # Select the best action based on visit counts or other criteria

    best_action = select_action(root_node)

    board_copy = apply_move(board_copy, best_action.state)

    return board_copy

