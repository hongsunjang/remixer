import warnings
warnings.filterwarnings('ignore')
import librosa
import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import unicodedata
from numpy import linalg
font = fm.FontProperties(fname='./cache/asd_font.ttf')

def wav2mel(path):
    audio, sample_rate= librosa.load(path)
    spec = librosa.feature.melspectrogram(
        y=audio, 
        sr=sample_rate, 
        n_fft=2048, 
        hop_length=512, 
        win_length=None, 
        window='hann', 
        center=True, 
        pad_mode='reflect', 
        power=2.0,
        n_mels=512
    )
    spec = cv2.resize(spec, (512, 512))
    plt.imsave('./output/mel_spectrogram.png', spec)

def inference(model, img_path, device):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    img = np.transpose(img, (2,0,1))
    img = torch.Tensor(img)
    img = img[None,:,:,:]
    x = img.to(device, dtype = torch.float)
    _, latent = model(x)
    return latent.squeeze().detach().cpu().numpy().tolist()

def plot_tsne(xy, colors=None, decoder = None):    
    fig = plt.figure(figsize = (30,30))
    #ax = fig.add_subplot(projection='3d')
    ax = fig.add_subplot()
    ax.axis('off')
    ax.scatter(xy[:,0], xy[:,1], c=colors, s=500)
    label = decoder.values()
    for i, txt in enumerate(label):
        ax.annotate(unicodedata.normalize('NFC',txt), (xy[i,0], xy[i,1]), fontproperties=font, textcoords='offset points')
    plt.show()
    plt.savefig('./output/tsne.png',dpi=300)
    
def recommend(query, features, decoder):
    similarity_list = [0]*165
    for i in range(165):
            similarity_list[i] = features[i].dot(query) / (linalg.norm(features[i])*linalg.norm(query))
    res = sorted(range(len(similarity_list)), key = lambda sub: similarity_list[sub])[-4:]
    res.reverse()
    print('제일 가까운 것')
    for idx, i in enumerate(res):
        if idx == 3:
            continue
        print(f'{idx+1}순위: ',decoder[i])
    print('제일 안 가까운 것')
    res = sorted(range(len(similarity_list)), key = lambda sub: similarity_list[sub])[:4]
    for idx, i in enumerate(res):
        if idx == 0:
            continue
        print(f'{idx}순위: ',decoder[i])