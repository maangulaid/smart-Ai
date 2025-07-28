from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_california_camera_snapshots():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    print("[INFO] Launching browser...")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        print("[INFO] Visiting site...")
        driver.get("https://cwwp2.dot.ca.gov/vm/iframemap.htm")
        time.sleep(5)

        print("[INFO] Parsing HTML...")
        soup = BeautifulSoup(driver.page_source, "html.parser")

        image_urls = []
        for img in soup.find_all("img"):
            src = img.get("src")
            print(f"Found image src: {src}")
            if src and "cctv/image" in src:
                full_url = src if src.startswith("http") else f"https://cwwp2.dot.ca.gov{src}"
                image_urls.append(full_url)

        print(f"[INFO] Found {len(image_urls)} valid CCTV image URLs")
        return image_urls
    finally:
        driver.quit()