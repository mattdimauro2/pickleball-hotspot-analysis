# Analyze state-level Google Trends metrics and create a 1x3 visualization that includes search interest distributions, averages, and correlations with composite scores.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
trends = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_google_trends.csv")
cities = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data_with_composite_score.csv")

# Prepare the data
trends['state'] = trends['state'].str.upper()
cities['state'] = cities['city_state'].str.split(', ').str[1]

# Merge the state average scores
state_scores = cities.groupby("state")[["composite_score"]].mean().reset_index()
trends_merged = pd.merge(trends, state_scores, on="state", how="left")

# Melt for long format
trend_long = trends_merged.melt(
    id_vars=["state", "composite_score"],
    value_vars=[
        'pickleball_interest', 'pickleball_court_interest', 'pickleball_lessons_interest',
        'pickleball_near_me_interest', 'pickleball_tournament_interest', 'ppa_tour_interest'
    ],
    var_name="term",
    value_name="interest"
)

# Get the correlation by term
correlations = trend_long.groupby("term").apply(
    lambda g: g["interest"].corr(g["composite_score"])
).sort_values(ascending=False)

# Plot 1x3 layout
fig, axs = plt.subplots(1, 3, figsize=(24, 6))
fig.suptitle("Google Trends Pickleball Hotspots", fontsize=20, y=1.05)

# Boxplot - Distribution of Google Search Interest by Term
sns.boxplot(data=trend_long, x='term', y='interest', color="#4CAF50", ax=axs[0])
axs[0].set_title("Distribution of Google Search Interest by Term")
axs[0].set_xlabel("Search Term")
axs[0].set_ylabel("Search Interest")
axs[0].tick_params(axis='x', rotation=45)

# Barplot of average interest
avg_interest = trend_long.groupby("term")["interest"].mean().sort_values(ascending=False)
sns.barplot(x=avg_interest.values, y=avg_interest.index, color="#4CAF50", ax=axs[1])
axs[1].set_title("Average Google Search Interest by Term")
axs[1].set_xlabel("Average Interest")
axs[1].set_ylabel("")

# Correlation by Term
sns.barplot(x=correlations.values, y=correlations.index,color="#4CAF50", ax=axs[2])
axs[2].set_title("Correlation of Search Terms with Composite Score")
axs[2].set_xlabel("Correlation")
axs[2].set_ylabel("Search Term")

# Save the visualization
plt.tight_layout()
plt.savefig("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\visualizations\\google_trends_visualization.png", dpi=300)
plt.close()