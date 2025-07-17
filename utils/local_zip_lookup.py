# backend/utils/local_zip_lookup.py

import csv
import requests
from io import StringIO

def load_zip_data_github(raw_csv_url):
    """
    Downloads and parses ZIP code data CSV from a raw GitHub URL.
    Returns a dictionary: {ZIP: {city, state, lat, lng}}.
    """
    zip_lookup = {}
    try:
        response = requests.get(raw_csv_url)
        response.raise_for_status()
        csvfile = StringIO(response.text)
        reader = csv.DictReader(csvfile)
        for row in reader:
            zip_code = row['zip'].strip()
            zip_lookup[zip_code] = {
                'city': row['city'],
                'state': row.get('state_id') or row.get('state'),
                'lat': float(row['lat']),
                'lng': float(row['lng']),
            }
    except Exception as e:
        print(f"[ERROR] Failed to fetch or parse CSV: {e}")
    return zip_lookup

def lookup_zip(zipcode, zip_data=None):
    """
    Looks up a ZIP code in the zip_data dictionary.
    Pads the ZIP to 5 digits.
    """
    return zip_data.get(str(zipcode).zfill(5), None)



def get_coords_from_zip(zip_code, zip_data=None):
    if zip_data is None:
        zip_data = load_zip_data_github("https://raw.githubusercontent.com/maangulaid/dataset-for-smart-ai-california/main/uszips.csv")
    entry = lookup_zip(zip_code, zip_data)
    if entry:
        return entry["lat"], entry["lng"]
    return None
