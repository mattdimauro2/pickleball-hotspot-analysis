"""
Data on pickleball court locations comes from: https://www.pickleheads.com/courts/us
For each state, I went into the state specific tab (ex: https://www.pickleheads.com/courts/us/alabama) and manually pulled the html json data on the particular cities, number of locations, and number of courts.
I created a folder called "json_files" where the json for each state is saved.
The code below parses through each state's json file and combines them into one file: "courts_combined.csv"
"""

import json
import pandas as pd
from pathlib import Path

# Define the input directory
json_dir = Path("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\json_files")

# Initialize an empty list to store extracted data
all_data = []

# Loop through each JSON file in the directory
for json_file in json_dir.glob("*.json"):
    with open(json_file, "r") as f:
        data = json.load(f)

    # Handle state files (stored as lists of city entries)
    if isinstance(data, list):
        for entry in data:
            all_data.append({
                "State": entry["state_name"],
                "City": entry["city"],
                "Locations": int(entry["location_count"]),
                "Courts": int(entry["court_count"])
            })

    # Handle DC separately (stored as a single dictionary)
    elif isinstance(data, dict):
        all_data.append({
            "State": data["state_name"],
            "City": data["city"],
            "Locations": int(data["location_count"]),
            "Courts": int(data["court_count"])
        })

# Convert extracted data into a pandas DataFrame
df = pd.DataFrame(all_data)

# Save the cleaned data to a CSV file
df.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\courts_combined.csv", index=False)