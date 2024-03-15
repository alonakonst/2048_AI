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
        ucb_value = (exploitation_term + exploration_term)*child.heuristic_score if child.heuristic_score>0 else (exploitation_term + exploration_term)

        if ucb_value > best_ucb_value:
            best_ucb_value = ucb_value
            print('best ucb value:', best_ucb_value)
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

                child = Node(board_copy.board_values, parent=node, score = node.score)
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
        board_copy=apply_move(board_copy, move[0], move[1])
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


def heuristic(board, score, board_score):
    heuristic_score = 0
    heuristic_score += score-board_score
    #heuristic has 5 components, each has max weight of 10, so max heuristic value is 50

    #print('heuristic score:', heuristic_score)
    max_value = 0
    count_of_max = 0
    count_of_2nd_max = 0
    count_of_3rd_max = 0
    count_of_zero = 0

    '''
    for row in range(4):
        for col in range(4):
            if board[row][col]==max_value:
                count_of_max += 1
            if board[row][col]>max_value:
                count_of_max = 1
                max_value=board[row][col]
    #first component is max value, closer to 2048 is better
    heuristic_score += max_value/10
    '''

    #second component is location of max value, if it is in the corner, heuristic score is plus 10, is it is in outside
    #row or column, it  is 5, otherwise it is 0
    #if board[3][3] or board[0][0] or board[0][3] or board[3][0] == max_value:
     #   heuristic_score +=

    #elif board[1][1] or board[1][2] or board[2][1] or board[2][2] == max_value:
     #   heuristic_score -=

    #else: heuristic_score += -25

    #heuristic_score += math.sqrt(score)




    count_of_small = 0
    #fourth component is concentration of second and third best components



    #heuristic_score = (count_of_2nd_max+count_of_3rd_max)/(17-count_of_zero-count_of_max)*10

    #fifth compont: concentration of zeroes:
    #heuristic_score += (count_of_zero/16)*10

    heuristic_score += snake_monoticity(board)

    return heuristic_score

def snake_monoticity(board):
    monoticity_count = 0
    monoticity_scores = [list_moniticity(board[3],False),
                         list_moniticity(board[2], True),
                         list_moniticity(board[1], False),
                         list_moniticity(board[0], True),

                         list_moniticity([row[0] for row in board],False),
                         list_moniticity([row[1] for row in board], True),
                         list_moniticity([row[2] for row in board], False),
                         list_moniticity([row[3] for row in board], True)]


    for i in monoticity_scores:
        if i == True:
            monoticity_count += 1

    #print('monoticity count:', monoticity_count)

    return monoticity_count*10

def calculate_heuristics_scores(node, board):

    for child in node.children:
        child.heuristic_score = heuristic(child.state, child.score, board.score)


def mcts_search(root_node, num_iterations, board):
    if root_node.is_terminal(board):
        return board

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

                if not node.is_terminal(board_copy):

                    reward = simulate(node, board_copy)
                    # Backpropagation phase: Update statistics of nodes back to the root

                    backpropagate(node, reward)
                    # Select the best action based on visit counts or other criteria

    best_action = select_action(root_node)

    board = apply_move(board_copy, best_action, best_action.score)

    board.score = best_action.score

    print('Current score of the board: ', board.score)

    return board

