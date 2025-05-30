import requests
import json
from datetime import datetime, timezone
from pathlib import Path

PARKS_URL = "https://queue-times.com/parks.json"
QUEUE_TEMPLATE = "https://queue-times.com/parks/{}/queue_times.json"

# Define output paths (the use of Path was generated with the help of ChatGPT)
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PARKS_FILE = OUTPUT_DIR / "parks.json"
QUEUE_FILE = OUTPUT_DIR / "queue_times_log.jsonl"


# Fetch and save parks metadata
def save_parks_metadata():
    if PARKS_FILE.exists():
        print("Parks metadata already exists. Skipping download.")
        return

    try:
        response = requests.get(PARKS_URL, timeout=10)
        response.raise_for_status()  # raises HTTPError for 4xx/5xx responses
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for parks metadata file: {e}")
            return

        with open(PARKS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print("Saved original parks.json data.")
    except requests.RequestException as e:
        print(f"Error fetching parks metadata: {e}")
        raise


# Get current queue times for one park and return JSON with timestamp
def get_queue_times_for_park(park_id):
    url = QUEUE_TEMPLATE.format(park_id)
    response = requests.get(url, timeout=10)
    data = response.json()
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "park_id": park_id,
        "data": data
    }


# Fetch and append queue times to JSONL file
def update_queue_times():
    with open(PARKS_FILE, "r", encoding="utf-8") as f:
        parks_data = json.load(f)

    park_ids = []
    for organization in parks_data:
        if "parks" in organization:
            park_ids.extend([park["id"] for park in organization["parks"]])

    print(f"Total parks found: {len(park_ids)}")
    print(f"Park IDs: {park_ids}")

    print("Fetching queue times")

    with open(QUEUE_FILE, "a", encoding="utf-8") as f:
        for park_id in park_ids:
            record = get_queue_times_for_park(park_id)
            f.write(json.dumps(record) + "\n")

        print(f"Appended data at {datetime.now(timezone.utc).isoformat()}")


def main():
    save_parks_metadata()
    update_queue_times()


if __name__ == "__main__":
    main()
