''' 
File for data handling functions. Read/write/conversions
'''
import numpy as np

def parse_training(filename):
    '''
    filename: a string for imput data file, in the form of "training<dataset number>.txt"
              for now, filename must be an abosolute path for the file
    
              face ordering of cubes is  ["L", "R", "U", "D", "B", "F"] 
              color ordering of cubes is ["r", "o", "y", "w", "b", "g"] (yellow face on top, red to the left)
    
    returns: list of pairs (numpy array for cube_state, raw string of moves performed to solve)
             cube state is a 3 x 18 numpy array using one-hot encoding (see make_state)
    
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

def parse_trainingseq(filename):
    """ Return a list representing the parsed states and moves in the filename

    Args:
        filename: a string representing the path of the target file, with file naming
                  convention "trainingseq<dataset number>.txt"

                  The file contains alternative lines of current states and next moves,
                  with the cube side sequence of ["L", "U", "F", "D", "R", "B"] for the states

    Returns:
        parsed_list: a list of tuples, each containing a pair of state and next move. The state is
                     represented by a 3x18 numpy array, where the 3x18 is the flattened view of all
                     blocks. The move is represented by a string.
    """
    parsed_list = []
    mapping = {"r":0, "o":1, "y":2, "w":3, "b": 4, "g": 5}
    TEMPCOUNTER = 0
    with open(filename, 'r') as file:
        while True:
            state = file.readline().split()
            move = file.readline().strip()
            if not move:
                break

            assert len(state) == 3 * 18
            state_array = np.empty([3, 18])

            for i in range(len(state)):
                if (i % 9) in range(3):
                    state_array[0, (i // 9) * 3 + (i % 9)] = int(state[i])
                if (i % 9) in range(3, 6):
                    state_array[1, (i // 9) * 3 + (i % 9 - 3)] = int(state[i])
                if (i % 9) in range(6, 9):
                    state_array[2, (i // 9) * 3 + (i % 9 - 6)] = int(state[i])

            parsed_list.append((state_array, move))
            TEMPCOUNTER += 1
            if TEMPCOUNTER == 1000:
                break

    return parsed_list

import sys

def make_state(cube):
    '''
    cube: a one-dimensional array of letters representing the colors on a rubiks cube
          face ordering is that of "parse_training" (see below), with each 9 consecutive letters representing a face
          
    returns: 3 x 18 numpy array representing the cube state
             the cube is "flattened" so that all faces are arranged horizontally from left to right (6 3 x 3 faces)
             
    '''
    mapping = {"r":0, "o":1, "y":2, "w":3, "b": 4, "g": 5}
    # ident = np.eye(6)
    assert len(cube) == 9*6
    COLOR_ORDER = "roywbg" # see parse_training
    ret = np.empty([3, 18])
    for face in range(6):
        for row in range(3):
            for col in range(3):
                ret[row,face*3+col] = mapping[cube.pop(0)] # ident[mapping[cube.pop(0)]]
        
    return ret

def main():
    for dataset_num in range(10):
        parse_training("../../dataset/training{}.txt".format(dataset_num))

if __name__ == "__main__":
    main()