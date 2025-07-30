# SmartLens AI

SmartLens AI is an AI-powered urban safety analyzer that processes video footage and public CCTV camera snapshots to detect potential hazards, threats, and anomalies. It uses state-of-the-art computer vision models from Hugging Face to analyze video frames and traffic camera images based on user-entered ZIP codes or addresses.

## Features

- Video Upload Analysis:
  - Upload surveillance or traffic videos for automated detection of:
    - Hazardous objects
    - Fire or smoke
    - Weapons
    - Police presence
    - Suspicious behavior
    - Accidents
    - Crowds
    - Abandoned objects

- ZIP Code Camera Search:
  - Enter a ZIP code or address to scan nearby public traffic or CCTV feeds (starting with California)
  - Scrapes official DOT websites for live images
  - Classifies snapshot images using Hugging Face AI models
  - Returns a road hazard summary showing areas to avoid

- Frame Extraction:
  - Automatically extracts video frames on upload for classification

- Hugging Face Integration:
  - Uses `google/vit-base-patch16-224` for image classification

- ZIP Location Lookup:
  - Converts ZIP codes into geographic coordinates to locate relevant camera feeds

## Tech Stack

Frontend:
- Next.js (App Router and Pages Router hybrid)
- React
- Tailwind CSS
- Axios

Backend:
- Python (FastAPI)
- OpenCV for frame extraction
- Playwright for scraping public camera snapshots
- Hugging Face Transformers and PyTorch for classification
- Custom ZIP code dataset for geolocation


# set up (foer windows)
backend set up:

-cd backend
-python -m venv venv
-venv\Scripts\activate       
-pip install -r requirements.txt
-uvicorn main:app --reload

Frontend Setup:
-cd client
-npm install
-npm run dev



#How It Works

1-Video Upload

2-User uploads a video

3-Backend extracts frames using OpenCV

4-Each frame is classified using a Hugging Face model

5-Predictions are displayed alongside each frame in the UI

it also has ZIP Code Search
--User enters a ZIP code or address

Runs classification on the images

Returns a summary of detected issues by road or area

Model Used
google/vit-base-patch16-224

Easily extendable to object detection and action recognition models from Hugging Face

#Use Cases:
Public safety and crime detection

Emergency response and hazard alerts

Urban analytics and traffic reporting

Smart city surveillance applications
