import torch
import os
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image


# Load the model and feature extractor from Hugging Face
extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224")
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")

# Classify a single image
def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = extractor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    predicted_label = model.config.id2label[predicted_class_idx]
    return predicted_label
