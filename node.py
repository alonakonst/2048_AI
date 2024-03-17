'''
Node class contains proprties of particular node and its functions
'''

class Node:
    def __init__(self, state, parent=None, score=0, heuristic_score=0):
        self.state = state #state of the node corresponds with board.board_values
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0 #this score corresponds on a reward based on a simulation
        self.heuristic_score = heuristic_score #this score evaluates node based on current condition
        self.score = score #this score corresponds to current game score

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def is_terminal(self, board):
        if board.board_is_full():
            return True
        return False

    #this function is for the nodes, whose children are 'choice' moves.
    #Therefore, node is fully expanded when it's children amount is equal to amount of zeroes on the board *2
    def is_fully_expanded(self, board):
        choice_children = 0
        for row in range(4):
            for col in range(4):
                if board.board_values[row][col] == 0:
                    choice_children += 2

        if len(self.children) >= choice_children:
                return True

        return False
