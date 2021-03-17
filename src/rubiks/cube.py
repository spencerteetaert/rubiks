'''
File for cube class
'''
import copy
import numpy as np
from ..ui.display_tools import display_console

possible_rotations = ['L','R','B','F','U','D','L\'','R\'','B\'','F\'','U\'','D\'','L2','R2','B2','F2','U2','D2']
possible_rotations_inverse = {'L':'L\'','R':'R\'','B':'B\'','F':'F\'','U':'U\'','D':'D\'', \
    'L\'':'L','R\'':'R','B\'':'B','F\'':'F','U\'':'U','D\'':'D', \
        'L2':'L2','R2':'R2','B2':'B2','F2':'F2','U2':'U2','D2':'D2'}

class Cube:
    def __init__(self, state=None, optimal_path=''):
        '''
        state:  3 x 18 numpy array representing the cube state
                the cube is "flattened" so that all faces are arranged horizontally from left to right (6 3 x 3 faces).
                If not specified, cube is initialized in the solved state. 

        optimal_path: string of N moves that lead to an optimal solve 
        '''
        self.initialize_solved()
        if state is None:
            self.state = copy.copy(self.state_solved)
        else:
            self.state = copy.copy(state)
        self.move_index = 0
        self.optimal_path = optimal_path.split(" ")
        
    def __repr__(self):
        print("<cube object>\nCurrent state:")
        print(self.state)
        print("Optimal path:\n" + self.optimal_path.__repr__())
        return ''
    
    def solved(self):
        '''
            Returns True if cube.state is solved
            Returns False else
        '''
        return np.all(self.state == self.state_solved)
    def scramble(self, num_moves=20):
        '''
            Performs num_moves random rotations starting from solved. 
            Saves optimal path
        '''
        self.state = copy.copy(self.state_solved)
        self.optimal_path = []
        self.move_index = 0
        last_rotation = ''
        for i in range(0, num_moves):
            while True:
                rot = np.random.choice(possible_rotations)
                if last_rotation != possible_rotations_inverse[rot]:
                    break
            last_rotation = rot
            self.rotate(rot)
            self.optimal_path = [possible_rotations_inverse[rot]] + self.optimal_path

    def rotate(self, rotation):
        '''
        rotation: a string specifying the rotation to be performed on the cube. 
            Performs the rotation in place on the cube state. 
            Acceptable characters include: LX, RX, UX, DX, BX, FX where X can be either
            nothing, an apostrophe, or the number 2
                
        '''
        clockwise = True
        number = 1
        if rotation[-1] == '\'':
            clockwise = False
        if rotation[-1] == '2':
            number = 2

        if rotation[0] == 'L': # :,0:3
            # Rotate ed tiles
            self.swap_inplace([[0, 3],[0, 6],[0, 9],[2, 17]], clockwise, number)
            self.swap_inplace([[1, 3],[1, 6],[1, 9],[1, 17]], clockwise, number)
            self.swap_inplace([[2, 3],[2, 6],[2, 9],[0, 17]], clockwise, number)
            # Rotate face tiles
            self.swap_inplace([[0, 1],[1, 2],[2, 1],[1, 0]], clockwise, number)
            self.swap_inplace([[0, 0],[0, 2],[2, 2],[2, 0]], clockwise, number)
        elif rotation[0] == 'U': # :,3:6
            # Rotate ed tiles
            self.swap_inplace([[0, 15],[0, 12],[0, 6],[0, 0]], clockwise, number)
            self.swap_inplace([[0, 16],[0, 13],[0, 7],[0, 1]], clockwise, number)
            self.swap_inplace([[0, 17],[0, 14],[0, 8],[0, 2]], clockwise, number)
            # Rotate face tiles
            self.swap_inplace([[1, 5],[2, 4],[1, 3],[0, 4]], clockwise, number)
            self.swap_inplace([[0, 5],[2, 5],[2, 3],[0, 3]], clockwise, number)
        elif rotation[0] == 'F': # :,6:9
            # Rotate ed tiles
            self.swap_inplace([[0, 2],[2, 5],[2, 12],[0, 9]], clockwise, number)
            self.swap_inplace([[1, 2],[2, 4],[1, 12],[0, 10]], clockwise, number)
            self.swap_inplace([[2, 2],[2, 3],[0, 12],[0, 11]], clockwise, number)
            # Rotate face tiles
            self.swap_inplace([[1, 8],[2, 7],[1, 6],[0, 7]], clockwise, number)
            self.swap_inplace([[0, 8],[2, 8],[2, 6],[0, 6]], clockwise, number)
        elif rotation[0] == 'D': # :,9:12
            # Rotate ed tiles
            self.swap_inplace([[2, 6],[2, 12],[2, 15],[2, 0]], clockwise, number)
            self.swap_inplace([[2, 7],[2, 13],[2, 16],[2, 1]], clockwise, number)
            self.swap_inplace([[2, 8],[2, 14],[2, 17],[2, 2]], clockwise, number)
            # Rotate face tiles
            self.swap_inplace([[1, 11],[2, 10],[1, 9],[0, 10]], clockwise, number)
            self.swap_inplace([[0, 11],[2, 11],[2, 9],[0, 9]], clockwise, number)
        elif rotation[0] == 'R': # :,12:15
            # Rotate ed tiles
            self.swap_inplace([[0, 15],[2, 11],[2, 8],[2, 5]], clockwise, number)
            self.swap_inplace([[1, 15],[1, 11],[1, 8],[1, 5]], clockwise, number)
            self.swap_inplace([[2, 15],[0, 11],[0, 8],[0, 5]], clockwise, number)
            # Rotate face tiles
            self.swap_inplace([[1, 14],[2, 13],[1, 12],[0, 13]], clockwise, number)
            self.swap_inplace([[0, 14],[2, 14],[2, 12],[0, 12]], clockwise, number)
        elif rotation[0] == 'B': # :,15:18
            # Rotate ed tiles
            self.swap_inplace([[2, 14],[0, 5],[0, 0],[2, 9]], clockwise, number)
            self.swap_inplace([[1, 14],[0, 4],[1, 0],[2, 10]], clockwise, number)
            self.swap_inplace([[0, 14],[0, 3],[2, 0],[2, 11]], clockwise, number)
            # Rotate face tiles
            self.swap_inplace([[1, 17],[2, 16],[1, 15],[0, 16]], clockwise, number)
            self.swap_inplace([[0, 17],[2, 17],[2, 15],[0, 15]], clockwise, number)
        
    def rotate_optimal(self):
        '''
            Performs the optimal rotation from a given state.

            returns:
                True if optimal move did not result in a solve
                False if optimal move did result in a solve
        '''
        if len(self.optimal_path) == 0:
            print("Optimal path has not been set")
            return 0
        if self.move_index < len(self.optimal_path):
            self.rotate(self.optimal_path[self.move_index])
            self.move_index += 1
            return 1
        else:
            print("Cube is already solved.")
            return 0
    
    def set_state(self, new_state):
        self.state = new_state
    def get_state(self):
        return self.state

    def initialize_solved(self):
        temp = [i for i in range(6)] * 3
        temp.sort()
        self.state_solved = np.array([temp, temp, temp], dtype=int)

    def swap_inplace(self, indeces, clockwise=True, number=1):
        for i in range(number):
            if clockwise:
                temp = copy.copy(self.state[indeces[-1][0], indeces[-1][1]])
                for i in range(len(indeces) - 1, 0, -1):
                    self.state[indeces[i][0], indeces[i][1]] = self.state[indeces[i-1][0], indeces[i-1][1]]
                self.state[indeces[0][0], indeces[0][1]] = temp
            else:
                temp = copy.copy(self.state[indeces[0][0], indeces[0][1]])
                for i in range(0, len(indeces)-1):
                    self.state[indeces[i][0], indeces[i][1]] = self.state[indeces[i+1][0], indeces[i+1][1]]
                self.state[indeces[-1][0], indeces[-1][1]] = temp
