'''
Example test file. When you add new features, write a test file here to ensure
that other people don't accidentally break it. Each feature should have its
own test file for traceability purposes. 
'''
file_name = "cube_class_test"

def run():
    # Test code goes here 
    from src.rubiks.cube import Cube
    import random
    ret = True
    msg = ""

    possible_rotations = ['L','R','B','F','U','D','L\'','R\'','B\'','F\'','U\'','D\'','L2','R2','B2','F2','U2','D2']
    possible_rotations_inverse = {'L':'L\'','R':'R\'','B':'B\'','F':'F\'','U':'U\'','D':'D\'', \
    'L\'':'L','R\'':'R','B\'':'B','F\'':'F','U\'':'U','D\'':'D', \
        'L2':'L2','R2':'R2','B2':'B2','F2':'F2','U2':'U2','D2':'D2'}

    solved_cube = Cube()
    if solved_cube.solved() != True:
        ret = False
        msg += "ERR: Solved cube not solved.\n"
    
    for rotation in possible_rotations:
        num = 4
        if rotation[-1] == 2:
            num = 2
        for i in range(num):
            solved_cube.rotate(rotation)
        if solved_cube.solved() != True:
            ret = False
            msg += "ERR: Move {} performed {} times did not return cube to solved.\n".format(rotation, num)

    solved_cube.scramble(20)
    for i in range(20):
        solved_cube.rotate_optimal()
    if solved_cube.solved() != True:
        ret = False
        msg += "ERR: Cube was unsucessfully scrambled and solved.\n"

    return ret, msg

if __name__=="__tests__."+file_name:
    print("Testing {}.py...".format(file_name))
    ret, msg = run()
    if ret:
        print("{}.py successful.\n".format(file_name))
    else:
        print("ERR: {}.py failed.\n{}".format(file_name, msg))