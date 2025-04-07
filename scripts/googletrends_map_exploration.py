"""
Google Trends - Map Data Cleaning Exploration
I focused on 6 key-words in google trends: "pickleball", "pickleball tournament", "pickleball court", "pickleball lessons", "pickleball near me", and "ppa tour"
The filters I used in Google Trends were "United States" and "previous 5 years".
Each file contains relative interest by US state.
This script standardizes column names, converts full state names to abbreviations, fills missing interest values with 0 for low-volume states, and saves clean versions of each file
"""
import pandas as pd

# List of Trends terms I explored
terms = [
    "pickleball",
    "pickleball_tournament",
    "pickleball_court",
    "pickleball_lessons",
    "ppa_tour",
    "pickleball_near_me"
]

# State mapping dictionary with DC
state_mapping = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC"
}

# Loop through each term
for term in terms:
    # Load the map file
    file_path = f"C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\Google_Trends/{term}_map.csv"
    trends_map = pd.read_csv(file_path, skiprows=2)
    print(f"\nPreview of {term}_map before cleaning:")
    print(trends_map.head())

    # Get the interest column dynamically
    interest_col = [col for col in trends_map.columns if col != "Region"][0]
    print(f"Interest column for {term}: {interest_col}")

    # Rename columns
    trends_map = trends_map.rename(columns={"Region": "state", interest_col: "interest"})

    # Convert full state names to abbreviations
    trends_map["state"] = trends_map["state"].map(state_mapping)

    # Google Trends returns blanks for low-volume searches, so I replaced with a 0 to retain state coverage
    trends_map["interest"] = trends_map["interest"].fillna(0)

    # Check the cleaned data
    print(f"Preview of {term}_map after cleaning:")
    print(trends_map.head())
    print(f"Missing values in {term}:")
    print(trends_map.isnull().sum())
    print(f"Unique states in {term}:")
    print(trends_map["state"].unique())

    # Save the cleaned file
    trends_map.to_csv(f"C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\Google_Trends/{term}_map_cleaned.csv", index=False)