

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0
        self.heuristic_score = 0

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def is_terminal(self, board):
        if board.board_is_full():
            return True

        if board.winning_condition():
            return True
        return False

    def is_fully_expanded(self):
        if len(self.children)==4:
            return True
        return False
    def initial_children_rewards(self, board_copy):
        rewards = []
        for i in board_copy.generate_move_options():
            i = Node(i, parent = self)
            self.add_child(i)
        for child in self.children:
            child.reward = simulate(child, board_copy)
            print(child.reward)