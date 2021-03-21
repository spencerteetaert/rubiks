
class Node:
	
	def __init__(self, moves_til_finish, cube_state):
		"""
		Later things to add:
			- a pointer to his parent node, use to reconstruct the path of moves taken
			
		"""
		self.moves = moves_til_finish
		self.cube_state = cube_state
	
	def __eq__(self, other):
		""""
		Define == operator to help check if we've reached the final state when searching
		"""
		return self.moves == other.moves and self.cube_state == other.cube_state
	
	def __lt__(self, other):
		"""
		You need to define < on Node to use priority queues for Dijkstra / A* searching
		"""
		return self.moves < other.moves

	def get_next_states(self):
		"""
		from a given state, generate and return all possible next states from here
		returns a list of "Node" objects to be processed by "SearchEngine"
		
		TODO: work with the model to generate and rank next states
		"""
		
		return []

# potential searching algorithms named here
BEST_FIRST = "BEST_FIRST"

class SearchEngine:
	
	def __init__(self):
		
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
		
		"""
		
		# Define the maximum number of moves allowed when searching
		# This is a performance benchmark that our model must beat
		MAX_MOVES = 500
		
		# define a queue of possible states to explore
		# most searching algorithms use some sort of queue to explore states
		queue = [starting_node]
		ptr = 0 # where are we in the queue
		
		# map of state -> number of moves needed to get here
		distance = {} 
		distance[cur_node] = 0
		
		while ptr < len(queue):
				
			cur_node = queue[ptr]
			ptr += 1
			
			if cur_node == finish_node:
				print("Successfully solved the cube in {} moves :)".format(distance[cur_node]))
				# do some more printing / generate path of moves here
				return
			
			if distance[cur_node] == MAX_MOVES:
				# we cannot extend this state any more
				continue

			
			next_states = cur_node.get_next_states()
			
			# right now, default and only algorithm is best-first, 
			# so we go to the best options first
			next_states.sort()
			
			for next_node in next_states:
				next_node_dist = distance[next_node] if next_node in distance else float('inf')
				if distance[cur_node] + 1 < next_node_dist:
					distance[next_node] = distance[cur_node] + 1
					queue.append(next_node)
			
		
		print("Unable to solve cube in {} moves :(".format(MAX_MOVES))
		# maybe add some printing here to see what the starting state was / throw an error
		
	
