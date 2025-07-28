import os
from utils.frame_classifier import classify_image

FRAME_DIR = "frames"

def classify_all_frames():
    if not os.path.exists(FRAME_DIR):
        print(f"{FRAME_DIR} does not exist.")
        return {}

    frame_files = [f for f in os.listdir(FRAME_DIR) if f.endswith(".jpg")]
    if not frame_files:
        print("No frames to classify.")
        return {}

    print(f"Found {len(frame_files)} frame(s). Classifying...")

    predictions = {}
    for filename in frame_files:
        path = os.path.join(FRAME_DIR, filename)
        label = classify_image(path)
        predictions[filename] = label
        print(f"{filename}: {label}")
    
    return predictions

if __name__ == "__main__":
    predictions = classify_all_frames()
    print("\nSummary:")
    for image, label in predictions.items():
        print(f"Image: {image} — Predicted: {label}")
