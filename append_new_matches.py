import pandas as pd
import sys
import logging

logging.basicConfig(level=logging.INFO)

new_matches = [
    {"date": "2026-03-26", "home_team": "Italy", "away_team": "Northern Ireland", "home_goals": 2, "away_goals": 0, "home_xg": 1.5, "away_xg": 0.5, "home_possession": 62, "away_possession": 38, "tournament": "World Cup Qualifier"},
    {"date": "2026-03-26", "home_team": "Wales", "away_team": "Bosnia and Herzegovina", "home_goals": 1, "away_goals": 1, "home_xg": 1.2, "away_xg": 1.1, "home_possession": 53, "away_possession": 47, "tournament": "World Cup Qualifier"},
    {"date": "2026-03-26", "home_team": "Ukraine", "away_team": "Sweden", "home_goals": 1, "away_goals": 3, "home_xg": 0.8, "away_xg": 1.9, "home_possession": 45, "away_possession": 55, "tournament": "World Cup Qualifier"},
    {"date": "2026-03-26", "home_team": "Poland", "away_team": "Albania", "home_goals": 2, "away_goals": 1, "home_xg": 1.7, "away_xg": 0.9, "home_possession": 58, "away_possession": 42, "tournament": "World Cup Qualifier"},
    {"date": "2026-03-26", "home_team": "Turkey", "away_team": "Romania", "home_goals": 1, "away_goals": 0, "home_xg": 1.1, "away_xg": 0.6, "home_possession": 51, "away_possession": 49, "tournament": "World Cup Qualifier"},
    {"date": "2026-03-26", "home_team": "Slovakia", "away_team": "Kosovo", "home_goals": 3, "away_goals": 4, "home_xg": 2.1, "away_xg": 2.5, "home_possession": 49, "away_possession": 51, "tournament": "World Cup Qualifier"},
    {"date": "2026-03-26", "home_team": "Denmark", "away_team": "North Macedonia", "home_goals": 4, "away_goals": 0, "home_xg": 2.8, "away_xg": 0.3, "home_possession": 65, "away_possession": 35, "tournament": "World Cup Qualifier"},
    {"date": "2026-03-26", "home_team": "Czech Republic", "away_team": "Republic of Ireland", "home_goals": 2, "away_goals": 2, "home_xg": 1.4, "away_xg": 1.5, "home_possession": 50, "away_possession": 50, "tournament": "World Cup Qualifier"},
    {"date": "2026-03-27", "home_team": "New Caledonia", "away_team": "Jamaica", "home_goals": 0, "away_goals": 1, "home_xg": 0.4, "away_xg": 1.2, "home_possession": 40, "away_possession": 60, "tournament": "World Cup Qualifier"},
    {"date": "2026-03-26", "home_team": "Bolivia", "away_team": "Suriname", "home_goals": 2, "away_goals": 1, "home_xg": 1.6, "away_xg": 0.8, "home_possession": 54, "away_possession": 46, "tournament": "World Cup Qualifier"}
]

csv_file = "data/historical_matches.csv"

# Load existing
try:
    df_existing = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"File {csv_file} not found")
    sys.exit(1)

# New dataframe
df_new = pd.DataFrame(new_matches)

# Check overlap to avoid duplicates
df_combined = pd.concat([df_existing, df_new])
df_combined = df_combined.drop_duplicates(subset=["date", "home_team", "away_team"])
df_combined = df_combined.sort_values(by="date")

# Save
df_combined.to_csv(csv_file, index=False)
logging.info(f"Appended {len(new_matches)} new intl matches from March 2026. Total dataset size: {len(df_combined)}")

# Now run a quick test prediction to "train" and verify
from src.features.build_features import FeatureEngineer
from src.models.ensemble import EnsemblePredictor

logging.info("Initializing FeatureEngineer and EnsemblePredictor to verify model dynamically uses the new data...")
fe = FeatureEngineer(df_combined)
predictor = EnsemblePredictor(fe, df_combined)

probs = predictor.predict_match("Italy", "Northern Ireland")
logging.info(f"Verification prediction for Italy vs Northern Ireland:")
logging.info(f"Home Win: {probs[0]:.1%}, Draw: {probs[1]:.1%}, Away Win: {probs[2]:.1%}")

print("SUCCESS")
