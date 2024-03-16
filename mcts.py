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
        ucb_value = child.heuristic_score+(exploration_term+exploitation_term)
        print('child heuristic score:', child.heuristic_score, 'exploitation:', exploitation_term, 'visit:', child.visits)

        if ucb_value > best_ucb_value:
            best_ucb_value = ucb_value
            best_action = child

    return best_action


def apply_move(board, node, score):
    if type(node)==list:
        board.board_values = node
    else:
        board.board_values = node.state

    board.score = score

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

                child = Node(board_copy.board_values, parent=node, score = node.score, heuristic_score=node.heuristic_score)
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
        move = random.choice(board_copy.generate_move_options_user())
        board_copy = apply_move(board_copy, move[0], move[1])
        reward = calculate_reward(board_copy)
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


def initial_children_rewards(node, board_copy):

    for move, score_num in board_copy.generate_move_options_user():
        move = Node(move, parent=node, score=score_num)
        node.add_child(move)

    for child in node.children:
        child.reward = simulate(child, board_copy)
        child.visits += 1
        node.visits += 1


def heuristic(child_state, score, board_score):
    heuristic_score = 0

    w = [[16, 15, 14,13],
         [9, 10, 11, 12],
         [8, 7, 6, 5],
         [1, 2, 3, 4]]

    eval = 0

    for i in range(4):
        for j in range(4):
            eval += w[i][j] * child_state[i][j]


    heuristic_score += eval*(1+score-board_score)

    return heuristic_score




def calculate_heuristics_scores(node, board):

    for child in node.children:
        child.heuristic_score = heuristic(child.state, child.score, board.score)


def mcts_search(root_node, num_iterations, board):
    board_copy = copy.deepcopy(board)
    initial_children_rewards(root_node, board_copy)
    calculate_heuristics_scores(root_node, board_copy)

    for _ in range(num_iterations):

        node = root_node

        #strategy to get to a leaf of the tree
        while node.children:

            node = select_action(node)
            board_copy = apply_move(board_copy, node, node.score)

                #Expansion phase: Expand the selected node if it's not a terminal state and not fully expanded
                #It is a chance turn
        if not node.is_terminal(board_copy) and not node.is_fully_expanded(board_copy):
            node=expand_node(node, board_copy)
            board_copy = apply_move(board_copy, node, node.score)

        reward = simulate(node, board_copy)
                    # Backpropagation phase: Update statistics of nodes back to the root
        backpropagate(node, reward)
          # Select the best action based on visit counts or other criteria

    best_action = select_action(root_node)


    return best_action