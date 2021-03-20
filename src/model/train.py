import torch
from random import shuffle
import numpy as np
import torch.nn as nn
import torch.optim as optim

def train(model, num_epochs=3, learning_rate=0.001, batch_size=32, train_on=10000, valid_on=2000):
    ''' Train the model inplace
    Args:
        model: the model to train on
        num_epochs: the number of epochs
        learning_rate: the learning rate
        batch_size: the number of data in each batch
        train_on: the number of data to train on, which will be generated with the function get_dataset
        valid_on: the number of data to validate on, which will be generated with the function get_dataset
    '''
    # get the training and validation sets
    train_set, valid_set = get_datset(train_on, batch_size), get_datset(valid_on, batch_size)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)
    # create arrays to store training data
    train_acc = np.zeros(num_epochs)
    train_loss = np.zeros(num_epochs)
    valid_acc = np.zeros(num_epochs)
    valid_loss = np.zeros(num_epochs)

    for epoch in range(num_epochs):
        # data for each epoch
        total_train_loss = 0.0
        total_train_acc = 0.0
        total_data = 0
        for i, data in enumerate(train_set, 0):
            # Get the inputs
            inputs, labels = data
            # Zero the parameter gradients
            optimizer.zero_grad()
            # Forward pass, backward pass, and optimize
            outputs = model(inputs.float())
            loss = criterion(outputs, labels.long())
            loss.backward()
            optimizer.step()
            # Calculate the statistics
            pred = outputs.max(1, keepdim=True)[1]
            corr = pred.eq(labels.view_as(pred))
            total_train_acc += corr.squeeze().sum().item()
            total_train_loss += loss.item()
            total_data += len(labels)
        # write data of each epoch to the arrays
        train_acc[epoch] = float(total_train_acc) / total_data
        train_loss[epoch] = float(total_train_loss) / (i + 1)
        valid_acc[epoch], valid_loss[epoch] = evaluate(model, valid_set, criterion)
        # print the data
        print(("Epoch {}: Train accuracy: {}, Train loss: {} |" +
               "Validation accuracy: {}, Validation loss: {}").format(
            epoch + 1,
            train_acc[epoch],
            train_loss[epoch],
            valid_acc[epoch],
            valid_loss[epoch]))


def get_datset(num_data, batch_size):
    '''
    Args:
        num_data: the number of data in the dataset to be built. Note the number will not be exactly num_data to ensure
                even division among the possible values of n.
        batch_size: the desired batch size for the dataset

    Returns:
        batched_set: list[tuple(tensor, tensor)]
                    a list of tuples representing the batches. The first tensor of each tuple represents the
                    input with shape torch.Size([batch_size, 3, 18]), and the second tensor represent labels with
                    shape torch.Size([batch_size]).
    '''
    lower_n = 5  # to be set later
    every_n = num_data // (21 - lower_n)
    dataset = []
    for i in range(lower_n, 21):
        for j in range(every_n):
            random_cube = Cube()
            random_cube.scramble(num_moves=i)
            dataset.append((random_cube.state, i))

    shuffle(dataset)
    batched_set = []
    index = 0
    while index < len(dataset):
        if (index+batch_size) >= len(dataset):
            end = len(dataset)
        else:
            end = index+batch_size

        batch_array = np.zeros((end-index, 3, 18), dtype=int)
        batch_label = np.zeros(end-index, dtype=int)

        for i in range(index, end):
            batch_array[i-index] = dataset[i][0]
            batch_label[i-index] = dataset[i][1]
        index += batch_size
        batched_set.append((torch.from_numpy(batch_array), torch.from_numpy(batch_label)))
    return batched_set

def evaluate(model, dataset, criterion):
    """ Evaluate the model on the validation set.
    Args:
        model: the model to be evaluated
        dataset: a return object of function get_dataset
        criterion: the loss function
    Returns:
        acc: a scalar for the avg classification accuracy over the validation set
        loss: a scalar for the average loss over the validation set
    """
    total_loss = 0.0
    total_corr = 0.0
    total_data = 0
    for i, data in enumerate(dataset, 0):
        inputs, labels = data
        outputs = model(inputs.float())
        loss = criterion(outputs, labels.long())
        pred = outputs.max(1, keepdim=True)[1]
        total_corr += pred.eq(labels.view_as(pred)).sum().item()
        total_loss += loss.item()
        total_data += len(labels)
    acc = float(total_corr) / total_data
    loss = float(total_loss) / (i + 1)
    return acc, loss