# Analyze why Atlantic City failed as a major pickleball tournament location, using monthly tournament data, Google Trends, and a demographic comparison with top cities.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Load cleaned datasets
tournaments = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\tournaments_cleaned.csv")
city_data = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data_with_composite_score.csv")
trend = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\Google_Trends\\pickleball_tournament_trend_cleaned.csv")

# Count number of tournaments by month
tournaments['Start Date'] = pd.to_datetime(tournaments['Start Date'])
tournaments['month'] = tournaments['Start Date'].dt.month_name()
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_counts = tournaments['month'].value_counts().reindex(month_order)

# Google Trends — Filter for 2023 data and flag February
trend['date'] = pd.to_datetime(trend['date'])
trend = trend[trend['date'].dt.year == 2023]
trend['month'] = trend['date'].dt.month
feb_mask = trend['month'] == 2

# Extract Jersey City and top 20 cities by composite score
atlantic = city_data[city_data['city_state'] == "Atlantic City, NJ"].copy()
top_cities = city_data.sort_values('composite_score', ascending=False).head(20)

# Normalize demographics for comparison
features = ['median_income', 'population', 'median_age']
scaler = MinMaxScaler()
top_scaled = pd.DataFrame(scaler.fit_transform(top_cities[features]), columns=features)
top_avg_scaled = top_scaled.mean()
jersey_scaled = pd.Series(scaler.transform(atlantic[features])[0], index=features)

# Colors
single_green = "#59a14f"       # one clean mid-tone green
highlight_feb = "#e1e5d3"      # soft neutral background highlight
line_color = "#2e7d32"         # dark green for line chart
jersey_color = "#b0413e"       # muted red
top20_color = "#81c784"        # soft green for top cities

# Create the figure and axes
fig, axs = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("Analysis: Why Atlantic City Failed as a Pickleball Tournament Location", fontsize=18)

# Tournaments by Month (single green)
sns.barplot(x=monthly_counts.index, y=monthly_counts.values, ax=axs[0], color=single_green)
axs[0].set_title("Total Tournaments by Month")
axs[0].set_ylabel("Number of Tournaments")
axs[0].tick_params(axis='x', rotation=45)
axs[0].axvspan(0.5, 1.5, color=highlight_feb, alpha=0.5, label="February")
axs[0].legend()

# Google Trends for "Pickleball Tournament" (2023)
axs[1].plot(trend['date'], trend['interest'], label="Search Interest", color=line_color)
axs[1].set_title("Google Trends (2023): 'Pickleball Tournament'")
axs[1].set_ylabel("Interest")
axs[1].set_xlabel("Date")
axs[1].fill_between(trend['date'], trend['interest'], where=feb_mask, color="#fbeec1", alpha=0.4, label="February")
axs[1].legend()

# Atlantic City Demographics vs Top 20 Cities (Normalized)
for f in features:
    axs[2].barh(f, jersey_scaled[f], color=jersey_color, label='Atlantic City' if f == features[0] else "")
    axs[2].barh(f, top_avg_scaled[f], left=0, color=top20_color, alpha=0.6, label='Top 20 Avg' if f == features[0] else "")
axs[2].set_title("Atlantic City Demographics vs Top 20 (Normalized)")
axs[2].set_xlim(0, 1)
axs[2].legend()

# Save chart
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\visualizations\\atlantic_city_analysis_visualization.png", dpi=300)
plt.close()