"""
Training utilities.

(c) Aleksei Tiulpin, University of Oulu, 2018

"""

import torch
import torch.nn as nn
from torch.autograd import Variable
from tqdm import tqdm
import gc


def train_epoch(epoch, net, optimizer, train_loader, criterion, max_ep):

    net.train(True)

    running_loss = 0.0
    n_batches = len(train_loader)

    for i, sample in tqdm(enumerate(train_loader), total=len(train_loader)):
        optimizer.zero_grad()
        # forward + backward + optimize
        labels = Variable(sample['label'].float().cuda(async=True))
        inputs = Variable(sample['img'].cuda(), requires_grad=True)
        
        outputs = net(inputs).squeeze()

        loss = criterion(outputs, labels)
        
        loss.backward()
        optimizer.step()

        running_loss += loss.data[0]

        gc.collect()
    gc.collect()

    return running_loss/n_batches
