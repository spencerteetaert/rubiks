'''
File for cube class. Should contain state space and tools for performing rotations, checking solved, etc. 
'''

class Cube:
    def __init__(self):
        pass
    def __repr__(self):
        pass
    
    def solved(self):
        pass
    def scramble(self, num_moves=20):
        pass
    def rotate(self, rotation):
        pass
    
    def set_state(self, new_state):
        self.state = new_state
    def get_state(self):
        return self.state