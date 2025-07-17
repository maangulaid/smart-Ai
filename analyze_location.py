import os
import uuid
from typing import List, Dict
from utils.frame_classifier import classify_image
from utils.video_utils import grab_rtsp_snapshot

# Mocked public CCTV stream database (replace with real sources later)
MOCK_CAMERA_DB = {
    "75201": [  # Dallas, TX zip code
        "rtsp://demo.example.com/traffic_cam1",
        "rtsp://demo.example.com/traffic_cam2"
    ],
    "10001": [  # NYC
        "rtsp://demo.example.com/nyc_1"
    ]
}

FRAME_DIR = "frames"  # reuse this directory for snapshot storage

def get_cameras_by_zip(zipcode: str) -> List[str]:
    return MOCK_CAMERA_DB.get(zipcode, [])

def analyze_location_by_zip(zipcode: str) -> Dict[str, str]:
    cameras = get_cameras_by_zip(zipcode)
    if not cameras:
        return {"error": "No public cameras found for this ZIP code."}

    results = {}

    for cam_url in cameras:
        # Generate unique frame filename
        frame_filename = f"{uuid.uuid4()}.jpg"
        save_path = os.path.join(FRAME_DIR, frame_filename)

        # Grab frame snapshot
        success = grab_rtsp_snapshot(cam_url, save_path)
        if not success:
            continue

        # Classify frame
        label = classify_image(save_path)
        results[frame_filename] = label

    return results
