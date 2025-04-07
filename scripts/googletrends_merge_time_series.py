# Consolidate the google trends 'trend' files (time-based) into one time series csv called "merged_google_trend_time.csv" with one row per date and separate columns for each term's interest score.

import pandas as pd
import os

# Folder containing all time trend files
trends_folder = "C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\Google_Trends"

# Initialize an empty list
trend_dfs = []

# Loop through files in folder
for filename in os.listdir(trends_folder):
    if filename.endswith("_trend_cleaned.csv"):
        term = filename.replace("_trend_cleaned.csv", "")
        path = os.path.join(trends_folder, filename)

        df = pd.read_csv(path)
        df.rename(columns={"interest": term}, inplace=True)  # Rename 'interest' to term
        trend_dfs.append(df)

# Merge all dataframes on 'date'
from functools import reduce
merged_trend_time = reduce(lambda left, right: pd.merge(left, right, on="date", how="outer"), trend_dfs)

# Convert date column to datetime
merged_trend_time["date"] = pd.to_datetime(merged_trend_time["date"])

# Sort by date
merged_trend_time = merged_trend_time.sort_values("date")

# Save to CSV
merged_trend_time.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_google_trend_time.csv", index=False)
print(merged_trend_time.head())