import os
file_name = os.path.basename(__file__)[:-3]

def run():
    # Test code goes here 
    from src.model.model import RubiksModel
    import random
    import numpy as np
    import torch
    ret = True
    msg = ""

    # Ensure model initialization 
    try:
        model = RubiksModel()
    except:
        msg += "ERR: Model unable to be initialized.\n"
        return ret, msg

    # Ensure forward pass
    state = np.array([[random.randint(0, 5) for i in range(6)] * 3,\
        [random.randint(0, 5) for i in range(6)] * 3,\
            [random.randint(0, 5) for i in range(6)] * 3], dtype=int)
    state = torch.unsqueeze(torch.tensor(state), 0)
    try:
        ret = model(state)
        expected = torch.random([1, 21])
        flag = 1/torch.all(ret.shape == expected.shape)
    except:
        msg += "ERR: Forward pass failed.\n"

    return ret, msg

if __name__=="__tests__."+file_name:
    print("Testing {}.py...".format(file_name))
    ret, msg = run()
    if ret:
        print("{}.py successful.\n".format(file_name))
    else:
        print("ERR: {}.py failed.\n{}".format(file_name, msg))