file_name = "cube_class_test"

def run():
    # Test code goes here 
    from src.rubiks.cube import Cube
    import random
    ret = True
    msg = ""

    possible_rotations = ['L','R','B','F','U','D','L\'','R\'','B\'','F\'','U\'','D\'','L2','R2','B2','F2','U2','D2']

    # Test cube initialization
    solved_cube = Cube()
    if solved_cube.solved() != True:
        ret = False
        msg += "ERR: Solved cube not solved.\n"
    
    # Test rotation functionality 
    for rotation in possible_rotations:
        num = 4
        if rotation[-1] == 2:
            num = 2
        for i in range(num):
            solved_cube.rotate(rotation)
        if solved_cube.solved() != True:
            ret = False
            msg += "ERR: Move {} performed {} times did not return cube to solved.\n".format(rotation, num)

    # Test scramble/solvle functionality 
    solved_cube.scramble(20)
    for i in range(20):
        solved_cube.rotate_optimal()
    if solved_cube.solved() != True:
        ret = False
        msg += "ERR: Cube was unsucessfully scrambled and solved.\n"

    # Test scramble/solve functionality with pre-scrambled cube
    _cube = Cube()
    _cube.scramble(20)
    new_cube = Cube(_cube.get_state(), _cube.optimal_path)
    moves = new_cube.optimal_path
    while len(moves) > 0:
        new_cube.rotate(moves.pop(0))
    if new_cube.solved() != True:
        ret = False
        msg += "ERR: Cube initialized with random state, was unsuccessfully solved.\n"

    return ret, msg

if __name__=="__tests__."+file_name:
    print("Testing {}.py...".format(file_name))
    ret, msg = run()
    if ret:
        print("{}.py successful.\n".format(file_name))
    else:
        print("ERR: {}.py failed.\n{}".format(file_name, msg))