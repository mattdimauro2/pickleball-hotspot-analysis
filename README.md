# Pickleball Hotspot Analysis

This project uses data science to identify US cities with high potential for future pickleball growth. The focus is on pinpointing cities that could support **major tournaments**, similar to the US Open Pickleball Championships held annually in Naples, FL. The project combines court availability, tournament activity, search interest, and city demographics into a clean, structured pipeline that highlights areas of opportunity and provides a broader view of the pickleball landscape across the US.

---

## Objective

The goal is to help tournament organizers make informed, data-driven decisions about where to expand next. I set out to spotlight cities that have the right mix of infrastructure, demand, and demographics to support hosting a large-scale pickleball event. I also sought out to identify factors that could lead to an unsuccessful major tournament (such as the 2023 Atlantic City Pickleball Open).

---

## Project Overview

The project follows a step-by-step pipeline from raw data to final visualizations and predictions:

### 1. Court Data
- Combines multiple raw JSON court files from [Pickleheads](https://www.pickleheads.com)
- Cleans and merges into: `courts_cleaned.csv`

### 2. Tournament Data
- Cleans tournament data from [PickleballTournaments.com](https://pickleballtournaments.com/), including player counts
- Outputs: `tournaments_cleaned.csv`, `tournaments_by_month.png`

### 3. Google Trends Data
- Pulls state-level and time-series search interest for the keywords:
  - `"pickleball"`, `"pickleball tournament"`, `"pickleball court"`, `"pickleball lessons"`, `"PPA Tour"`, and `"pickleball near me"`
- Outputs:
  - `merged_google_trends.csv`
  - `merged_google_trend_time.csv`

### 4. Demographics (Census Data)
- Uses the 2023 U.S. Census API to pull city-level population, income, and age data
- Output: `census_city_data_2023_cleaned.csv`

### 5. Data Merge
- Combines all cleaned datasets into a single city-level dataset:
  - `merged_city_data.csv`

---

## Scoring & Prediction

### Composite Scoring
Generates a “hotspot score” based on:
- Number of courts
- Number of tournaments
- Player participation
- Courts per 10,000 residents

→ Output: `merged_city_data_with_score.csv`

### Random Forest Model
Trains a model to predict the probability a city could host a **major tournament**.

→ Outputs:
- Adds `rf_major_prob` column
- Generates: `decision_tree.png`, `feature_importance_major_tournament.png`

### Final Score
Combines composite score with model probability into:
- `merged_city_data_with_composite_score.csv`
- Visualized in: `composite_score_bar_chart.png`

---

## Tableau Dashboards

All final data is visualized in two interactive Tableau dashboards:

### [Dynamic Pickleball Landscape Map](https://public.tableau.com/app/profile/matthew.dimauro/viz/DynamicPickleballLandscapeMap/PickleballDynamicOverviewMap)
- A US map showing city-level pickleball activity
- Dropdown lets users toggle between metrics:
  - Number of Courts
  - Number of Tournaments
  - Number of Large Tournaments (>250 players)
  - Number of Major Tournaments
  - Composite Score
  - Untapped Composite Score (cities that haven’t hosted a major)
  - Random Forest Major Tournament Probability
- Circle **size and color** reflect the selected metric
- Table below the map lists the **top 10 cities** by that metric

### [Pickleball Growth & Opportunity Overview](https://public.tableau.com/app/profile/matthew.dimauro/viz/PickleballGrowthandOpportunityOverview/PickleballGrowthOpportunityOverview)
- Filters for state, city, and major tournament presence
- Summary KPIs for:
  - Total courts
  - Total tournaments
  - Large tournaments
  - Major tournaments
- Bar charts for:
  - Courts by State
  - Tournaments by State
- Top 10 city rankings for:
  - Composite Score
  - High-potential cities that haven’t hosted a major
- Line chart: Tournaments by Month (2024)
- Scatterplots: Composite Score vs. Median Age and Median Income

→ Static screenshots saved in the `tableau/` folder.

---

## Atlantic City Case Study

This project also includes a special case study exploring **why a past tournament in Atlantic City underperformed**.

Atlantic City was once selected as a tournament location but failed to gain traction. I wanted to dig into the data and see if I could identify **why it didn’t succeed**. The analysis looks at:
- Low Google Trends interest in February
- Limited court infrastructure
- Lack of prior large or major tournaments
- Demographic factors like age and income

The visualization `atlantic_city_analysis_visualization.png` provides a visual breakdown of these findings.

---



## Project Structure

```
pickleball-analysis/
│
├── raw-data/           # Original scraped/raw files
├── clean-data/         # Cleaned datasets used in modeling & Tableau
├── scripts/            # Python scripts for cleaning, merging, modeling
├── visualization/      # Tableau dashboards and supporting charts
└── README.md           # Project overview and documentation
```

---

## ▶️ How to Run

1. Clone the repository:
```bash
git clone https://github.com/your-username/pickleball-hotspot-analysis.git
```

2. Navigate into the folder:
```bash
cd pickleball-hotspot-analysis
```

3. Install required Python packages:
```bash
pip install -r requirements.txt
```

4. Run any script from the `scripts/` folder:
```bash
python scripts/random_forest.py
```

---

## 🛠️ Built With

- Python (`pandas`, `scikit-learn`, `matplotlib`)
- Tableau Public
- Google Trends API
- U.S. Census API

---

## 👤 Author

Created by Matthew DiMauro to support data-informed growth in the world of pickleball.