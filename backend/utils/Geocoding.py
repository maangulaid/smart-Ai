import requests

def get_coordinates_from_zip(zip_code: str):
    try:
        response = requests.get(f"http://api.zippopotam.us/us/{zip_code}")
        if response.status_code == 200:
            data = response.json()
            place = data["places"][0]
            return float(place["latitude"]), float(place["longitude"])
        else:
            print(f"Zippopotam API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Failed to get coordinates: {e}")
        return None
