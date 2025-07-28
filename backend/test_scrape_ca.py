from utils.scrape_california_cameras import get_california_camera_snapshots

urls = get_california_camera_snapshots()

print(f"Total cameras found: {len(urls)}")
for url in urls:
    print(url)