import timm
import torch
import joblib
import gradio as gr
from torchvision import transforms
from PIL import Image

# Load models
feature_extractor = timm.create_model('nextvit_small.bd_ssld_6m_in1k_384', pretrained=True)
feature_extractor.eval()

logreg = joblib.load('potato_logreg.pkl')

class_names = ['not_potato', 'potato']

transform = transforms.Compose([
    transforms.Resize((384, 384)),
    transforms.ToTensor(),
])

# Define prediction function
def predict(image):
    image = image.convert('RGB')
    img_tensor = transform(image).unsqueeze(0)  # (1, 3, 384, 384)

    with torch.no_grad():
        features = feature_extractor.forward_features(img_tensor)
        features = features.mean(dim=[2, 3])  # (1, 960)

    pred = logreg.predict(features.cpu().numpy())
    label = class_names[pred[0]]
    
    return label

# Build Gradio Interface
demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="🥔 Potato Classifier",
    description="Upload an image to see if it's a Potato or Not!"
)

# Launch locally
if __name__ == "__main__":
    demo.launch()
