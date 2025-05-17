import pandas as pd
import json
from pathlib import Path

# Define file paths relative to the script's location
SCRIPT_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"
PARKS_FILE = RAW_DATA_DIR / "parks.json"
QUEUE_TIMES_FILE = RAW_DATA_DIR / "queue_times_log.jsonl"
MERGED_FILE = RAW_DATA_DIR.parent / "transformed" / "merged_parks_and_rides.csv"

# Ensure output directory exists
MERGED_FILE.parent.mkdir(parents=True, exist_ok=True)


def transform_parks():
    """Transform parks data into a dataframe."""
    try:
        with open(PARKS_FILE, "r") as f:
            parks_data = json.load(f)

        parks_df = pd.json_normalize(
            parks_data,
            record_path="parks",
            meta=["id", "name"],
            meta_prefix="company_"
        )
        # Rename columns for clarity
        parks_df.rename(columns={"id": "park_id", "name": "park_name"}, inplace=True)
        # Set index to park_id
        parks_df.set_index("park_id", inplace=True)

        return parks_df
    except FileNotFoundError:
        print(f"Error: {PARKS_FILE} not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {PARKS_FILE}: {e}")


def transform_queue_times():
    """Transform queue times data into a dataframe."""
    try:
        df_raw = pd.read_json(QUEUE_TIMES_FILE, lines=True)
        records = []

        for _, row in df_raw.iterrows():
            timestamp = row["timestamp"]
            park_id = row["park_id"]
            data = row["data"]

            if data["lands"] == []:
                for ride in data.get("rides", []):
                    record = {
                        "timestamp": timestamp,
                        "park_id": park_id,
                        "ride_id": ride.get("id"),
                        "ride_name": ride.get("name"),
                        "is_open": ride.get("is_open"),
                        "wait_time": ride.get("wait_time"),
                        "last_updated": ride.get("last_updated"),
                        "land_id": None,
                        "land_name": None
                    }
                    records.append(record)
            else:
                for land in data.get("lands", []):
                    land_id = land.get("id")
                    land_name = land.get("name")
                    for ride in land.get("rides", []):
                        record = {
                            "timestamp": timestamp,
                            "park_id": park_id,
                            "ride_id": ride.get("id"),
                            "ride_name": ride.get("name"),
                            "is_open": ride.get("is_open"),
                            "wait_time": ride.get("wait_time"),
                            "last_updated": ride.get("last_updated"),
                            "land_id": land_id,
                            "land_name": land_name
                        }
                        records.append(record)

        df_rides = pd.DataFrame(records)
        return df_rides
    except FileNotFoundError:
        print(f"Error: {QUEUE_TIMES_FILE} not found.")
    except ValueError as e:
        print(f"Error reading JSON in {QUEUE_TIMES_FILE}: {e}")


def merge_dataframes(df_parks, df_rides):
    """Merge parks and rides dataframes."""
    if df_parks.empty or df_rides.empty:
        print("Error: One or both dataframes are empty. Cannot merge.")
        return

    merged_df = pd.merge(df_rides, df_parks, on="park_id", how="left")
    merged_df.to_csv(MERGED_FILE, index=False)
    print(f"Merged dataframe saved to {MERGED_FILE}")


def main():
    df_parks = transform_parks()
    df_rides = transform_queue_times()
    merge_dataframes(df_parks, df_rides)


if __name__ == "__main__":
    main()