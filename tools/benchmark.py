from context import src # This allows for aunt/uncle imports 
from src.rubiks.cube import Cube
from src.model.data_handler import parse_training

def benchmark_data(file, stateOrCube, n=30):
    x = parse_training(file)
    y = [[],[]]

    for i in range(min(n, len(x))):
        if stateOrCube == 1:
            y[0].append(Cube(x[i][0]))
        else:
            y[0].append(x[i][0])
        y[1].append(x[i][1].count(" ")+1)

    return y

benchmark_data("misc/training0.txt", 1)
