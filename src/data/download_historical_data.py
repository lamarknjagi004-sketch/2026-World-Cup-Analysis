import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_mock_historical_data(num_matches=1000, output_path='data/historical_matches.csv'):
    """
    Generates a mock dataset of international football matches to simulate a historical database.
    This provides the necessary volume and features to train the Poisson and ML models.
    """
    # Top 32 teams approx for a world cup with their base mock Elo ratings
    teams = {
        "Argentina": 2100, "France": 2050, "Brazil": 2040, "England": 2000,
        "Spain": 1950, "Portugal": 1940, "Netherlands": 1920, "Germany": 1900,
        "Italy": 1880, "Croatia": 1850, "Uruguay": 1840, "Morocco": 1820,
        "USA": 1800, "Colombia": 1780, "Mexico": 1760, "Senegal": 1750,
        "Japan": 1740, "Switzerland": 1730, "Iran": 1700, "South Korea": 1680,
        "Australia": 1650, "Ecuador": 1640, "Serbia": 1630, "Poland": 1620,
        "Saudi Arabia": 1600, "Ghana": 1580, "Wales": 1560, "Costa Rica": 1550,
        "Cameroon": 1540, "Canada": 1520, "Tunisia": 1500, "Qatar": 1450
    }
    
    team_names = list(teams.keys())
    data = []
    
    start_date = datetime(2022, 1, 1) # Training window last 4 years
    
    for i in range(num_matches):
        match_date = start_date + timedelta(days=random.randint(0, 1500))
        home_team, away_team = random.sample(team_names, 2)
        
        # Calculate winning expectation probabilities based on mock Elo diff
        elo_diff = teams[home_team] - teams[away_team] + 50  # +50 simulates home advantage
        
        # Base expected goals (xG) structurally tied to team strength
        home_xg_base = 1.2 + (elo_diff / 500.0)
        away_xg_base = 1.2 - (elo_diff / 500.0)
        
        home_xg = max(0.1, random.gauss(home_xg_base, 0.4))
        away_xg = max(0.1, random.gauss(away_xg_base, 0.4))
        
        # Actual goals simulated as a Poisson process from xG
        home_goals = np.random.poisson(home_xg)
        away_goals = np.random.poisson(away_xg)
        
        # Other match stats
        home_possession = max(30, min(70, int(50 + (elo_diff / 40) + random.randint(-5, 5))))
        away_possession = 100 - home_possession
        
        data.append({
            "date": match_date.strftime("%Y-%m-%d"),
            "home_team": home_team,
            "away_team": away_team,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "home_xg": round(home_xg, 2),
            "away_xg": round(away_xg, 2),
            "home_possession": home_possession,
            "away_possession": away_possession,
            "tournament": "International Friendly" if random.random() > 0.3 else "World Cup Qualifier"
        })
        
    df = pd.DataFrame(data).sort_values(by="date")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {num_matches} historical matches at {output_path}")

if __name__ == "__main__":
    generate_mock_historical_data(1500)
    print("Data Ingestion complete.")
