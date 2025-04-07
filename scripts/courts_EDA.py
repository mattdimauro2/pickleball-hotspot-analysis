# EDA on the courts_combined.csv file to verify integrity, handle zero court counts, and standardize state names to abbreviations.

import pandas as pd

# Load the combined court data
courts = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\courts_combined.csv")
print("Court data preview:")
print(courts.head())

# Display data structure
print("\nColumn info:")
print(courts.info())

# Check for any missing values
print("\nMissing values:")
print(courts.isnull().sum())

# Review the minimum number of locations and courts across all cities
print("\nMinimum values:")
print(courts[["Locations", "Courts"]].min())

# Check for any negative values
print("\nAny negative values?")
print((courts[["Locations", "Courts"]] < 0).sum())

# Check for zero values
print("\nAny zero values?")
print((courts[["Locations", "Courts"]] == 0).sum())

# Impute missing court counts by assuming each location has at least 2 courts
courts.loc[courts["Courts"] == 0, "Courts"] = courts["Locations"] * 2

# Re-check the fix
print("\nMinimum court count after fix:", courts["Courts"].min())
print("Any cities with 0 courts left?", (courts["Courts"] == 0).sum())

# View all unique state names
print("\nUnique state names before standardizing:")
print(courts["State"].unique())

# Dictionary to map full state names to abbreviations
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

# Apply the mapping to the State column
courts["State"] = courts["State"].map(state_mapping)

# Check results of mapping
print("\nUnique state abbreviations after mapping:")
print(courts["State"].unique())
print("\nAny missing states after mapping?")
print(courts["State"].isnull().sum())

# Top 10 cities with the most locations
print("\nTop 10 cities with the most locations:")
print(courts.sort_values("Locations", ascending=False).head(10))

# Top 10 cities with the most courts
print("\nTop 10 cities with the most courts:")
print(courts.sort_values("Courts", ascending=False).head(10))

# Save cleaned data
courts.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\courts_cleaned.csv", index=False)