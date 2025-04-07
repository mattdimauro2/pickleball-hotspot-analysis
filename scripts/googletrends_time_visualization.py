# Visualize Google Trends time series for pickleball-related terms - includes smoothed trends, seasonal patterns, and normalized growth since 2021.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Load and reshape the data
df = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_google_trend_time.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.melt(id_vars="date", var_name="term", value_name="interest")
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

# Define term groups
group1 = ["pickleball", "pickleball_tournament", "ppa_tour"]
group1a = ["pickleball", "pickleball_tournament"]
group2 = ["pickleball_near_me", "pickleball_lessons", "pickleball_court"]
group3 = ["ppa_tour"]

# Palettes
green_palette = ["#2e7d32", "#4caf50", "#81c784"]
lighter_palette = ["#81c784", "#aed581", "#c8e6c9"]

# Setup 2x4 plot
fig, axs = plt.subplots(2, 4, figsize=(18, 10))
fig.suptitle("Google Trends Over Time", fontsize=18, y=0.98)

# Smoothed Search Interest (Group 1)
for term, color in zip(group1, green_palette):
    subset = df[df["term"] == term].copy()
    subset = subset.sort_values("date")
    subset["smoothed"] = subset["interest"].rolling(window=4, min_periods=1).mean()
    axs[0, 0].plot(subset["date"], subset["smoothed"], label=term.replace("_", " ").title(), color=color)
axs[0, 0].set_title("Smoothed Search Interest (Group 1)")
axs[0, 0].set_ylabel("Interest")
axs[0, 0].legend()
axs[0, 0].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# Smoothed Search Interest (Group 2)
for term, color in zip(group2, green_palette):
    subset = df[df["term"] == term].copy()
    subset = subset.sort_values("date")
    subset["smoothed"] = subset["interest"].rolling(window=4, min_periods=1).mean()
    axs[1, 0].plot(subset["date"], subset["smoothed"], label=term.replace("_", " ").title(), color=color)
axs[1, 0].set_title("Smoothed Search Interest (Group 2)")
axs[1, 0].set_ylabel("Interest")
axs[1, 0].legend()
axs[1, 0].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# Seasonal Patterns (Group 1)
group1_df = df[df["term"].isin(group1)]
sns.lineplot(data=group1_df, x="month", y="interest", hue="term", ax=axs[0, 1])
axs[0, 1].set_title("Seasonal Interest Patterns (Group 1)")
axs[0, 1].set_ylabel("Interest")
axs[0, 1].legend(title="Search Term")

# Seasonal Patterns (Group 2)
group2_df = df[df["term"].isin(group2)]
sns.lineplot(data=group2_df, x="month", y="interest", hue="term", ax=axs[1, 1])
axs[1, 1].set_title("Seasonal Interest Patterns (Group 2)")
axs[1, 1].set_ylabel("Interest")
axs[1, 1].legend(title="Search Term")

# Normalized YoY Growth (Group 1, excluding PPA)
yoy_data = []
for term in group1a:
    yearly_values = df[df["term"] == term].groupby("year")["interest"].mean()
    for y in [2021, 2022, 2023]:
        if y + 1 in yearly_values.index:
            pct_change = (yearly_values[y + 1] - yearly_values[y]) / yearly_values[y]
            yoy_data.append({"term": term, "period": f"{y}-{y+1}", "growth": pct_change})
yoy_df1 = pd.DataFrame(yoy_data)
sns.barplot(data=yoy_df1, x="period", y="growth", hue="term", palette=green_palette[:2], ax=axs[0, 2])
axs[0, 2].set_title("Normalized YoY Growth (Group 1)")
axs[0, 2].set_ylabel("Growth Rate")
axs[0, 2].legend(title="Search Term")
for bar in axs[0, 2].containers:
    axs[0, 2].bar_label(bar, labels=[f"{v.get_height() * 100:.1f}%" for v in bar], label_type="edge", padding=2)

# Normalized YoY Growth (PPA Tour)
yoy_data_group3 = []
for term in group3:
    yearly_values = df[df["term"] == term].groupby("year")["interest"].mean()
    for y in [2021, 2022, 2023]:
        if y + 1 in yearly_values.index:
            pct_change = (yearly_values[y + 1] - yearly_values[y]) / yearly_values[y]
            yoy_data_group3.append({"term": term, "period": f"{y}-{y+1}", "growth": pct_change})
yoy_df3 = pd.DataFrame(yoy_data_group3)
axs[0, 3].set_title("Normalized YoY Growth (PPA Tour)")
sns.barplot(data=yoy_df3, x="period", y="growth", hue="term", palette=green_palette, ax=axs[0, 3])
axs[0, 3].set_ylabel("Growth Rate")
axs[0, 3].legend(title="Search Term")
for bar in axs[0, 3].containers:
    axs[0, 3].bar_label(bar, labels=[f"{v.get_height() * 100:.1f}%" for v in bar], label_type="edge", padding=2)

# Normalized YoY Growth (Group 2)
yoy_data_group2 = []
for term in group2:
    yearly_values = df[df["term"] == term].groupby("year")["interest"].mean()
    for y in [2021, 2022, 2023]:
        if y + 1 in yearly_values.index:
            pct_change = (yearly_values[y + 1] - yearly_values[y]) / yearly_values[y]
            yoy_data_group2.append({"term": term, "period": f"{y}-{y+1}", "growth": pct_change})
yoy_df2 = pd.DataFrame(yoy_data_group2)
axs[1, 2].set_title("Normalized YoY Growth (Group 2)")
sns.barplot(data=yoy_df2, x="period", y="growth", hue="term", palette=green_palette, ax=axs[1, 2])
axs[1, 2].set_ylabel("Growth Rate")
axs[1, 2].legend(title="Search Term")
for bar in axs[1, 2].containers:
    axs[1, 2].bar_label(bar, labels=[f"{v.get_height() * 100:.1f}%" for v in bar], label_type="edge", padding=2)

# Save the visualization
fig.delaxes(axs[1, 3]) # remove the empty chart in bottom right
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\visualizations\\google_trends_time_series_visualization.png", dpi=300)
plt.close()
