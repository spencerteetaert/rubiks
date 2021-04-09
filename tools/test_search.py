from context import src
from src.rubiks.cube import Cube

import time
from src.model.search import SearchEngine
from src.model.search import Node 
import torch

test_set = torch.load("misc/test_set")
model_path = r"misc/EXAMPLEMODEL"
model = torch.load(model_path, map_location=torch.device('cuda'))
model.eval()
engine = SearchEngine(model)

cube_solved = Cube()

s = time.time()
results = []
total_cubes = 0
for i in range(len(test_set)):
    cnt_bad = 0
    print("\nRunning {} cubes that are {} moves scrambled".format(len(test_set[i]), i+1))
    for t in range(len(test_set[i])):
        total_cubes += 1
        # print("\n{}: Trying to solve the following cube:\n".format(t+1))
        # print(cube_start)
        # print("Running search...")
        cube_start = test_set[i][t]
        now = engine.search( Node(cube_start, model), Node(cube_solved, model) )
        if now is None:
            cnt_bad += 1
    results.append(len(test_set[i]) - cnt_bad)
        
e = time.time()

print("Test completed in {:.3}s".format(e-s))
print("Sucess Rate = {}/{}".format(sum(results), total_cubes))
