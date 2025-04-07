"""
Google Trends - Trend Data Cleaning and Exploration
I focused on 6 key-words in google trends: "pickleball", "pickleball tournament", "pickleball court", "pickleball lessons", "pickleball near me", and "ppa tour"
The filters I used in Google Trends were "United States" and "previous 5 years".
Each CSV contains weekly interest over time.
This script focuses on cleaning the trend time series (not map data), standardizing column names, checking for missing values, and saving cleaned versions of each file.
"""
import pandas as pd

# List of Trends terms
terms = [
    "pickleball",
    "pickleball_tournament",
    "pickleball_court",
    "pickleball_lessons",
    "ppa_tour",
    "pickleball_near_me"
]

# Loop through each term
for term in terms:
    # Load the trend file
    file_path = f"C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\Google_Trends/{term}_trend.csv"
    trends_time = pd.read_csv(file_path, skiprows=1)
    print(f"\nPreview of {term}_trend before cleaning:")
    print(trends_time.head())

    # Identify the interest score column (non-date column) – usually the term itself
    interest_col = [col for col in trends_time.columns if col != "Week"][0]
    print(f"Interest column for {term}: {interest_col}")

    # Rename columns
    trends_time = trends_time.rename(columns={"Week": "date", interest_col: "interest"})

    # Check the cleaned data
    print(f"Preview of {term}_trend after cleaning:")
    print(trends_time.head())
    print(f"Missing values in {term}:")
    print(trends_time.isnull().sum())

    # Save the cleaned file
    trends_time.to_csv(f"C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\Google_Trends/{term}_trend_cleaned.csv", index=False)