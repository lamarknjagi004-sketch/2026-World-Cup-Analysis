import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info(f"✅ Generated {num_matches} historical matches at {output_path}")
    return df


def fetch_live_historical_data(api_key: Optional[str] = None, output_path: str = 'data/historical_matches.csv', use_api: bool = False):
    """
    Fetch real historical data from API-Football or generate mock data.
    
    Args:
        api_key: RapidAPI key for API-Football (get from https://rapidapi.com/api-sports/api/api-football)
        output_path: Path to save historical data
        use_api: If True, use API-Football; if False, generate mock data
        
    Returns:
        DataFrame with match data
    """
    if use_api and api_key:
        try:
            from api_football_client import fetch_and_update_historical_data
            logger.info("📡 Fetching live data from API-Football...")
            return fetch_and_update_historical_data(api_key, output_path)
        except ImportError:
            logger.warning("api_football_client not available. Falling back to mock data.")
            return generate_mock_historical_data(1000, output_path)
    else:
        logger.info("📊 Generating mock historical data...")
        return generate_mock_historical_data(1000, output_path)


if __name__ == "__main__":
    import sys
    
    # Check if API key provided as command line argument
    api_key = sys.argv[1] if len(sys.argv) > 1 else None
    use_api = "--live" in sys.argv
    
    if use_api and not api_key:
        logger.warning("⚠️ --live flag provided but no API key. Using mock data instead.")
        logger.info("Usage: python download_historical_data.py YOUR_API_KEY --live")
    
    df = fetch_live_historical_data(api_key, use_api=use_api)
    logger.info(f"✅ Data Ingestion complete. Loaded {len(df)} matches.")
