import pandas as pd
from pathlib import Path

# Define file paths relative to the script's location
SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DATA_DIR = SCRIPT_DIR.parent / "data" / "transformed"
CLEANED_DATAFRAME = SOURCE_DATA_DIR / "cleaned_dataframe.csv"
AVERAGE_WAIT_FILE = SOURCE_DATA_DIR.parent / "outputs" / "average_wait.csv"
MAP_FILE = SOURCE_DATA_DIR.parent / "outputs" / "map_dataframe.csv"
BY_COUNTRY_FILE = SOURCE_DATA_DIR.parent / "outputs" / "parks_by_country.csv"
BY_CONTINENT_FILE = SOURCE_DATA_DIR.parent / "outputs" / "parks_by_continent.csv"
MAX_WAIT_FILE = SOURCE_DATA_DIR.parent / "outputs" / "max_wait_time_per_continent.csv"

# Ensure output directory exists
AVERAGE_WAIT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Create separate dataframe to display map
def create_map_dataframe():
    """Create a map dataframe."""
    try:
        # Read the cleaned dataframe
        df = pd.read_csv(CLEANED_DATAFRAME)
    except FileNotFoundError:
        print(f"Error: {CLEANED_DATAFRAME} not found.")
        return
    # Drop unnecessary columns
    map_df = df.drop(columns=['ride_id', 'ride_name', 'wait_time', 'is_open', 'park_name', 'country', 'continent', 'date'])
    # Remove duplicates
    map_df = map_df.drop_duplicates(subset=['park_id'])
    # Save to CSV
    map_df.to_csv(MAP_FILE, index=False)
    print(f"Map dataframe saved to {MAP_FILE}")

# Add average wait by ride field, for the rides that are open
def add_average_wait_by_ride():
    """Add average wait time by ride."""
    try:
        # Read the cleaned dataframe
        df = pd.read_csv(CLEANED_DATAFRAME)
    except FileNotFoundError:
        print(f"Error: {CLEANED_DATAFRAME} not found.")
        return
    # Filter for open rides
    open_ride_records = df[df['is_open']].copy()
    open_rides = open_ride_records.filter(['ride_id', 'wait_time'])
    # Group by ride_id and calculate average wait time
    avg_wait_by_ride = open_rides.groupby('ride_id').agg(
        avg_wait_time=('wait_time', 'mean')
        )
    # Convert avg_wait_time to int
    avg_wait_by_ride['avg_wait_time'] = avg_wait_by_ride['avg_wait_time'].astype('int64')
    # Merge with the original dataframe
    avg_wait_by_ride = open_ride_records.merge(avg_wait_by_ride, on='ride_id', how='left')
    # Remove duplicates
    avg_wait_by_ride = avg_wait_by_ride.drop_duplicates(subset=['ride_id'])
    # Drop unnecessary columns
    avg_wait_by_ride = avg_wait_by_ride.drop(columns=['wait_time', 'is_open', 'latitude', 'longitude', 'date'])
    # Save to CSV
    avg_wait_by_ride.to_csv(AVERAGE_WAIT_FILE, index=False)
    print(f"Enriched dataframe saved to {AVERAGE_WAIT_FILE}")


# Create separate dataframe with count of parks by countries
# Also display continent to allow filtering on the page
def parks_count_by_country():
    """Count the number of parks by country."""
    try:
        # Read the cleaned dataframe
        df = pd.read_csv(CLEANED_DATAFRAME)
    except FileNotFoundError:
        print(f"Error: {CLEANED_DATAFRAME} not found.")
        return
    # Count the number of parks by country
    parks_count = df.groupby(['country', 'continent']).agg(
        num_of_parks=('park_id', 'nunique')
    ).reset_index()
    # Save to CSV
    parks_count.to_csv(BY_COUNTRY_FILE, index=False)
    print(f"Parks count by country dataframe saved to {BY_COUNTRY_FILE}")


# Create separate dataframe with count of parks vy continent
def parks_count_by_continent():
    """Count the number of parks by continent."""
    try:
        # Read the cleaned dataframe
        df = pd.read_csv(CLEANED_DATAFRAME)
    except FileNotFoundError:
        print(f"Error: {CLEANED_DATAFRAME} not found.")
        return
    # Count the number of parks by continent
    parks_count = df.groupby('continent').agg(
        num_of_parks=('park_id', 'nunique')
    ).reset_index()
    # Save to CSV
    parks_count.to_csv(BY_CONTINENT_FILE, index=False)
    print(f"Parks count by continent dataframe saved to {BY_CONTINENT_FILE}")


# Create separate dataframe with the longest ride wait times per continent
def max_wait_time_per_continent():
    """Get the longest ride wait times per continent."""
    try:
        # Read the cleaned dataframe
        df = pd.read_csv(CLEANED_DATAFRAME)
    except FileNotFoundError:
        print(f"Error: {CLEANED_DATAFRAME} not found.")
        return
    # Get the longest ride wait times per continent
    max_wait_time_per_continent = df.loc[
        df.groupby("continent")["wait_time"].idxmax()
    ]
    max_wait_time_per_continent = max_wait_time_per_continent.drop(columns=[
        'ride_id',
        'latitude',
        'longitude',
        'park_id',
        'is_open'
    ])
    max_wait_time_per_continent = max_wait_time_per_continent.set_index('continent')
    # Save to CSV
    max_wait_time_per_continent.to_csv(MAX_WAIT_FILE, index=True)
    print(f"Max wait per continent dataframe saved to {MAX_WAIT_FILE}")


# Main function for enrichment
def main():
    create_map_dataframe()
    add_average_wait_by_ride()
    parks_count_by_country()
    parks_count_by_continent()
    max_wait_time_per_continent()
    print("Data transformation for visualisation completed.")


if __name__ == "__main__":
    main()
