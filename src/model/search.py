import copy
import torch
from ..rubiks.cube import Cube
from .model import RubiksModel
import time
from heapq import heapify, heappush, heappop

possible_rotations_inverse = {'L':'L\'','R':'R\'','B':'B\'','F':'F\'','U':'U\'','D':'D\'', \
    'L\'':'L','R\'':'R','B\'':'B','F\'':'F','U\'':'U','D\'':'D', \
        'L2':'L2','R2':'R2','B2':'B2','F2':'F2','U2':'U2','D2':'D2'}

class Node:
	
	total_nodes = 0
	rotations = ["L", "R", "U", "D", "B", "F", "L'", "R'", "U'", "D'", "B'", "F'", "L2", "R2", "U2", "D2", "B2", "F2"]
	
	def __init__(self, cube, model, moves=-1, transition_turn=""):
		"""
		
		cube: a Cube object defined in cube.py (Holds numpy state that is useful to our model)
		model: a RubiksModel object, used for ranking how close this cube is to being solved
		
		Later things to add:
			- a pointer to his parent node, use to reconstruct the path of moves taken
			
		"""
		if moves == -1:
			self.moves = model([cube.state])[0][0]#.item() # the number of moves until the cube is solved
		else:
			self.moves = moves
		self.model = model
		self.cube = cube#copy.copy(cube)
		self.parent = None
		self.id = Node.total_nodes
		self.transition_turn = transition_turn
		Node.total_nodes += 1
	
	def set_parent(self, parent):
		self.parent = parent
	
	def __eq__(self, other):
		""""
		Define == operator to help check if we've reached the final state when searching
		"""
		return (self.cube.state == other.cube.state).all()
	
	def __lt__(self, other):
		"""
		You need to define < on Node to use priority queues for Dijkstra / A* searching
		"""
		# return self.moves < other.moves
		return torch.lt(self.moves, other.moves)

	def __hash__(self):
		return (tuple(self.cube.state[0]), tuple(self.cube.state[1]), tuple(self.cube.state[2])).__hash__()

	def get_next_states(self):
		"""
		from a given state, generate and return all possible next states from here
		returns a list of "Node" objects to be processed by "SearchEngine"
		"""
		
		neighbours = []
		cubes = []
		states = []
		# old_state = copy.copy(self.cube.state)
		for rotation in Node.rotations:
			cube_copy = Cube(self.cube.state)
			cube_copy.rotate(rotation)
			cubes.append(cube_copy)
			states.append(cube_copy.state)
		moves = self.model(torch.tensor(states).long())
		for i in range(18):
			neighbours.append( Node(cubes[i], self.model, moves[i], Node.rotations[i]) )
		return neighbours

	def find_transition_turn(self, other_node):
		for rotation in Node.rotations:
			c = Cube(self.cube.state)
			c.rotate(rotation)
			if c == other_node.cube:
				return rotation
		return ""

# potential searching algorithms named here
BEST_FIRST = "BEST_FIRST"

class SearchEngine:
	
	close_nodes = torch.load("close_nodes")
	
	def __init__(self, model):
		
		self.set_algo(BEST_FIRST)
		self.model = model
	
	def set_algo(self, algo_name):
		"""
		Define the searching algorithm to use when searching
		Default = BEST_FIRST
		
		algo_name must be in { BEST_FIRST } (add more when needed)
		"""
		
	def backtrack(self, node, depth):
		
		if depth == 0:
			return
		
		queue = [(node, depth)]
		
		while queue:
			node, d = queue.pop(0)
			
			if d > 0:		
				neighbours = node.get_next_states()
				for next_node in neighbours:
					next_node.set_parent(node)
					if next_node not in SearchEngine.close_nodes:
						SearchEngine.close_nodes[next_node] = node
						queue.append((next_node, d-1))
		
	def get_close_nodes(self):
		"""
		Generate close_nodes dictionary
		
		Key: Node object
		Value: Next Node object on the path to being solved 
		"""

		SearchEngine.close_nodes = torch.load("close_nodes")
		# SEARCH_DEPTH = 4
		# self.backtrack( Node(Cube(), self.model), SEARCH_DEPTH)

	def search(self, starting_node, finish_node):
		"""
		perform the searching algoritm to solve the cube
		
		starting_node: an object of class "Node" (the initial cube state)
		finish_node:   an object of class "Node" (the final solved cube state)
		
		Prints some error message if a path is not found
		
		returns:
				- A path of Node objects representing the sequence of moves performed to solve the cube
				- returns None if our model was not able to solve the cube in under 'MAX_MOVES' steps
		
		"""
		
		# Define the maximum number of moves allowed when searching
		# This is a performance benchmark that our model must beat
		MAX_MOVES = 25
		MAX_TIME = 30
		
		# define a queue of possible states to explore
		# most searching algorithms use some sort of queue to explore states
		queue = []
		queue.append(starting_node)
		# heapify(queue)
		# heappush(queue, starting_node)
		
		# map of state -> number of moves needed to get here
		distance = {} 
		distance[starting_node] = 0
		
		start_time = time.time()
		while queue and time.time() - start_time < MAX_TIME:

			# cur_node = heappop(queue)
			cur_node = queue.pop(0)
			
			if cur_node in SearchEngine.close_nodes:
				# print("HERE")
				while cur_node != finish_node:
					next_node = SearchEngine.close_nodes[cur_node]#Node( Cube(state=SearchEngine.close_nodes[cur_node].cube.state), self.model)
					next_node.transition_turn = cur_node.find_transition_turn(next_node)
					next_node.set_parent(cur_node)
					distance[next_node] = distance[cur_node] + 1
					cur_node = next_node
			
			if cur_node == finish_node:
				# do some more printing / generate path of moves here
				print("Successfully solved the cube in {} moves :)".format(distance[cur_node]))
				solution_nodes = []
				path = []
				
				while cur_node is not None:
					solution_nodes.append(cur_node)
					path.append(cur_node.transition_turn)
					cur_node = cur_node.parent
				
				solution_nodes.reverse()
				path.reverse()
				
				# for node in solution_nodes:
				# 	print(node.transition_turn)
				# 	print(node.cube)
					
				# 	print("")
				print("Rotations:", path[1:])

				return solution_nodes

			next_states = cur_node.get_next_states()
			
			# right now, default and only algorithm is best-first, 
			# so we go to the best options first
			# next_states.sort()
			
			# next_states = next_states[:2]
			
			for next_node in next_states:
				next_node_dist = distance[next_node] if next_node in distance else float('inf')
				if distance[cur_node] + 1 < next_node_dist:
					distance[next_node] = distance[cur_node] + 1
					next_node.moves += distance[next_node]
					# next_node.moves += 0.5 * distance[next_node]
					if next_node.moves < MAX_MOVES:
						next_node.set_parent(cur_node) # for retracing the path of moves performed
						heappush(queue, next_node)
					# queue.append(next_node)
		print("Unable to solve cube in {} seconds :( - Searched {} nodes".format(MAX_TIME, len(distance)))
		# maybe add some printing here to see what the starting state was / throw an error
		
		return None
