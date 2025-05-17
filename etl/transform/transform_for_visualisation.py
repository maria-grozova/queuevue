# Map
map_df = full_df.filter(['park_name', 'latitude', 'longitude'])
map_df = map_df.drop_duplicates(subset=['name', 'latitude', 'longitude'])
map_df = map_df.dropna(subset=['latitude', 'longitude'])

# Max time
max_wait_time_per_continent = full_df.loc[
    full_df.groupby("continent")["wait_time"].idxmax()
]
max_wait_time_per_continent = max_wait_time_per_continent.drop(columns=['ride_id', 'latitude', 'longitude', 'timezone', 'company_id', 'company_name', 'park_id', 'timestamp', 'is_open', 'last_updated'])
max_wait_time_per_continent = max_wait_time_per_continent.set_index('continent')
# Display the result
max_wait_time_per_continent.to_csv('max_wait_time_per_continent.csv', index=True)