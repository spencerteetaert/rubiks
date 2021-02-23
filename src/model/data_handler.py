''' 
File for data handling functions. Read/write/conversions
'''
import numpy as np


def num_one_hot(number):
    """ Return the one hot encoding of an integer value that represents a color block on the cube

    Args:
        number: an integer from 0 to 5, representing a color

    Returns:
        result: a 1x6 numpy array that is a one hot encoding for the number
    """
    assert number in range(6)
    result = np.zeros(6)
    result[number] = 1
    return result

def parse_file(filename):
    """ Return a list representing the parsed states and moves in the filename

    Args:
        filename: a string representing the path of the target file, with file naming
                  convention "trainingseq<dataset number>.txt"

                  The file contains alternative lines of current states and next moves,
                  with the cube side sequence of ["L", "U", "F", "D", "R", "B"] for the states

    Returns:
        parsed_list: a list of tuples, each containing a pair of state and next move. The state is
                     represented by a 3x18x6 numpy array, where the 3x18 is the flattened view of all
                     blocks, and each block has a one hot encoding with dimension 6. The move is
                     represented by a string.
    """
    parsed_list = []
    with open(filename, 'r') as file:
        while True:
            state = file.readline().split()
            move = file.readline().strip()
            if not move:
                break

            assert len(state) == 3 * 18
            state_array = np.empty([3, 18, 6])
            for i in range(len(state)):
                if (i % 9) in range(3):
                    state_array[0, (i // 9) * 3 + (i % 9)] = num_one_hot(int(state[i]))
                if (i % 9) in range(3, 6):
                    state_array[1, (i // 9) * 3 + (i % 9 - 3)] = num_one_hot(int(state[i]))
                if (i % 9) in range(6, 9):
                    state_array[2, (i // 9) * 3 + (i % 9 - 6)] = num_one_hot(int(state[i]))

            parsed_list.append((state_array, move))

    return parsed_list

def main():
    file_path = ".../rubiks/dataset/trainingseq0.txt"
    result = parse_file(file_path)