from context import src # This allows for aunt/uncle imports 

import numpy as np
from src.model.model import RubiksModel
from src.rubiks.cube import Cube
from src.ui.display_tools import display_console
from src.model.data_handler import parse_training

def benchmark_data(file, stateOrCube):
    x = parse_training(file)
    y = [[],[]]

    for i in range(len(x)):
        if stateOrCube == 1:
            y[0].append(Cube(x[i][0]))
        else:
            y[0].append(x[i][0])
        y[1].append(x[i][1].count(" ")+1)

    return y

benchmark_data("training0.txt", 1)
