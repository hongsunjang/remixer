# %%
import warnings
warnings.filterwarnings('ignore')
import sys
import json
import cv2
import torch

from sklearn.manifold import TSNE
from sklearn.decomposition import IncrementalPCA
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import unicodedata
import numpy as np
from numpy import linalg

from dataset import Custom_dataset
from model import *
from utils import *
    
# %%
print('$ Converting .wav file into mel spectrogram $')
wav_path = sys.argv[1]
img_path = './output/mel_spectrogram.png'
#device = torch.device('cuda')
device = torch.device('cpu')
model = autoencoder().to(device)
model.load_state_dict(torch.load('/home/hahajjjun/Junha Park/remixer/REMIX/cache/best.pth'))
wav2mel(wav_path)
rec_img, query_latent = inference(model, img_path, device)
with open('./cache/title.json', 'r') as file:
    path = json.load(file)['titles']

# %%
with open('./cache/encode.json') as file:
    encoder = json.load(file)
decoder = {}
for idx, item in enumerate(path):
    ID = item.split('_')[1].split('.')[0]
    decoder[idx] = encoder[ID].split('/')[-1].replace('-accompaniment.wav', '')
    
# %%
features = np.load('./cache/12_latent.npy')
query_latent = query_latent[None,:]
features = np.concatenate((features, query_latent), axis = 0)
embedded = TSNE(n_components=2).fit_transform(features)
font = fm.FontProperties(fname='./cache/asd_font.ttf')

# %%
print('$ Plotting PCA-colored tSNE map $')
pca = IncrementalPCA(n_components=3)
pca_projection = pca.fit_transform(features)
pca_projection -= np.min(pca_projection, axis=0)
pca_projection /= np.max(pca_projection, axis=0)
plot_tsne(embedded, pca_projection, decoder)

# %%
print('$ Recommendation $')
recommend(embedded, decoder)