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
    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
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
    try:
        df['date'] = df['last_updated'].apply(format_date)
        if pd.isnull(dt):
            return None
        return df
    except ValueError:
        return None