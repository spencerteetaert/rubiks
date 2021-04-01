import copy
import torch
from ..rubiks.cube import Cube
from .model import RubiksModel
import time
from heapq import heapify, heappush, heappop


class Node:
	
	total_nodes = 0
	
	def __init__(self, cube, model):
		"""
		
		cube: a Cube object defined in cube.py (Holds numpy state that is useful to our model)
		model: a RubiksModel object, used for ranking how close this cube is to being solved
		
		Later things to add:
			- a pointer to his parent node, use to reconstruct the path of moves taken
			
		"""
		self.moves = model([cube.state])[0][0].item() # the number of moves until the cube is solved
		self.model = model
		self.cube = copy.copy(cube)
		self.parent = None
		self.id = Node.total_nodes
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
		return self.moves < other.moves

	def __hash__(self):
		h = 0
		p = 1
		for row in self.cube.state:
			for x in row:
				h += p * x
				p *= 7 
		return h

	def get_next_states(self):
		"""
		from a given state, generate and return all possible next states from here
		returns a list of "Node" objects to be processed by "SearchEngine"
		"""
		
		neighbours = []
		# old_state = copy.copy(self.cube.state)
		for direction in {"L", "R", "U", "D", "B", "F"}:
			for modifier in {"", "'", "2"}:
				cube_copy = Cube(self.cube.state)
				cube_copy.rotate(direction + modifier)
				neighbours.append( Node(cube_copy, self.model) )
		
		return neighbours

# potential searching algorithms named here
BEST_FIRST = "BEST_FIRST"

class SearchEngine:
	
	def __init__(self, model):
		
		self.set_algo(BEST_FIRST)
	
	def set_algo(self, algo_name):
		"""
		Define the searching algorithm to use when searching
		Default = BEST_FIRST
		
		algo_name must be in { BEST_FIRST } (add more when needed)
		"""
		
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
		MAX_MOVES = 20
		MAX_TIME = 10
		
		# define a queue of possible states to explore
		# most searching algorithms use some sort of queue to explore states
		queue = []
		# queue.append(starting_node)
		heapify(queue)
		heappush(queue, starting_node)
		
		# map of state -> number of moves needed to get here
		distance = {} 
		distance[starting_node] = 0
		
		start_time = time.time()
		dd = -1
		while queue and time.time() - start_time < MAX_TIME:

			cur_node = heappop(queue)
			# cur_node = queue.pop(0)
			if distance[cur_node] > dd:
				dd = distance[cur_node]
				print("Current Search depth: {}".format(dd))
			
			if cur_node == finish_node:
				# do some more printing / generate path of moves here
				print("Successfully solved the cube in {} moves :)".format(distance[cur_node]))
				moves = []
				
				while cur_node is not None:
					moves.append(cur_node)
					cur_node = cur_node.parent
				
		
				moves.reverse()
				
				for node in moves:
					print(node.cube)
					
					print("")
				
				return moves

			next_states = cur_node.get_next_states()
			
			# right now, default and only algorithm is best-first, 
			# so we go to the best options first
			next_states.sort()
			
			next_states = next_states[:3]
			
			for next_node in next_states:
				next_node_dist = distance[next_node] if next_node in distance else float('inf')
				if distance[cur_node] + 1 < next_node_dist:
					distance[next_node] = distance[cur_node] + 1
					# next_node.moves += 0.6 * cur_node.moves
					next_node.moves += 0.5 * distance[next_node]
					next_node.set_parent(cur_node) # for retracing the path of moves performed
					heappush(queue, next_node)
					# queue.append(next_node)
		print("Unable to solve cube in {} seconds :(".format(MAX_TIME))
		# maybe add some printing here to see what the starting state was / throw an error
		
		return None
