import random
import time
import pygame
import copy
from node import Node
import math
from reward import *

def select_action(node):
    best_action = None
    best_ucb_value = 0

    for child in node.children:
        exploitation_term = child.reward / child.visits if child.visits > 0 else 0
        exploration_term = math.sqrt(2*(math.log(node.visits)) / child.visits) if child.visits > 0 else float('inf')
        ucb_value = exploitation_term +  exploration_term

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

def initial_children_rewards(node, board_copy):
    rewards = []
    for i in board_copy.generate_move_options_user():
        i = Node(i, parent = node)
        node.add_child(i)
    for child in node.children:
        child.reward = simulate(child, board_copy)
        child.visits += 1
        node.visits += 1


def mcts_search(root_node, num_iterations, board):

    board_copy = copy.deepcopy(board)
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

