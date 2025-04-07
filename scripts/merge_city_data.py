# Merge the cleaned Census, court, and tournament datasets at the city level, and add counts for tournaments, players, large tournaments, and major events.

import pandas as pd

# Load the datasets
census_cities = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\census_city_data_2023_cleaned.csv")
courts = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\courts_cleaned.csv")
tournaments = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\tournaments_cleaned.csv")

# Standardize the city_state key across all datasets
courts["city_state"] = courts["City"] + ", " + courts["State"]
tournaments["city_state"] = tournaments["City"] + ", " + tournaments["State"]

# Add the major flag, large tournament flag, and aggregate tournaments by city_state
tournaments["is_large_tournament"] = tournaments["Players"] > 250  # Define large as >250 players
tournaments_agg = tournaments.groupby("city_state").agg(
    num_tournaments=("Tournament Name", "count"),           # Total number of tournaments
    total_players=("Players", "sum"),        # Sum of players across all tournaments
    large_tournaments=("is_large_tournament", "sum"),       # Count of tournaments >250 players
    major_tournaments=("is_major_tournament", "sum")        # Count of major tournaments (based on is_major flag)
).reset_index()

# Merge the datasets
# Use left join on census_cities to keep all Census cities
merged_city_data = (census_cities
                    .merge(courts[["city_state", "Locations", "Courts"]],
                           on="city_state", how="left")
                    .merge(tournaments_agg[["city_state", "num_tournaments", "total_players", "large_tournaments", "major_tournaments"]],
                           on="city_state", how="left"))

# Clean up missing values
# Fill NaN with 0 for counts where there are no courts or tournaments
columns_to_fill = ["Locations", "Courts", "num_tournaments", "total_players", "large_tournaments", "major_tournaments"]
merged_city_data[columns_to_fill] = merged_city_data[columns_to_fill].fillna(0)

# Ensure integer types for counts
for col in columns_to_fill:
    merged_city_data[col] = merged_city_data[col].astype(int)

# Save to CSV
merged_city_data.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data.csv", index=False)
print(merged_city_data.head())