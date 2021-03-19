'''
PyTorch model file
'''
import torch.nn as nn
import torch
import torch.nn.functional as F
import numpy

class RubiksModel(nn.Module):
    def __init__(self, internal_dimensions=[800, 800, 320], dropout_rate=0.1):
        super(RubiksModel, self).__init__()
        self.name = 'RubiksModel'
        self.net = nn.Sequential(
            # 1,163,540 tunable parameters
            nn.Linear(3*18*6, internal_dimensions[0]),
            nn.ReLU(),
            nn.Linear(internal_dimensions[0], internal_dimensions[1]),
            nn.ReLU(),
            nn.Dropout(p=dropout_rate), # Use of dropout to encourage generlization. 
                                # Used because of the large state space
            nn.Linear(internal_dimensions[1], internal_dimensions[2]),
            nn.ReLU(),
            nn.Dropout(p=dropout_rate),
            nn.Linear(internal_dimensions[2], 21)
        )

    def forward(self, x):
        # Input: Nx3x18x6 one hot encoded rubiks cube state data
        x = torch.flatten(x)

        # Output: Nx21 one hot encoded heuristic prediction
        return self.net(x)