
class Node:
    def __init__(self, state):
        self.state = state  # Game state (2D array)
        self.visit_count = 0
        self.reward = 0
        self.children = {}  # Map of actions to child nodes


