''' 
File for data handling functions. Read/write/conversions
'''
from datetime import datetime
import time
import tqdm
import random
import copy
import numpy as np
import torch
from ..rubiks.cube import Cube

def parse_training(filename):
    '''
    filename: a string for input data file, in the form of "training<dataset number>.txt"
              for now, filename must be an absolute path for the file
    
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

def generate_dataset(num_data):
    '''
    Args:
        num_data: the number of data in the dataset to be built. Note the number will not be exactly num_data to ensure
                even division among the possible values of n.

    Returns:
        dataset: torch.utils.data.TensorDataset object containing num_data samples.
    '''
    lower_n = 5  # to be set later
    every_n = num_data // (21 - lower_n)
    data = []
    labels = []
    for i in range(lower_n, 21):
        for j in range(every_n):
            random_cube = Cube()
            random_cube.scramble(num_moves=i)
            labels.append(i)
            data.append(random_cube.get_state())

    data = torch.tensor(data)
    labels = torch.tensor(labels)
    dataset = torch.utils.data.TensorDataset(data.long(), labels)

    return dataset

def save_datasets(filepath, num_train, num_valid)
    training_set = generate_data(num_train)
    valid_set = generate_data(num_valid)

    print("Exporting data...")
    now = datetime.now()
    curr_time = now.strftime("%d%m%Y_%H%M%S")
    data_name = filepath + "generated_dataset_" + curr_time
    torch.save((training_set, valid_set), data_name)
    print("Data exported.")

def load_datasets(filepath):
    s = time.time()
    (training_set, valid_set) = torch.load(filepath)
    print("Datasets loaded in {:.2}s".format(time.time() - s))
    return training_set, valid_set


def main():
    for dataset_num in range(10):
        parse_training("../../dataset/training{}.txt".format(dataset_num))

if __name__ == "__main__":
    main()
