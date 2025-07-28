# download_snapshots.py

import os
import json
import requests

CAMERA_JSON = "california_cameras.json"
SNAPSHOT_DIR = "snapshots"
LIMIT = 10  # ✅ Only download first 10 for testing

def download_all_snapshots():
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)

    with open(CAMERA_JSON, "r") as f:
        cameras = json.load(f)

    count = 0
    for cam in cameras[:LIMIT]:
        url = cam.get("img_url")
        name = cam.get("title", f"camera_{count}")
        filename = name.replace(" ", "_").replace("/", "_") + ".jpg"
        path = os.path.join(SNAPSHOT_DIR, filename)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Saved: {filename}")
                count += 1
            else:
                print(f"[WARN] Failed {url} — status {response.status_code}")
        except Exception as e:
            print(f"[ERROR] {url} — {e}")

    print(f"\n✅ Finished downloading {count} snapshots to '{SNAPSHOT_DIR}/'")

if __name__ == "__main__":
    download_all_snapshots()
