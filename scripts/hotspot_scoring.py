# Calculate a composite "hotspot score" for each city based on courts, tournaments, and players.
# Normalize each feature and average them for scoring and save a dataset with scores for further analysis and visualization.

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Load merged data
df = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data.csv")

# Feature engineering
df["courts_per_10k"] = df["Courts"] / df["population"] * 10000

# Fill missing with 0 to avoid issues in scoring
score_features = ["Courts", "num_tournaments", "total_players", "courts_per_10k"]
df[score_features] = df[score_features].fillna(0)

# Normalize features
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df[score_features])
df_scaled = pd.DataFrame(df_scaled, columns=[f"scaled_{col}" for col in score_features])

# Add scaled columns back to original df
df = pd.concat([df, df_scaled], axis=1)

# Create composite hotspot score
df["hotspot_score"] = df[[f"scaled_{col}" for col in score_features]].mean(axis=1)

# Top cities by score
top_hotspots = df.sort_values("hotspot_score", ascending=False).head(10)

# green palette
green_palette = ["#4c9a2a", "#57a637", "#62b244", "#6ebf51", "#79cb5e", "#85d76b", "#90e378", "#9cef85", "#a7fb92", "#b2ffa0"]

# Bar graph of the top 10 cities by hotspot score
plt.figure(figsize=(12, 8))
sns.barplot(data=top_hotspots, x="hotspot_score", y="city_state", palette=green_palette)
plt.title("Top 10 Pickleball Hotspot Cities")
plt.xlabel("Hotspot Score")
plt.ylabel("City")
plt.tight_layout()
plt.show()

# Export final data with score
df.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data_with_score.csv", index=False)
print(top_hotspots[["city_state", "hotspot_score"]])
