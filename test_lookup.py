# backend/test_lookup.py

from utils.local_zip_lookup import load_zip_data_github, lookup_zip

RAW_CSV_URL = "https://raw.githubusercontent.com/maangulaid/dataset-for-smart-ai-california/main/uszips.csv"

# Load from GitHub
zip_data = load_zip_data_github(RAW_CSV_URL)

# Test ZIP code
zip_code = "75080"
info = lookup_zip(zip_code, zip_data)

# Show result
if info:
    print(f"[FOUND] ZIP {zip_code}: {info}")
else:
    print(f"[NOT FOUND] ZIP {zip_code}")
