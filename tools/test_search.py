from context import src
from src.rubiks.cube import Cube

import time
from src.model.search import SearchEngine
from src.model.search import Node 
import torch

test_set = torch.load("test_set")
model = torch.load(r"D:\Unversity of Toronto\Courses\Year 3\APS360 (Applied Fundamentals of Machine Learning)\Project\results\Models\RubiksModel004", map_location=torch.device('cuda'))
model.eval()
engine = SearchEngine(model)

cube_solved = Cube()

s = time.time()
results = []
for i in range(len(test_set)):
    cnt_bad = 0
    print("\nRunning {} cubes that are {} moves scrambled".format(len(test_set[i]), i+1))
    for t in range(len(test_set[i])):
        # print("\n{}: Trying to solve the following cube:\n".format(t+1))
        # print(cube_start)
        # print("Running search...")
        cube_start = test_set[i][t]
        now = engine.search( Node(cube_start, model), Node(cube_solved, model) )
        if now is None:
            cnt_bad += 1
    results.append(len(test_set[i]) - cnt_bad)
    print(results)
        
e = time.time()

print("took: {}".format(e-s))
print("Times we failed = {}/{}".format(cnt_bad, T))
