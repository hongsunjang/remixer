# %%
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import json
from glob import glob
from tqdm import tqdm
import cv2
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import albumentations as A
import matplotlib.pyplot as plt

from dataset import Custom_dataset
from model import AE

# %%
cfg = {
    'batch_size' : 8,
    'learning_rate': 1e-3
}

train_path = glob('/home/hahajjjun/Junha Park/remixer/REMIX/processed/*.png')
train_dataset = Custom_dataset(train_path)
train_loader = DataLoader(train_dataset, shuffle=False, batch_size=cfg['batch_size'])
device = torch.device('cuda')
model = AE().to(device)
optimizer = optim.Adam(model.parameters(), lr = cfg['learning_rate'])

def reconstruction_loss(x, x_prime):
    return nn.MSELoss(reduction='mean')(x_prime, x)/(224*224)

def train(model, optimizer, cfg):
    print('TRAINING MODEL...')
    print(cfg)
    best = 10000000
    losses = []
    for epoch in range(20):
        latents = []
        paths = []
        train_loss = 0
        for i, (path, x) in enumerate(train_loader):
            optimizer.zero_grad()
            x = x.to(device, dtype = torch.float)
            x_prime, latent = model(x)
            loss = reconstruction_loss(x, x_prime)
            loss.backward()
            train_loss += loss.item()/len(train_loader)
            optimizer.step()
            latents += latent.squeeze().cpu().detach().numpy().tolist()
            paths += path
        losses.append(train_loss)
        if train_loss < best:
            best = train_loss
            best_latents = latents
            torch.save(model.state_dict(), f'/home/hahajjjun/Junha Park/remixer/REMIX/best.pth')
        print(f'>>> Epoch: {epoch}, Average loss: {train_loss}')
    print('PLOTTING LOSS...')
    plt.title('MSE Reconstruction Loss')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.plot(range(1,len(losses)+1), losses)
    plt.savefig('loss.png', dpi=300)
    
    return paths, best_latents

def run():
    paths, best_latents = train(model, optimizer, cfg)
    return paths, best_latents
        