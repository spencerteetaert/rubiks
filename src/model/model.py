'''
PyTorch model file
'''
import torch.nn as nn
import torch
import torch.nn.functional as F
torch.manual_seed(0)
import numpy
from collections import OrderedDict

class RubiksModel(nn.Module):
    def __init__(self, internal_dimensions=[800, 800, 320], dropout_rate=0.1, activation=nn.ReLU, gpu=True):
        super(RubiksModel, self).__init__()
        self.name = 'RubiksModel'
        self.internal_dimensions = internal_dimensions
        self.dropout_rate = dropout_rate
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if not gpu:
            device = torch.device('cpu')
        self.ident = torch.eye(6).to(device)

        fcs = [('Linear_input', nn.Linear(3*18*6, internal_dimensions[0]))]
        fcs += [('Activation_input', activation())]
        fcs += [('Dropout_input', nn.Dropout(dropout_rate))]
        for i in range(len(internal_dimensions)-1):
            fcs += [('Linear{}'.format(i), nn.Linear(internal_dimensions[i], internal_dimensions[i+1]))]
            fcs += [('Activation{}'.format(i), activation())]
            fcs += [('Dropout{}'.format(i), nn.Dropout(dropout_rate))]
        fcs += [('Linear_output', nn.Linear(internal_dimensions[-1], 1))]
        fcs += [('Activation_ouput', activation())]

        self.sequential = nn.Sequential(OrderedDict(fcs))

    def forward(self, x):
        # Input: Nx3x18x6 one hot encoded rubiks cube state data
        x = self.ident[x].view(-1, 3*18*6)
        return torch.clamp(self.sequential(x), 4.51, 20.49)