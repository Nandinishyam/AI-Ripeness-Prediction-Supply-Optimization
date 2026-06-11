import os
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms

class BananaRotDataset(Dataset):
    def __init__(self, csv_file, root_dir):
        self.annotations = pd.read_csv(csv_file)
        self.root_dir = root_dir
        
        # The SDE Data Augmentation Pipeline!
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),           
            transforms.RandomHorizontalFlip(p=0.5), 
            transforms.RandomRotation(degrees=15),  
            transforms.ColorJitter(brightness=0.1, contrast=0.1), 
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                 std=[0.229, 0.224, 0.225])
        ])

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        img_path = os.path.join(self.root_dir, self.annotations.iloc[index, 0])
        image = Image.open(img_path).convert("RGB")
        image = self.transform(image)
        y_label = torch.tensor(float(self.annotations.iloc[index, 1]))
        return image, y_label

# This block tests the file when you run it directly
if __name__ == "__main__":
    print("Testing the BananaRotDataset pipeline...")
    try:
        dataset = BananaRotDataset(csv_file="banana_labels.csv", root_dir="./banana_dataset")
        img, label = dataset[0]
        print(f"SUCCESS! Image tensor shape: {img.shape}") 
        print(f"Label: {label} days")
    except Exception as e:
        print(f"Error occurred: {e}")