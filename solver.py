import sys
import resource
import numpy as np
from collections import deque
import heapq


class Board:
	parent = None
	state = None
	operator = None
	depth = 0
	zero = None
	cost = 0

	def __init__(self, state, parent = None, operator = None, depth = 0):
		self.parent = parent
		self.state = np.array(state)
		self.operator =  operator
		self.depth = depth
		self.zero = self.find_0()
		self.cost = self.depth + self.manhattan()
	
	def __lt__(self, other):
		if self.cost != other.cost:
			return self.cost < other.cost
		else:
			op_pr = {'Up': 0, 'Down': 1, 'Left': 2, 'Right': 3}
			return op_pr[self.operator] < op_pr[other.operator]

	def __str__(self):
		return str(self.state[:3]) + '\n' \
				+ str(self.state[3:6]) + '\n' \
				+ str(self.state[6:]) + ' ' + str(self.depth) + str(self.operator) + '\n' 

	def goal_test(self):
		if np.array_equal(self.state, np.arange(9)):
			return True
		else:
			return False

	def find_0(self):
		for i in range(9):
			if self.state[i] == 0:
				return i

	def manhattan(self):
		state = self.index(self.state)
		goal = self.index(np.arange(9))
		return sum((abs(state // 3 - goal // 3) + abs(state % 3 - goal % 3))[1:])

	def index(self, state):
	    index = np.array(range(9))
	    for x, y in enumerate(state):
	        index[y] = x
	    return index

	def swap(self, i, j):
		new_state = np.array(self.state)
		new_state[i], new_state[j] = new_state[j], new_state[i]
		return new_state

	def up(self):
		if self.zero > 2:
			return Board(self.swap(self.zero, self.zero - 3), self, 'Up', self.depth + 1)
		else:
			return None	

	def down(self):
		if self.zero < 6:
			return Board(self.swap(self.zero, self.zero + 3), self, 'Down', self.depth + 1)
		else:
			return None

	def left(self):
		if self.zero % 3 != 0:
			return Board(self.swap(self.zero, self.zero - 1), self, 'Left', self.depth + 1)
		else:
			return None

	def right(self):
		if (self.zero + 1) % 3 != 0:
			return Board(self.swap(self.zero, self.zero + 1), self, 'Right', self.depth + 1)
		else:
			return None

	def neighbors(self):
		neighbors = []
		neighbors.append(self.up())
		neighbors.append(self.down())
		neighbors.append(self.left())
		neighbors.append(self.right())
		return list(filter(None, neighbors))

	__repr__ = __str__


class Solver:
	soln = None
	path = None
	nodes_expanded = 0
	max_depth = 0

	def ancestral_chain(self):
		current = self.soln
		chain = [current]
		while current.parent != None:
			chain.append(current.parent)
			current = current.parent
		return chain

	def path(self):
		path = [node.operator for node in self.ancestral_chain()[-2::-1]]
		return path

	def bfs(self, state):
		frontier = deque()
		frontier.append(state)
		froxplored = set()
		while frontier:
			board = frontier.popleft()
			froxplored.add(tuple(board.state))
			if board.goal_test():
				self.soln = board
				self.path = self.path()
				self.nodes_expanded = len(froxplored)-len(frontier)-1
				return self.soln
			for neighbor in board.neighbors():
				if tuple(neighbor.state) not in froxplored:
					frontier.append(neighbor)
					froxplored.add(tuple(neighbor.state))
					self.max_depth = max(self.max_depth, neighbor.depth)
		return None

	def dfs(self, state):
		frontier = []
		frontier.append(state)
		froxplored = set()
		while frontier:
			board = frontier.pop()
			froxplored.add(tuple(board.state))
			if board.goal_test():
				self.soln = board
				self.path = self.path()
				self.nodes_expanded = len(froxplored)-len(frontier)-1
				return self.soln
			for neighbor in board.neighbors()[::-1]:
				if tuple(neighbor.state) not in froxplored:
					frontier.append(neighbor)
					froxplored.add(tuple(neighbor.state))
					self.max_depth = max(self.max_depth, neighbor.depth)
		return None

	def ast(self, state):
		frontier = []
		heapq.heappush(frontier, state)
		froxplored = set()
		while frontier:
			board = heapq.heappop(frontier)
			froxplored.add(tuple(board.state))
			if board.goal_test():
				self.soln = board
				self.path = self.path()
				self.nodes_expanded = len(froxplored)-len(frontier)-1
				return self.soln
			for neighbor in board.neighbors():
				if tuple(neighbor.state) not in froxplored:
					heapq.heappush(frontier, neighbor)
					froxplored.add(tuple(neighbor.state))
					self.max_depth = max(self.max_depth, neighbor.depth)
		return None

def main():

	p = Board(np.array(eval(sys.argv[2])))
	s = Solver()
	if sys.argv[1] == 'bfs':
		soln = s.bfs(p)
	elif sys.argv[1] == 'dfs':
		soln = s.dfs(p)
	elif sys.argv[1] == 'ast':
		soln = s.ast(p)
	file = open('output.txt', 'w')

	file.write('path_to_goal: ' + str(s.path) + '\n')
	file.write('cost_of_path: ' + str(len(s.path)) + '\n')
	file.write('nodes_expanded: ' + str(s.nodes_expanded) + '\n')
	file.write('search_depth: ' + str(soln.depth) + '\n')
	file.write('max_search_depth: ' + str(s.max_depth) + '\n')
	file.write('running_time: ' + str(resource.getrusage(resource.RUSAGE_SELF).ru_utime + \
							resource.getrusage(resource.RUSAGE_SELF).ru_stime) + '\n')
	file.write('max_ram_usage: ' + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))

	file.close()

if __name__ == "__main__":
	main()