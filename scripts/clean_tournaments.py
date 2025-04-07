"""
Data on pickleball tournaments comes from: https://pickleballtournaments.com/
I filtered to the year 2024 and combined all tournaments into a file called "tournament_raw_data.csv"
The raw file was a single column that had 5 rows for each tournament with values for:
1.) Tournament Name; 2..) Location; 3.) Date; 4.) Completion Status; 5.) Number of Players
The code below cleans the tournaments file, adds a flag if it was a major tournament, adds a flag if the tournament had >250 players,
imputes missing player counts if 0, and removes tournaments that were not in the US
"""
import pandas as pd

# Read the raw text data
# Each tournament is 5 lines long: Name, Location, Date Range, Status, Players
with open("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\raw-data\\tournament_raw_data.csv", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip() != ""]

# Check that data is in 5-line chunks
assert len(lines) % 5 == 0, "Data is not cleanly split into 5-line blocks."

# Parse raw lines into structured tournament records
tournaments = []
for i in range(0, len(lines), 5):
    name = lines[i]
    location = lines[i + 1].replace('"', '')
    date_range = lines[i + 2]
    status = lines[i + 3]
    players_raw = lines[i + 4]

    # Extract the player count
    num_players = int(players_raw.split()[0]) if "player" in players_raw else 0

    tournaments.append({
        "Tournament Name": name,
        "Location": location,
        "Date Range": date_range,
        "Status": status,
        "Players": num_players
    })

# Convert it to a DataFrame
df = pd.DataFrame(tournaments)

# Extract the City and State info from Location
df[["City", "State"]] = df["Location"].str.extract(r"^(.*?),\s*([A-Z]{2})")

# Only keep valid US states + DC
valid_states = {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
                'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
                'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'}
df = df[df["State"].isin(valid_states)]

# Extract and parse the Start Date info
# Extract raw start date
df["Raw Start Date"] = df["Date Range"].str.split(" - ").str[0]

# Clean quotes and weird characters
df["Raw Start Date"] = df["Raw Start Date"].str.replace('"', '', regex=False)
df["Raw Start Date"] = df["Raw Start Date"].str.strip()

# Parse using the known format
df["Start Date"] = pd.to_datetime(df["Raw Start Date"], format="%b %d, %Y", errors="coerce")

# Impute missing player counts
df.loc[df["Players"] == 0, "Players"] = 25

# Add custom flags for large tournaments (>250) and major tournaments - as denoted below

# Flag for large tournaments (>250 players)
df["is_large_tournament"] = df["Players"] > 250

# List of known major tournaments and their names mapped from the tournament data
major_tournaments = [
    "PPA Tour: Daytona Beach Open Presented by Roar",
    "PPA Tour: CIBC The Finals",
    "PPA Tour: Vulcan Orlando Cup",
    "PPA Tour: Veolia Milwaukee Open",
    "2024 Lapiplasty Pickleball World Championships",
    "Minor League Pickleball @ MLP Miami",
    "PPA Tour: Guaranteed Rate Las Vegas Open",
    "2024 Tournament of Champions",
    "PPA Tour: Stratusphere Gin Virginia Beach Cup",
    "Minor League Pickleball @ MLP Virginia",
    "MLP Takeover Clinic at Life Time NYC",
    "PPA Tour: CIBC Atlanta Slam",
    "PPA Tour: Las Vegas Pickleball Cup",
    "PPA Tour: Picklr Utah Open",
    "PPA Tour: Bristol Open",
    "PPA Tour: Selkirk Kansas City Open",
    "2024 Grand Rapids BEER CITY OPEN Pickleball Championships",
    "PPA Tour: Select Medical Orange County Cup",
    "DC Open Team Powered by the PPA Tour and MLP",
    "PPA Tour: Veolia Sacramento Open",
    "SMASH INTO SUMMER MLP TOURNAMENT",
    "PPA Tour: CIBC Texas Open",
    "PPA Tour: Vizzy Atlanta Slam",
    "MLP - Atlanta Amateur Smash",
    "PPA Tour: Selkirk Red Rock Open",
    "PPA Tour: Veolia LA Open",
    "Minto US Open Pickleball Championships",
    "PPA Tour: Veolia Houston Open",
    "PPA Tour: North Carolina Cup",
    "PPA Tour: Austin TX",
    "PPA Tour: Lakeville MN",
    "PPA Tour: Mesa AZ",
    "PPA Tour: Phoenix AZ",
    "PPA Tour: Palm Springs CA"
]

# Flag for major tournaments
df["is_major_tournament"] = df["Tournament Name"].isin(major_tournaments)

# Final cleanup
df = df.drop(columns=["Date Range", "Location"])
df = df.reset_index(drop=True)

# Preview the cleaned dataset
print(df.head())

# Save to new CSV
df.to_csv("C:\\Users\\Matty\\GitHub\\pickleball-analysis\\clean-data\\tournaments_cleaned.csv", index=False)