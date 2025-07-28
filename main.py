from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uuid
import shutil
import json
from dotenv import load_dotenv
load_dotenv()
from dotenv import load_dotenv
load_dotenv()

from utils.frame_classifier import classify_image
from utils.video_utils import extract_frames
#from utils.analyze_location import analyze_location_by_zip
from analyze_location import analyze_location_by_zip
from utils.local_zip_lookup import get_coords_from_zip


# Paths for upload and frame storage
UPLOAD_DIR = "uploads"
FRAME_DIR = "frames"

# Create folders if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)

# Initialize FastAPI
app = FastAPI()

# Enable frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve images in /frames as static files
app.mount("/frames", StaticFiles(directory=FRAME_DIR), name="frames")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    upload_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save uploaded file
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract frames to FRAME_DIR
    extract_frames(upload_path, FRAME_DIR)

    return {
        "filename": unique_filename,
        "status": "Video uploaded and frames extracted successfully."
    }


@app.get("/frames-list")
def get_frame_list():
    files = os.listdir(FRAME_DIR)
    jpgs = [f for f in files if f.endswith(".jpg")]
    jpgs.sort()
    return jpgs


@app.post("/classify")
def classify_all_frames():
    results = {}
    frame_files = [f for f in os.listdir(FRAME_DIR) if f.endswith(".jpg")]
    for filename in frame_files:
        full_path = os.path.join(FRAME_DIR, filename)
        label = classify_image(full_path)
        results[filename] = label

    # Save to JSON file
    with open("predictions.json", "w") as f:
        json.dump(results, f)

    return {"message": "Classification complete", "total": len(results)}



@app.get("/predictions")
def get_predictions():
    predictions_path = "predictions.json"

    if not os.path.exists(predictions_path):
        return {"error": "No predictions file found yet."}

    with open(predictions_path, "r") as f:
        content = f.read().strip()
        if not content:
            return {"error": "Predictions file is empty."}

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"error": "Predictions file is corrupted."}


@app.post("/analyze-location")
async def analyze_location_route(request: Request):
    body = await request.json()
    zip_code = body.get("zip_code")

    if not zip_code:
        return {"error": "ZIP code is required."}

    result = analyze_location_by_zip(zip_code)
    return result

from utils.local_zip_lookup import get_coords_from_zip

@app.get("/zip-to-coords/{zip_code}")
def zip_to_coords(zip_code: str):
    zip_data = load_zip_data_github("https://raw.githubusercontent.com/maangulaid/dataset-for-smart-ai-california/main/uszips.csv")
    coords = get_coords_from_zip(zip_code, zip_data)
    if coords:
        return {"lat": coords[0], "lng": coords[1]}
    return {"error": "Unable to geocode ZIP code"}
