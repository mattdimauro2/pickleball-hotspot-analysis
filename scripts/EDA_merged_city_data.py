# EDA for city-level pickleball trends
# Visualizes a 3x3 visualization pn court access, tournaments, and demographics across US cities

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load merged city data
df = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data.csv")

# Feature: Courts per 10k residents
df["courts_per_10k"] = df["Courts"] / df["population"] * 10000

# Set up consistent style and palettes
sns.set(style="whitegrid")

fig, axes = plt.subplots(3, 3, figsize=(20, 16))

# Top 10 cities by number of courts
top_courts = df.sort_values("Courts", ascending=False).head(10)
sns.barplot(data=top_courts, x="Courts", y="city_state", ax=axes[0, 0], color="#4CAF50")
axes[0, 0].set_title("Top 10 Cities by Number of Courts")
axes[0, 0].set_xlabel("Courts")
axes[0, 0].set_ylabel("")

# Top 10 cities by tournaments hosted
top_tournaments = df.sort_values("num_tournaments", ascending=False).head(10)
sns.barplot(data=top_tournaments, x="num_tournaments", y="city_state", ax=axes[0, 1], color="#4CAF50")
axes[0, 1].set_title("Top 10 Cities by Number of Tournaments")
axes[0, 1].set_xlabel("Tournaments")
axes[0, 1].set_ylabel("")

# Top cities by major tournaments hosted
top_majors = df[df["major_tournaments"] > 0].sort_values("major_tournaments", ascending=False).head(10)
sns.barplot(data=top_majors, x="major_tournaments", y="city_state", ax=axes[0, 2], color="#4CAF50")
axes[0, 2].set_title("Top Cities by Major Tournaments")
axes[0, 2].set_xlabel("Major Tournaments")
axes[0, 2].set_ylabel("")

# Scatter: Courts vs Population
sns.scatterplot(data=df, x="population", y="Courts", ax=axes[1, 0], color="#59a14f", alpha=0.6)
axes[1, 0].set_title("Courts vs Population")
axes[1, 0].set_xlabel("Population")
axes[1, 0].set_ylabel("Courts")

# Scatter: Courts vs Tournaments
sns.scatterplot(data=df, x="Courts", y="num_tournaments", ax=axes[1, 1], color="#59a14f", alpha=0.6)
axes[1, 1].set_title("Courts vs Tournaments")
axes[1, 1].set_xlabel("Courts")
axes[1, 1].set_ylabel("Tournaments")

# Violin Plot: Median income for cities with/without courts
df["has_courts"] = df["Courts"] > 0
sns.violinplot(data=df, x="has_courts", y="median_income", ax=axes[1, 2], palette=["#a7fb92", "#4c9a2a"])
axes[1, 2].set_title("Median Income by Court Presence")
axes[1, 2].set_xlabel("Has Courts")
axes[1, 2].set_ylabel("Median Income")

# Top cities by court saturation (courts per 10k residents)
top_saturation = df[df["population"] > 1000].sort_values("courts_per_10k", ascending=False).head(10)
sns.barplot(data=top_saturation, x="courts_per_10k", y="city_state", ax=axes[2, 0], color="#4CAF50")
axes[2, 0].set_title("Top Cities by Courts per 10k Residents")
axes[2, 0].set_xlabel("Courts per 10k")
axes[2, 0].set_ylabel("")

# Boxplot: Tournament player counts by population quartile
df["pop_quartile"] = pd.qcut(df["population"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
sns.boxplot(data=df, x="pop_quartile", y="total_players", ax=axes[2, 1], color="#4CAF50")
axes[2, 1].set_title("Tournament Players by Population Quartile")
axes[2, 1].set_xlabel("Population Quartile")
axes[2, 1].set_ylabel("Total Players")

# Correlation heatmap for numeric variables
numeric_df = df[["population", "median_income", "median_age", "Courts", "num_tournaments", "total_players"]]
corr = numeric_df.corr()
sns.heatmap(corr, annot=True, cmap="Greens", ax=axes[2, 2])
axes[2, 2].set_title("Correlation Heatmap")

# Final layout and export
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.suptitle("Pickleball Hotspot City EDA", fontsize=22, y=1.03)
plt.savefig("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\visualizations\\city_eda_visualization.png", dpi=300)
plt.close()