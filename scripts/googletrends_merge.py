# Consolidate the google trends 'map' files into one csv called "merged_google_trends.csv" that calculates an average interest score across all terms.

import pandas as pd
import os

# Folder containing all the trend CSVs
trends_folder = "C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\Google_Trends"

# Initialize an empty list to store each term's DataFrame
trend_dfs = []

# Loop through files in the folder
for filename in os.listdir(trends_folder):
    if filename.endswith("_map_cleaned.csv"):
        term = filename.replace("_map_cleaned.csv", "")
        path = os.path.join(trends_folder, filename)

        # Read the file and rename 'interest' column to the term name
        df = pd.read_csv(path)
        df = df[["state", "interest"]].copy()
        df.rename(columns={"interest": f"{term}_interest"}, inplace=True)

        trend_dfs.append(df)

# Merge all DataFrames on state field
from functools import reduce
merged_trends = reduce(lambda left, right: pd.merge(left, right, on="state", how="outer"), trend_dfs)

# Calculate average interest score across all terms
interest_cols = [col for col in merged_trends.columns if col.endswith("_interest")]
merged_trends["avg_interest"] = merged_trends[interest_cols].mean(axis=1)

# Export to CSV
merged_trends.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_google_trends.csv", index=False)

# Preview
print(merged_trends.head())