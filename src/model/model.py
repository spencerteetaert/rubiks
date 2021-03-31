'''
PyTorch model file
'''
import torch.nn as nn
import torch
import torch.nn.functional as F
import numpy

class RubiksModel(nn.Module):
    def __init__(self, internal_dimensions=[800, 800, 320], dropout_rate=0.1, activation=F.relu):
        super(RubiksModel, self).__init__()
        self.name = 'RubiksModel'
        self.activation = activation
        self.internal_dimensions = internal_dimensions
        self.dropout_rate = dropout_rate
        self.ident = torch.eye(6)

        self.fc1 = nn.Linear(3*18*6, internal_dimensions[0])
        self.fcs = []
        for i in range(len(internal_dimensions)-1):
            self.fcs += [nn.Linear(internal_dimensions[i], internal_dimensions[i+1])]
        self.fc2 = nn.Linear(internal_dimensions[-1], 21)

    def forward(self, x):
        # Input: Nx3x18x6 one hot encoded rubiks cube state data
        x = self.ident[x].view(-1, 3*18*6)
        # x = x.view(-1, 3*18).float()
        x = self.activation(self.fc1(x))
        for i in range(len(self.internal_dimensions)-1):
            x = F.dropout(self.activation(self.fcs[i](x)), self.dropout_rate)
        x = self.activation(self.fc2(x))

        # Output: Nx21 one hot encoded heuristic prediction
        return x