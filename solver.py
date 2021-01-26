from abc import ABC, abstractmethod


class Solver(ABC):
    solution = None
    frontier = None
    nodes_expanded = 0
    max_depth = 0
    explored_nodes = set()
    initial_state = None

    def __init__(self, initial_state):
        self.initial_state = initial_state

    def ancestral_chain(self):
        current = self.solution
        chain = [current]
        while current.parent is not None:
            chain.append(current.parent)
            current = current.parent
        return chain

    @property
    def path(self):
        path = [node.operator for node in self.ancestral_chain()[-2::-1]]
        return path

    @abstractmethod
    def solve(self):
        pass

    def set_solution(self, board):
        self.solution = board
        self.nodes_expanded = len(self.explored_nodes) - len(self.frontier) - 1
        # return self.solution
