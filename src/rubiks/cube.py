'''
File for cube class
'''
import copy
import numpy as np
from ..ui.display_tools import display_console

#W, R, B, G, O, Y
# color_ind = [0, 1, 2, 3, 4, 5]
color_ind = [2, 1, 4, 5, 0, 3]
possible_rotations = ['L','R','B','F','U','D','L\'','R\'','B\'','F\'','U\'','D\'','L2','R2','B2','F2','U2','D2']
possible_rotations_inverse = {'L':'L\'','R':'R\'','B':'B\'','F':'F\'','U':'U\'','D':'D\'', \
    'L\'':'L','R\'':'R','B\'':'B','F\'':'F','U\'':'U','D\'':'D', \
        'L2':'L2','R2':'R2','B2':'B2','F2':'F2','U2':'U2','D2':'D2'}

class Cube:
    def __init__(self, state=None, optimal_path=[]):
        self.initialize_solved()
        if state is None:
            self.state = copy.copy(self.state_solved)
        else:
            self.state = state
        self.move_index = 0
        self.optimal_path = optimal_path
        
    def __repr__(self):
        return str(self.state)#display_console(self)
    
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
                # print(rot, last_rotation)
                if last_rotation != possible_rotations_inverse[rot]:
                    break
                else:
                    print("INVERTED MOVE", rot, last_rotation)
            last_rotation = rot
            self.rotate(rot)
            self.optimal_path = [possible_rotations_inverse[rot]] + self.optimal_path

    def rotate(self, rotation):
        print(rotation)
        if rotation[-1] == '\'':
            print("Counterclockwise rotation")
            if rotation[0] == 'L': # :,0:3,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'R': # :,3:6,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'B': # :,12:15,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'F': # :,15:18,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'U': # :,6:9,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'D': # :,9:12,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
        elif rotation[-1] == '2':
            print("Double rotation")
            if rotation[0] == 'L': # :,0:3,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'R': # :,3:6,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'B': # :,12:15,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'F': # :,15:18,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'U': # :,6:9,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'D': # :,9:12,:
                # Rotate edge tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
        else:
            print("Regular rotation")
            if rotation[0] == 'L': # :,0:3,:
                # Rotate ed tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'R': # :,3:6,:
                # Rotate ed tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'B': # :,12:15,:
                # Rotate ed tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'F': # :,15:18,:
                # Rotate ed tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'U': # :,6:9,:
                # Rotate ed tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
            elif rotation[0] == 'D': # :,9:12,:
                # Rotate ed tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                # Rotate face tiles
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
                self.swap_inplace([[0, 0],[0, 0],[0, 0],[0, 0]])  
        
    def rotate_optimal(self):
        '''
            Performs the optimal rotation from a given state
        '''
        if self.move_index < len(self.optimal_path):
            self.rotate(self.optimal_path[self.move_index])
            self.move_index += 1
        else:
            print("Cube is already solved.")
    
    def set_state(self, new_state):
        self.state = new_state
    def get_state(self):
        return self.state

    def initialize_solved(self):
        F = [0, 0, 0, 0, 0, 0]
        F[color_ind[3]] = 1
        F_solved = np.tile(F, [3,3,1])
        U = [0, 0, 0, 0, 0, 0]
        U[color_ind[0]] = 1
        U_solved = np.tile(U, [3,3,1])
        L = [0, 0, 0, 0, 0, 0]
        L[color_ind[4]] = 1
        L_solved = np.tile(L, [3,3,1])
        R = [0, 0, 0, 0, 0, 0]
        R[color_ind[1]] = 1
        R_solved = np.tile(R, [3,3,1])
        B = [0, 0, 0, 0, 0, 0]
        B[color_ind[2]] = 1
        B_solved = np.tile(B, [3,3,1])
        D = [0, 0, 0, 0, 0, 0]
        D[color_ind[5]] = 1
        D_solved = np.tile(D, [3,3,1])
        self.state_solved = np.concatenate((L_solved, R_solved, U_solved, D_solved, B_solved, F_solved), axis=1)
    def swap_inplace(self, indeces):
        temp = copy.copy(self.state[indeces[-1][0], indeces[-1][1]])
        for i in range(1, len(indeces)):
           self.state[indeces[i][0], indeces[i][1]] = self.state[indeces[i-1][0], indeces[i-1][1]]
        self.state[indeces[0][0], indeces[0][1]] = temp