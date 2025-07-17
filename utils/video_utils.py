## we will use 3 tools to extract pictures from a given videos 
# 1. CV2
# 2. os to create a new folder AND CHECKED FILE PATH

# 3. uuid to create a unique id for each picture





import cv2
import os
import uuid

def extract_frames(video_path, output_directory, max_frames: int = 100):
    # check if video file exists
    # create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    # if could not open video file
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    while True:
        sucess, frame = cap.read()
        if not sucess:
            break
        
        
        filename = f"{uuid.uuid4()}.jpg"
        frame_path = os.path.join(output_directory, filename)
        cv2.imwrite(frame_path, frame)
        frame_count += 1
        
    cap.release()
    return frame_count
import cv2

def grab_rtsp_snapshot(rtsp_url: str, output_path: str = "snapshot.jpg") -> bool:
    try:
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            print(f"❌ Failed to open RTSP stream: {rtsp_url}")
            return False

        ret, frame = cap.read()
        cap.release()

        if ret:
            cv2.imwrite(output_path, frame)
            print(f"✅ Snapshot saved to {output_path}")
            return True
        else:
            print("❌ Failed to capture frame.")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
