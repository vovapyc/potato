import numpy as np
import onnxruntime as ort
from PIL import Image

class PotatoPredictor:
    def __init__(self, model_path):
        self.session = ort.InferenceSession(model_path)
    
    def preprocess(self, image_path):
        img = Image.open(image_path).convert("RGB")
        img = img.resize((384, 384))
        arr = np.asarray(img).astype(np.float32) / 255.0
        arr = np.transpose(arr, (2, 0, 1))  # (C, H, W)
        arr = np.expand_dims(arr, axis=0)  # (1, C, H, W)
        return arr
    
    def predict(self, image_path, threshold=0.5):
        input_array = self.preprocess(image_path)
        input_name = self.session.get_inputs()[0].name
        output = self.session.run(None, {input_name: input_array})
        logit = output[0][0][0]
        prob = 1 / (1 + np.exp(-logit))
        is_potato = prob > threshold
        return is_potato, prob