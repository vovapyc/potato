# filename: app.py

from fastapi import FastAPI, File, UploadFile
from PIL import Image
import torch
import timm
import joblib
import numpy as np
from torchvision import transforms
from pydantic import BaseModel


class ResponseBody(BaseModel):
    is_potato: bool

# ====== Initialize FastAPI ======
app = FastAPI()

# ====== Load Models ======
# Load backbone
feature_extractor = timm.create_model('nextvit_small.bd_ssld_6m_in1k_384', pretrained=True)
feature_extractor.eval()

# Load logistic regression
logreg = joblib.load('potato_logreg.pkl')

# Classes
class_names = ['not_potato', 'potato']

# Preprocessing
transform = transforms.Compose([
    transforms.Resize((384, 384)),
    transforms.ToTensor(),
])

# ====== Define Endpoint ======
@app.post("/predict/")
async def predict(file: UploadFile = File(...)) -> ResponseBody:
    # Load image
    image = Image.open(file.file).convert('RGB')
    img_tensor = transform(image).unsqueeze(0)  # (1, 3, 384, 384)
    
    # Extract features
    with torch.no_grad():
        features = feature_extractor.forward_features(img_tensor)
        features = features.mean(dim=[2, 3])  # (1, 960)

    # Predict
    preds = logreg.predict(features.cpu().numpy())
    label = class_names[preds[0]]
    
    return {'is_potato': label == 'potato'}
