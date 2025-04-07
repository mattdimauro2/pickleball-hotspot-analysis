# Pull the 2023 city-level demographic data (population, income, age) from the Census API.
# Clean and standardize city names and format for merging with pickleball data.

import requests
import pandas as pd

# Census API key
API_KEY = "68fb55a2c061c0bf39a9011145ff16c22918e539"

# Define variables to pull from the Census API
variables = [
    "NAME",            # Place name
    "B01003_001E",     # Total population
    "B19013_001E",     # Median household income
    "B01002_001E"      # Median age
]

# Mapping from Census codes to readable column names
rename_dict = {
    "NAME": "place_name",
    "B01003_001E": "population",
    "B19013_001E": "median_income",
    "B01002_001E": "median_age"
}

# Define FIPS → state abbreviation mapping (50 states + DC)
state_fips_to_abbr = {
    '01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA',
    '08': 'CO', '09': 'CT', '10': 'DE', '11': 'DC', '12': 'FL',
    '13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL', '18': 'IN',
    '19': 'IA', '20': 'KS', '21': 'KY', '22': 'LA', '23': 'ME',
    '24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN', '28': 'MS',
    '29': 'MO', '30': 'MT', '31': 'NE', '32': 'NV', '33': 'NH',
    '34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND',
    '39': 'OH', '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI',
    '45': 'SC', '46': 'SD', '47': 'TN', '48': 'TX', '49': 'UT',
    '50': 'VT', '51': 'VA', '53': 'WA', '54': 'WV', '55': 'WI',
    '56': 'WY'
}

# Pull data from the API for each state (loop by FIPS code)
all_places = []
state_fips = list(state_fips_to_abbr.keys())

for fips in state_fips:
    url = f"https://api.census.gov/data/2023/acs/acs5?get={','.join(variables)}&for=place:*&in=state:{fips}&key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        all_places.append(df)
    else:
        print(f"Error for state {fips}: {response.status_code} - {response.text}")

# Combine all state data into one DataFrame
places_df = pd.concat(all_places, ignore_index=True)

# Rename Census codes to readable names
places_df.rename(columns=rename_dict, inplace=True)

# Clean and simplify place names (ex: "Naples city, Florida" → "Naples, FL")
def clean_place_name(row):
    name = row["place_name"]
    state_fips = row["state"]
    state_abbr = state_fips_to_abbr.get(state_fips, "")
    # Remove 'city', 'town', 'CDP' suffixes
    city = name.split(",")[0].replace(" city", "").replace(" town", "").replace(" CDP", "").strip()
    return f"{city}, {state_abbr}"

places_df["city_state"] = places_df.apply(clean_place_name, axis=1)

# Keep only necessary columns
places_df = places_df[["city_state", "population", "median_income", "median_age"]]

# Convert columns to numeric and clean invalid data
places_df["population"] = pd.to_numeric(places_df["population"], errors="coerce")
places_df["median_income"] = pd.to_numeric(places_df["median_income"], errors="coerce")
places_df["median_age"] = pd.to_numeric(places_df["median_age"], errors="coerce")

# Drop rows with missing or negative values
places_df = places_df.dropna()
places_df = places_df[places_df["median_income"] > 0]

# Export cleaned data to CSV
places_df.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\census_city_data_2023_cleaned.csv", index=False)
print(places_df.head())
