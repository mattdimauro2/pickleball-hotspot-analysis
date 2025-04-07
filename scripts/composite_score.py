# Combine hotspot score and random forest major tournament probability into one composite metric.
# Identify the top 10 cities by composite score.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the file that contains the RF probability column
df = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data_with_score.csv")

# Normalize hotspot_score and rf_major_prob to [0, 1]
hotspot_scaled = (df["hotspot_score"] - df["hotspot_score"].min()) / (df["hotspot_score"].max() - df["hotspot_score"].min())
rf_scaled = (df["rf_major_prob"] - df["rf_major_prob"].min()) / (df["rf_major_prob"].max() - df["rf_major_prob"].min())

# Calculate composite score with equal weighting
df["composite_score"] = (hotspot_scaled + rf_scaled) / 2

# Save the csv with the composite scores
df.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data_with_composite_score.csv", index=False)

# Show top 10 cities by composite score
top_composite = df.sort_values("composite_score", ascending=False).head(10)
print(top_composite[["city_state", "composite_score", "hotspot_score", "rf_major_prob"]])

# Visualize top composite cities
plt.figure(figsize=(12, 6))
sns.barplot(data=top_composite, x="composite_score", y="city_state", color="#4CAF50")
plt.title("Top 10 Cities by Composite Score (Hotspot + Major Potential)")
plt.xlabel("Composite Score")
plt.ylabel("City")
plt.tight_layout()
plt.savefig("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\visualizations\\composite_score_bar_chart.png")
plt.close()