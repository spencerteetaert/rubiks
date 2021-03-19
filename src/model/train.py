import torch
from random import shuffle
import numpy as np

def get_datset(num_data, batch_size):
    '''
    Args:
        num_data: the number of data in the dataset to be built. Note the number will not be exactly num_data to ensure
                even division among the possible values of n.
        batch_size: the desired batch size for the dataset

    Returns:
        batched_set: list[tuple(tensor, tensor)]
                    a list of tuples representing the batches. The first tensor of each tuple represents the
                    input with shape torch.Size([batch_size, 3, 18]), and the second tensor represent labels with
                    shape torch.Size([batch_size]).
    '''
    lower_n = 5  # to be set later
    every_n = num_data // (21 - lower_n)
    dataset = []
    for i in range(lower_n, 21):
        for j in range(every_n):
            random_cube = Cube()
            random_cube.scramble(num_moves=i)
            dataset.append((random_cube.state, i))

    shuffle(dataset)
    batched_set = []
    index = 0
    while index < len(dataset):
        if (index+batch_size) >= len(dataset):
            end = len(dataset)
        else:
            end = index+batch_size

        batch_array = np.zeros((end-index, 3, 18), dtype=int)
        batch_label = np.zeros(end-index, dtype=int)

        for i in range(index, end):
            batch_array[i-index] = dataset[i][0]
            batch_label[i-index] = dataset[i][1]
        index += batch_size
        batched_set.append((torch.from_numpy(batch_array), torch.from_numpy(batch_label)))
    return batched_set
