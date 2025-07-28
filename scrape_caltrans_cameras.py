from playwright.sync_api import sync_playwright
import json
import time

OUTPUT_FILE = "california_cameras.json"
TARGET_URL = "https://cwwp2.dot.ca.gov/vm/iframemap.htm"

def scrape_caltrans_cameras():
    cameras = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # set to False to see browser window
        page = browser.new_page()
        page.goto(TARGET_URL)

        print("[INFO] Waiting for map to load...")
        page.wait_for_timeout(5000)

        print("[INFO] Clicking the 'Cameras' toggle button...")
        try:
            page.locator("text=Cameras").click()
        except:
            print("[WARN] Failed to click 'Cameras' using text locator.")
            page.mouse.click(70, 190)  # fallback

        print("[INFO] Waiting for camera snapshots to appear...")
        page.wait_for_timeout(8000)

        print("[INFO] Scanning for <img> elements...")
        img_tags = page.query_selector_all("img")
        print(f"[DEBUG] Found {len(img_tags)} <img> tags")

        for img in img_tags:
            src = img.get_attribute("src")
            title = img.get_attribute("title")

            if src:
                print(" -", src)  # Debug: print every image src

            if src and "digitalimages" in src:
                cameras.append({
                    "img_url": "https://cwwp2.dot.ca.gov" + src,
                    "title": title or "Unnamed"
                })

        browser.close()

    print(f"\n✅ Found {len(cameras)} camera snapshot images.")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(cameras, f, indent=2)
    print(f"📦 Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_caltrans_cameras()
