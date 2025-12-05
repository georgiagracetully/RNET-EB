import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset

class RNA_Dataset(Dataset):
    def __init__(self, data):
        self.data = data
        self.tokens = {nt: i for i, nt in enumerate('ACGU')}
        self.label_names = ['logkd_lig_scaled', 'logkd_nolig_scaled']

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sequence=[self.tokens[nt] for nt in (self.data.loc[idx,'sequence'])]
        sequence=np.array(sequence)
        sequence=torch.tensor(sequence)

        labels = np.array([self.data.loc[idx, l] for l in self.label_names])  # Just 1 value per label
        labels = torch.tensor(labels, dtype=torch.float32)  # Ensure labels are of correct float type


        return {'sequence': sequence, 'labels': labels}