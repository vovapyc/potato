from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from potatoPredictor import PotatoPredictor


class ResponseBody(BaseModel):
    is_potato: bool
    probability: float


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


@app.post("/predict/")
async def predict(file: UploadFile = File(...)) -> ResponseBody:
    # Initialize the predictor with ONNX model path
    predictor = PotatoPredictor("nextvit_potatoclassifer.onnx")

    # Make a prediction on an image
    is_potato, prob = predictor.predict(file.file)

    return {"is_potato": is_potato, "probability": round(prob, 4)}
