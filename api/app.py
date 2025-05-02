from fastapi import FastAPI, File, UploadFile
from PIL import Image
import torch
import timm
import joblib
from torchvision import transforms
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class ResponseBody(BaseModel):
    is_potato: bool


app = FastAPI()

# CORS middleware
origins = [
    "http://localhost:5173",
    "https://vovapyc.github.io",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
emb_model = timm.create_model("nextvit_small.bd_ssld_6m_in1k_384", pretrained=True)
emb_model.eval()
potato_model = joblib.load("potato_logreg.pkl")


# Preprocessing
transform = transforms.Compose(
    [
        transforms.Resize((384, 384)),
        transforms.ToTensor(),
    ]
)


@app.post("/predict/")
async def predict(file: UploadFile = File(...)) -> ResponseBody:
    # Load and transform image
    image = Image.open(file.file).convert("RGB")
    img_tensor = transform(image).unsqueeze(0)

    # Get embeddings
    with torch.no_grad():
        features = emb_model.forward_features(img_tensor)
        features = features.mean(dim=[2, 3])

    preds = potato_model.predict(features.cpu().numpy())
    is_potato = preds[0]

    return {"is_potato": is_potato}
