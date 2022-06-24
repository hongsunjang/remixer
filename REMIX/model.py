import torch.nn as nn

class AE(nn.Module):
    def __init__(self):
        super(AE, self).__init__()
        #Encoder with Conv
        self.block1 = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(64),
            nn.Conv2d(64, 64, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2,2)
        )

        self.block2 = nn.Sequential(
            nn.Conv2d(64, 128, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(128),
            nn.Conv2d(128, 128, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(2,2)
        )

        self.block3 = nn.Sequential(
            nn.Conv2d(128, 256, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(256),
            nn.Conv2d(256, 256, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(256),
            nn.Conv2d(256, 256, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(256),
            nn.MaxPool2d(2,2)
        )

        self.block4 = nn.Sequential(
            nn.Conv2d(256, 512, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(512),
            nn.Conv2d(512, 512, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(512),
            nn.Conv2d(512, 512, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(512),
            nn.MaxPool2d(2,2)
        )

        self.block5 = nn.Sequential(
            nn.Conv2d(512, 512, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(512),
            nn.Conv2d(512, 512, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(512),
            nn.Conv2d(512, 512, 3, padding = 1),
            nn.GELU(),
            nn.BatchNorm2d(512),
            nn.MaxPool2d(2,2)
        )

        self.gap = nn.MaxPool2d(7,7)

        #Decoder with Conv

        self.block6 = nn.Sequential(
            nn.ConvTranspose2d(512, 512, 1, padding = 0),
            nn.ReLU(),
            nn.BatchNorm2d(512),
            nn.UpsamplingBilinear2d(scale_factor=2)
        )
        
        self.block7 = nn.Sequential(
            nn.ConvTranspose2d(512, 256, 3, padding = 1),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.UpsamplingBilinear2d(scale_factor=2)
        )

        self.block8 = nn.Sequential(
            nn.ConvTranspose2d(256, 128, 3, padding = 1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.UpsamplingBilinear2d(scale_factor=2)
        )

        self.block9 = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 3, padding = 1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.UpsamplingBilinear2d(scale_factor=2)
        )

        self.block10 = nn.Sequential(
            nn.ConvTranspose2d(64, 64, 3, padding = 1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.UpsamplingBilinear2d(scale_factor=2)
        )

        self.block11 = nn.Sequential(
            nn.ConvTranspose2d(64, 64, 3, padding = 1),
            nn.ReLU(),
            nn.BatchNorm2d(64)
        )

        self.block12 = nn.Sequential(
            nn.ConvTranspose2d(64, 3, 3, padding = 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        
        h = self.block1(x)
        h = self.block2(h)
        h = self.block3(h)
        h = self.block4(h)
        #h = self.block5(h)

        latent_vec = self.gap(h)
        #print(latent_vec.shape)

        #h = self.block6(h)
        h = self.block7(h)
        h = self.block8(h)
        h = self.block9(h)
        h = self.block10(h)
        h = self.block11(h)
        out = self.block12(h)

        return out, latent_vec
    
class autoencoder(nn.Module):
    def __init__(self):
        super(autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(784, 128),
            nn.ReLU(True),
            nn.Linear(128, 64),
            nn.ReLU(True), nn.Linear(64, 12))
        self.decoder = nn.Sequential(
            nn.Linear(12, 64),
            nn.ReLU(True),
            nn.Linear(64, 128),
            nn.ReLU(True), nn.Linear(128, 784), nn.Tanh())

    def forward(self, x):
        b = self.encoder(x)
        x = self.decoder(b)
        return x, b