import random
import time
import pygame


clock = pygame.time.Clock()
def getBoardCopy(cls,board):
    board_copy = [row[:] for row in board]
    print(board_copy)
    return board_copy


def evaluate_states(cls, children_states):
    score = 0
    scores=[]
    move = children_states[0]
    for i in children_states:
        score_i=0
        for row in range(4):
            for col in range(4):
                if i[row][col] > score:
                    score_i = i[row][col]
                    if score_i > score:
                        score=score_i
                        move = i


def perform_action(state, action):
    # Apply action to the game state and return the new state
    # Example: move tiles in the specified direction
    new_state = state.copy()  # Make a copy of the state
    # Apply the action to new_state
    return new_state

def select_action(node):
    # Use selection strategy (e.g., UCB1) to select an action from the node's children
    pass

def expand_node(node):
    # Expand the node by adding child nodes for all possible actions
    for action in legal_actions(node.state):
        child_state = perform_action(node.state, action)
        node.children[action] = Node(child_state)


def apply_move(board, move):
    board.board_values = move

    return board.board_values


def simulate(node, board):
    reward = 0
    game_state = node.state


    while not board.game_over():
        game_moves = board.create_children_set()
        move = random.choice(game_moves)
        apply_move(board, move)
        print(board.board_values)
        board.get_new = True
        if board.get_new:
            board.get_new_tiles()
            board.get_new = False

    print('last one', board.board_values)
    '''
    # Evaluate the final state
    if has_won(game_state, node.player):
        reward = 1  # Player wins
    elif has_won(game_state, get_opponent(node.player)):
        reward = -1  # Opponent wins
    else:
        reward = 0  # Draw
    
    '''
    return reward


def backpropagate(node, reward):
    # Update visit counts and rewards of nodes along the path from the node to the root
    while node is not None:
        node.visit_count += 1
        node.reward += reward
        node = node.parent

def mcts_search(root_node,board,num_iterations):
    for _ in range(num_iterations):
        node = root_node
        node.children = board.create_children_set()
        if not board.board_is_full():
            print(node.children)
        if node.children:
            print('there are')


'''
def mcts_search(root_node, num_iterations):
    for _ in range(num_iterations):
        node = root_node
        while not board.board_is_full(node):
            if node.children:
                action = select_action(node)
                node = node.children[action]
            else:
                expand_node(node)
                action = select_action(node)
                node = node.children[action]
        reward = simulate(node)
        backpropagate(node, reward)
    # Select the best action based on visit counts or other criteria
    best_action = select_best_action(root_node)
    print('search completed')
    return best_action
'''
