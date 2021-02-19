''' 
File for data handling functions. Read/write/conversions
'''
import numpy as np
import sys

def one_hot(color):
	'''
	color: a single chacter that is in "roywbg"
	
	returns: 1 x 6 numpy array that encodes the color depending on its position in the string above
	'''
	COLOR_ORDER = "roywbg" # see parse_training
	assert color in COLOR_ORDER
	return np.array([int(c == color) for c in COLOR_ORDER])

def make_state(cube):
	'''
	cube: a one-dimensional array of letters representing the colors on a rubiks cube
	      face ordering is that of "parse_training" (see below), with each 9 consecutive letters representing a face
	      
	returns: 3 x 18 x 6 numpy array representing the cube state
	         the cube is "flattened" so that all faces are arranged horizontally from left to right (6 3 x 3 faces)
	         with the 3rd dimension being a one-hot encoding for the color (100000 = red, 010000 = orange, etc ...)
	         
	'''
	assert len(cube) == 9*6
	ret = np.empty([3, 18, 6])
	for face in range(6):
		for row in range(3):
			for col in range(3):
				ret[row,face*3+col] = one_hot(cube.pop(0))
		
	return ret

def parse_training(filename):
	'''
	filename: a string for imput data file, in the form of "training<dataset number>.txt"
			  for now, filename must be an abosolute path for the file
	
			  face ordering of cubes is  ["L", "R", "U", "D", "B", "F"] 
			  color ordering of cubes is ["r", "o", "y", "w", "b", "g"] (yellow face on top, red to the left)
	
	returns: list of pairs (numpy array for cube_state, raw string of moves performed to solve)
		     cube state is a 3 x 18 x 6 numpy array using one-hot encoding (see make_state)
	
	'''
	ret = []
	try:
		training = open(filename)
		while True:
			cube = training.readline()[:-1].split()
			moves = training.readline()[:-1]
			if not moves: break # EOF
			
			# print(' '.join(cube[i+4] for i in range(0, 9*6, 9))) # prints the colors on the faces [r, o, y, w, b, g]
			
			ret.append( (make_state(cube), moves) )
			
		print("all good {}".format(filename))
		
	except FileNotFoundError:
		print("training data file: {} not found".format(filename))	
	
	return ret

def main():
	for dataset_num in range(10):
		parse_training("../../dataset/training{}.txt".format(dataset_num))

if __name__ == "__main__":
	main()
