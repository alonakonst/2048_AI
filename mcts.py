import random
import time
import pygame
import copy


def select_action(node):
    best_action = None
    best_ucb_value = float('-inf')

    for child in node.children:
        exploitation_term = child.reward / child.visits if child.visits > 0 else 0
        exploration_term = math.sqrt(math.log(node.visits) / child.visits) if child.visits > 0 else float('inf')
        ucb_value = exploitation_term + exploration_constant * exploration_term

        if ucb_value > best_ucb_value:
            best_ucb_value = ucb_value
            best_action = child

    return best_action


def apply_move(board, move):
    board.board_values = move

    return board.board_values

def expand_node(node):
    # Generate child nodes for possible actions from the current state
    possible_actions = generate_possible_actions(node.state)
    for action in possible_actions:
        new_state = apply_action(node.state, action)  # Apply the action to the current state to obtain the new state
        child_node = Node(new_state, parent=node)    # Create a child node with the new state
        node.children.append(child_node)             # Add the child node to the parent's list of children

def simulate(node, board):
    board_copy = copy.deepcopy(board)
    reward = 0
    game_state = node.state
    while not board_copy.game_over():
        game_moves = board_copy.create_children_set()
        move = random.choice(game_moves)
        apply_move(board_copy, move)
        total_sum = 0
        for row in range(4):
            for col in range(4):
                total_sum += board_copy.board_values[row][col]
                if total_sum>reward:
                    reward=total_sum
        board_copy.get_new = True
        if board_copy.get_new:
            board_copy.get_new_tiles()
            board_copy.get_new = False
    print(reward)
    return reward


def backpropagate(node, reward):
    # Update visit counts and rewards of nodes along the path from the node to the root
    while node is not None:
        node.visit_count += 1
        node.reward += reward
        node = node.parent

    def mcts_search(root_node, num_iterations, board):
        board_copy = copy.deepcopy(board)
        for _ in range(num_iterations):
            node = root_node
            node.children = board_copy.create_children_set()
            # Selection phase: Traverse down the tree until a leaf node is reached
            while node.children:
                # Implement selection strategy (e.g., UCB1)
                node = select_action(node)
            # Expansion phase: Expand the selected node if it's not a terminal state
            if node.children:
                expand_node(node)
            # Simulation phase: Simulate a random game from the selected node
            reward = simulate(node)
            # Backpropagation phase: Update statistics of nodes back to the root
            backpropagate(node, reward)
        # Select the best action based on visit counts or other criteria
        best_action = select_action(root_node)
        print('best_action')
        return best_action

