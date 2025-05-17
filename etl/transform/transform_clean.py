import pandas as pd
from pathlib import Path

# Define file paths relative to the script's location
SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DATA_DIR = SCRIPT_DIR.parent / "data" / "transformed"
ORIGINAL_DATAFRAME = SOURCE_DATA_DIR / "merged_parks_and_rides.csv"
CLEANED_FILE = SOURCE_DATA_DIR / "cleaned_dataframe.csv"

# Ensure output directory exists
CLEANED_FILE.parent.mkdir(parents=True, exist_ok=True)


def clean_dataframe():
    """Clean the merged dataframe."""
    try:
        # Read the original dataframe
        df = pd.read_csv(ORIGINAL_DATAFRAME)
    except FileNotFoundError:
        print(f"Error: {ORIGINAL_DATAFRAME} not found.")
        return

    # Drop unnecessary columns
    df = df.drop(columns=['company_id', 'company_name', 'timezone', 'timestamp', 'land_name', 'land_id'])

    # Change data types
    df = df.astype({
        'park_id': 'int64',
        'park_name': 'string',
        'ride_id': 'int64',
        'ride_name': 'string',
        'is_open': 'bool',
        'wait_time': 'int64',
        'country': 'string',
        'continent': 'string',
        'latitude': 'float64',
        'longitude': 'float64'
    })
    return df


# Transform the date to a more readable format 
def transform_date_num(dt):
    """Transform the date number to include suffix"""
    day = dt.day
    if 11 <= day <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return f"{day}{suffix} {dt.strftime('%B %Y')}"


def format_date(df):
    """Format the date string to a more readable format."""
    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')

    df['date'] = df['last_updated'].apply(
        lambda dt: transform_date_num(dt) 
        if pd.notnull(dt) 
        else None
        )

    df = df.drop(columns=['last_updated']) # Drop the original last_updated column as no longer needed
    return df


# Save the cleaned dataframe to a CSV file
def save_dataframe(df):
    """Save transformed dataframe"""
    try:
        df.to_csv(CLEANED_FILE, index=False)
        print(f"Cleaned dataframe saved to {CLEANED_FILE}")
    except Exception as e:
        print(f"Error saving cleaned dataframe: {e}")
        return


# Main function for cleaning
def main():
    df = clean_dataframe()
    df = format_date(df)
    save_dataframe(df)


if __name__ == "__main__":
    main()
