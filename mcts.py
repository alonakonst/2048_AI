n_simulations = 300

def getBoardCopy(board):
    board_copy = [row[:] for row in board]
    return board_copy

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

def simulate(node):
    # Simulate a game from the node's state until the end and return the reward
    pass

def backpropagate(node, reward):
    # Update visit counts and rewards of nodes along the path from the node to the root
    while node is not None:
        node.visit_count += 1
        node.reward += reward
        node = node.parent

def mcts_search(root_node, num_iterations):
    for _ in range(num_iterations):
        node = root_node
        while not is_terminal(node):
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