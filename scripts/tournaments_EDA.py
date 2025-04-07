# EDA on the tournaments_cleaned.csv file to verify integrity and handle tournaments with zero players.


import pandas as pd
import matplotlib.pyplot as plt

# Load and preview the cleaned tournaments data
tournaments_df = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\tournaments_cleaned.csv")
tournaments_df["Start Date"] = pd.to_datetime(tournaments_df["Start Date"], errors="coerce")
print("Tournaments data preview:")
print(tournaments_df.head())

# Basic Overview
print("\nColumn info:")
print(tournaments_df.info())

# Check for any negative values in players
print("\nAny negative values?")
print((tournaments_df["Players"] < 0).sum())

# Check for any zero values
print("\nAny zero values?")
print((tournaments_df["Players"] == 0).sum())

# Check for any missing values
print("\nMissing values:")
print(tournaments_df.isnull().sum())

# Top 10 States by Tournament Count
top_states = tournaments_df["State"].value_counts().head(10)
print("Top 10 States by Tournament Count:")
print(top_states)

# Distribution of Player Counts
tournaments_df["Players"].plot(kind="hist", bins=30, edgecolor="black", figsize=(10, 5))
plt.title("Distribution of Tournament Player Counts")
plt.xlabel("Number of Players")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# Large Tournaments Count by State
large_tournaments = tournaments_df[tournaments_df["is_large_tournament"]]
large_counts = large_tournaments["State"].value_counts().head(10)
print("States with Most Large Tournaments (Players > 250):")
print(large_counts)

# Tournaments Over Time
tournaments_df["Month"] = tournaments_df["Start Date"].dt.to_period("M")
monthly_counts = tournaments_df.groupby("Month").size()

monthly_counts.plot(kind="line", marker="o", figsize=(12, 5))
plt.title("Tournaments Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Tournaments")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Major Tournament Locations
major_df = tournaments_df[tournaments_df["is_major_tournament"]]
major_locations = major_df["State"].value_counts().head(10)
print("Top States for Major Tournaments:")
print(major_locations)

# Check to see if any tournaments have 0 players
num_zero_player_tournaments = (tournaments_df["Players"] == 0).sum()
print(f"Tournaments with 0 players: {num_zero_player_tournaments}")

# Mapping the number of tournaments by month
#  Extract month name from start date
tournaments_df["Month"] = tournaments_df["Start Date"].dt.month_name()

# Count tournaments by month
monthly_counts = tournaments_df["Month"].value_counts().reindex([
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
], fill_value=0)

# Plot
plt.figure(figsize=(10, 6))
monthly_counts.plot(kind="line", color="mediumseagreen")
plt.title("Number of Pickleball Tournaments by Month (2024)")
plt.xlabel("Month")
plt.ylabel("Number of Tournaments")
plt.xticks(rotation=45)
plt.tight_layout()

# Save plot
plt.savefig("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\visualizations\\tournaments_by_month.png")
plt.close()