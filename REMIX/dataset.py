import cv2
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import albumentations as A

class Custom_dataset(Dataset):
    def __init__(self, img_path):
        self.img_path = img_path

    def __len__(self):
        return len(self.img_path)

    def __getitem__(self, idx):
        path = self.img_path[idx]
        img = cv2.imread(path)
        img = cv2.resize(img, (224, 224))
        img = np.transpose(img, (2,0,1))
        
        #img = A.VerticalFlip(p=0.5)(image=img)['image']
        img = A.HorizontalFlip(p=0.5)(image=img)['image']
        #img = A.RandomRotate90(90, p=0.5)(image=img)['image']
        '''
         if self.mode=='train':
            augmentation = random.randint(0,2)
            if augmentation==1:
                img = img[::-1].copy()
            elif augmentation==2:
                img = img[:,::-1].copy()
            img = transforms.ToTensor()(img)
            label = self.labels[idx]
            label = label_unique[label]
            #label = to_categorical(label, 49)
            return img, label
        if self.mode=='test':
            img = transforms.ToTensor()(img)
        '''
        return path, img