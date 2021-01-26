from collections import deque

from solver import Solver


class BFS(Solver):
    def __init__(self, initial_state):
        super(BFS, self).__init__(initial_state)
        self.frontier = deque()

    def solve(self):
        self.frontier.append(self.initial_state)
        while self.frontier:
            board = self.frontier.popleft()
            self.explored_nodes.add(tuple(board.state))
            if board.goal_test():
                self.set_solution(board)
                break
            for neighbor in board.neighbors():
                if tuple(neighbor.state) not in self.explored_nodes:
                    self.frontier.append(neighbor)
                    self.explored_nodes.add(tuple(neighbor.state))
                    self.max_depth = max(self.max_depth, neighbor.depth)
        return
