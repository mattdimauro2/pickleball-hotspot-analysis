# Predict the likelihood of a city hosting a major pickleball tournament.
# Also train a decision tree and random forest using city-level features.
# Add the predicted probability column called rf_major_prob to the dataset.

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier

# Load data
data = pd.read_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data_with_score.csv")
data['has_major_tournament'] = (data['major_tournaments'] > 0).astype(int)
data['state'] = data['city_state'].str.split(', ').str[1]

# Use the same feature set from previous modeling
features = ["population", "median_income", "median_age", "Courts", "num_tournaments", "large_tournaments", "courts_per_10k"]
X = data[features].fillna(0)
y = data['has_major_tournament']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Decision Tree
dt = DecisionTreeClassifier(max_depth=3, random_state=42)
dt.fit(X_train, y_train)

# Create a clean decision tree
plt.figure(figsize=(16, 8))
plot_tree(
    dt,
    feature_names=features,
    class_names=['No Major', 'Has Major'],
    filled=True,
    rounded=True,
    impurity=False,
    fontsize=12,
    label='none',
    proportion=True
)
plt.title("Decision Tree: What Makes a City Suitable for a Major Tournament?")
plt.tight_layout()
plt.savefig("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\visualizations\\decision_tree.png", dpi=300)
plt.close()

# Feature importance
importances = pd.Series(dt.feature_importances_, index=features).sort_values()
plt.figure(figsize=(8, 6))
importances.plot(kind="barh", color="#4CAF50")
plt.title("Feature Importance for Hosting a Major Tournament")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\visualizations\\feature_importance_major_tournament.png")
plt.close()

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
data['rf_major_prob'] = rf.predict_proba(X)[:, 1]

# Top 10 cities by RF predicted probability
top_rf = data.sort_values(by='rf_major_prob', ascending=False).head(10)
print("Top 10 Cities by Random Forest Predicted Probability of Hosting a Major Tournament:")
print(top_rf[['city_state', 'rf_major_prob', 'Courts', 'num_tournaments']])

# Save updated data with rf_major_prob
data.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\merged_city_data_with_score.csv", index=False)
