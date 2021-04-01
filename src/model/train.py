import torch
import time
from datetime import datetime
import os
from random import shuffle
import numpy as np
import torch.nn as nn
import torch.optim as optim
from .data_handler import generate_dataset, load_datasets
from ..rubiks.cube import Cube

def train(model, num_epochs=30, learning_rate=0.001, batch_size=32, train_on=10000, momentum=0.9, valid_on=2000, data_path="", savepath="", gpu=True):
    ''' Train the model inplace
    Args:
        model: the model to train on
        num_epochs: the number of epochs
        learning_rate: the learning rate
        batch_size: the number of data in each batch
        train_on: the number of data to train on, which will be generated with the function gen_dataset
        valid_on: the number of data to validate on, which will be generated with the function gen_dataset
    '''

    # get the training and validation sets
    if data_path == "":
        train_set, valid_set = generate_dataset(train_on), generate_dataset(valid_on)
    else:
        train_set, valid_set = load_datasets(data_path)

    train_loader = torch.utils.data.DataLoader(train_set, batch_size, shuffle=True)
    valid_loader = torch.utils.data.DataLoader(valid_set, batch_size, shuffle=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if not gpu:
        device = torch.device('cpu')
    model.to(device) # Puts model on training hardware
    print("Training on device: {}".format(torch.cuda.get_device_name(model.ident.get_device())))

    criterion = nn.L1Loss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=momentum)
    # create arrays to store training data
    train_acc = np.zeros(num_epochs)
    train_loss = np.zeros(num_epochs)
    valid_acc = np.zeros(num_epochs)
    valid_loss = np.zeros(num_epochs)

    if savepath != "":
        now = datetime.now()
        curr_time = now.strftime("%d%m%Y_%H%M%S")
        savepath += "{}_{}".format(model.name, curr_time)
        os.mkdir(savepath)
        savepath += "/"
        create_readme(model, num_epochs, batch_size, len(train_set), len(valid_set), criterion, optimizer, savepath)

    for epoch in range(num_epochs):
        s = time.time()
        model.train()
        # data for each epoch
        total_train_loss = 0.0
        total_train_acc = 0.0
        total_data = 0
        for i, data in enumerate(train_loader, 0):
            # Get the inputs, sends to device 
            inputs, labels = data[0].to(device), data[1].to(device)
            labels = labels.unsqueeze(1)

            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward pass, backward pass, and optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels.long())
            loss.backward()
            optimizer.step()

            # Calculate the statistics
            pred = torch.round(outputs)
            corr = pred.eq(labels).sum()
            total_train_acc += corr
            total_train_loss += loss.item()
            total_data += len(labels)
        # write data of each epoch to the arrays
        train_acc[epoch] = float(total_train_acc) / total_data
        train_loss[epoch] = float(total_train_loss) / (i + 1)
        valid_acc[epoch], valid_loss[epoch] = evaluate(model, valid_loader, criterion, gpu=gpu)
        # print the data
        print(("Epoch {}: Train accuracy: {}, Train loss: {} | " +
               "Validation accuracy: {}, Validation loss: {} | Time: {}").format(
            epoch + 1,
            train_acc[epoch],
            train_loss[epoch],
            valid_acc[epoch],
            valid_loss[epoch],
            time.time() - s))
        if savepath != "":
            name = savepath + "{}_e{}".format(model.name, epoch)
            torch.save(model, name)
            name = savepath + "{}_RESULTS_e{}".format(model.name, epoch)
            results = (train_acc, train_loss, valid_acc, valid_loss)
            torch.save(results, name)

    return train_acc, train_loss, valid_acc, valid_loss

def evaluate(model, dataset, criterion, gpu=True):
    """ Evaluate the model on the validation set.
    Args:
        model: the model to be evaluated
        dataset: a return object of function gen_dataset
        criterion: the loss function
    Returns:
        acc: a scalar for the avg classification accuracy over the validation set
        loss: a scalar for the average loss over the validation set
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if not gpu:
        device = torch.device('cpu')
    model.eval()
    total_loss = 0.0
    total_corr = 0.0
    total_data = 0
    for i, data in enumerate(dataset, 0):
        inputs, labels = data[0].to(device), data[1].to(device)
        labels = labels.unsqueeze(1)
        outputs = model(inputs)
        loss = criterion(outputs, labels.long())
        pred = torch.round(outputs)
        total_corr += pred.eq(labels).sum()
        total_loss += loss.item()
        total_data += len(labels)
    acc = float(total_corr) / total_data
    loss = float(total_loss) / (i + 1)
    return acc, loss

def create_readme(model, num_epochs, batch_size, train_set_length, valid_set_length, criterion, optimizer, savepath):
    b = "-------------------------\n"
    filename = savepath + "README.txt"

    text = "Training Data Information\n\n"
    text += "Training size: {:,}\n".format(train_set_length)
    text += "Validation size: {:,}\n".format(valid_set_length)
    text += b

    text += "Model Parameters\n\n"
    text += model.__repr__() + "\n"
    text += b

    text += "Training Parameters\n\n"
    text += "Batch size: {}\n".format(batch_size)
    text += "Nominal epochs: {}\n".format(num_epochs)
    text += "Loss function: {}\n".format(criterion)
    text += "Optimizer: {}\n".format(optimizer)
    device = torch.cuda.get_device_name(model.ident.get_device())
    text += "Device trained on: {}\n".format(device)

    f = open(filename, "w")
    f.write(text)
    f.close()
