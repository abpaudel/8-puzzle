import heapq

from solver import Solver


class AStar(Solver):
    def __init__(self, initial_state):
        super(AStar, self).__init__(initial_state)
        self.frontier = []

    def solve(self):
        heapq.heappush(self.frontier, self.initial_state)
        while self.frontier:
            board = heapq.heappop(self.frontier)
            self.explored_nodes.add(tuple(board.state))
            if board.goal_test():
                self.set_solution(board)
                break
            for neighbor in board.neighbors():
                if tuple(neighbor.state) not in self.explored_nodes:
                    heapq.heappush(self.frontier, neighbor)
                    self.explored_nodes.add(tuple(neighbor.state))
                    self.max_depth = max(self.max_depth, neighbor.depth)
        return
