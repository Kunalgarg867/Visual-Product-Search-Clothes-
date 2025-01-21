from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms
from sklearn.metrics.pairwise import cosine_similarity
import os

model = torch.hub.load('pytorch/vision', 'resnet50', pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])  # Remove the classification (FC) layer
model.eval()

# Define the transformation used for the dataset
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Function to get the embedding of an image
def get_embedding(img_path):
    with Image.open(img_path) as img:
        img_tensor = transform(img).unsqueeze(0)  # Add batch dimension
        with torch.no_grad():
            embedding = model(img_tensor).squeeze().numpy()  # Extract embedding
    return embedding
