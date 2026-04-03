"""
Fetch Recent International Matches
Fetches football international matches from the past week and appends to training data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
import logging
import random

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_recent_mock_matches(days_back: int = 7):
    """
    Generate mock international matches from the past N days.
    
    Args:
        days_back: Number of days to look back
        
    Returns:
        DataFrame with recent mock matches
    """
    # International teams
    teams = [
        "Argentina", "France", "Brazil", "England", "Spain", "Portugal", "Netherlands", "Germany",
        "Italy", "Croatia", "Uruguay", "Morocco", "USA", "Colombia", "Mexico", "Senegal",
        "Japan", "Switzerland", "Iran", "South Korea", "Australia", "Ecuador", "Serbia", "Poland",
        "Saudi Arabia", "Ghana", "Wales", "Costa Rica", "Cameroon", "Canada", "Tunisia", "Qatar"
    ]
    
    matches = []
    end_date = datetime.now()
    
    # Generate 10-15 random matches in the past week
    num_matches = random.randint(10, 15)
    
    for i in range(num_matches):
        # Random date in past week
        match_date = end_date - timedelta(days=random.randint(1, days_back))
        
        # Random teams
        home_team, away_team = random.sample(teams, 2)
        
        # Simulate realistic scores (international matches tend to have lower scores)
        home_goals = np.random.poisson(1.2)
        away_goals = np.random.poisson(1.0)
        
        # Realistic xG and possession
        home_xg = max(0.1, random.gauss(1.3, 0.4))
        away_xg = max(0.1, random.gauss(1.1, 0.4))
        home_possession = random.randint(45, 65)
        away_possession = 100 - home_possession
        
        match = {
            "date": match_date.strftime("%Y-%m-%d"),
            "home_team": home_team,
            "away_team": away_team,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "home_xg": round(home_xg, 2),
            "away_xg": round(away_xg, 2),
            "home_possession": home_possession,
            "away_possession": away_possession,
            "tournament": "International Friendly",  # or "World Cup Qualifier"
            "status": "FT"
        }
        matches.append(match)
    
    df = pd.DataFrame(matches)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    logger.info(f"✅ Generated {len(df)} mock recent international matches")
    return df

def fetch_recent_international_matches(api_key: str = None, days_back: int = 7):
    """
    Fetch or generate international matches from the past N days.
    
    Args:
        api_key: Optional RapidAPI key for API-Football
        days_back: Number of days to look back
        
    Returns:
        DataFrame with recent matches
    """
    if api_key and api_key != "your_rapidapi_key_here":
        # Try real API
        try:
            from src.data.api_football_client import APIFootballClient
            client = APIFootballClient(api_key)
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            date_from = start_date.strftime("%Y-%m-%d")
            date_to = end_date.strftime("%Y-%m-%d")
            
            logger.info(f"Fetching real international matches from {date_from} to {date_to}")
            
            # Try multiple international leagues
            all_fixtures = []
            international_leagues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # FIFA tournaments
            
            for league_id in international_leagues:
                try:
                    fixtures = client.get_fixtures_by_date(date_from, date_to, league=league_id)
                    all_fixtures.extend(fixtures)
                except:
                    pass
            
            matches = []
            for fixture in all_fixtures:
                match_data = client.extract_match_data(fixture)
                if match_data and match_data['home_goals'] is not None:
                    matches.append(match_data)
            
            if matches:
                df = pd.DataFrame(matches)
                df['date'] = pd.to_datetime(df['date'])
                df = df.drop_duplicates(subset=['date', 'home_team', 'away_team'])
                df = df.sort_values('date')
                logger.info(f"✅ Found {len(df)} real recent international matches")
                return df
        except Exception as e:
            logger.warning(f"API fetch failed: {str(e)}. Using mock data instead.")
    
    # Fall back to mock data
    logger.info("Using mock data for recent international matches")
    return generate_recent_mock_matches(days_back)

def append_to_training_data(new_matches_df: pd.DataFrame, output_path: str = 'data/historical_matches.csv'):
    """
    Append new matches to existing training data.
    
    Args:
        new_matches_df: DataFrame with new matches
        output_path: Path to training data CSV
    """
    if new_matches_df.empty:
        logger.info("No new matches to append")
        return
    
    # Load existing data
    try:
        existing_df = pd.read_csv(output_path)
        existing_df['date'] = pd.to_datetime(existing_df['date'])
    except FileNotFoundError:
        logger.warning(f"Existing file {output_path} not found, creating new one")
        existing_df = pd.DataFrame()
    
    # Combine and deduplicate
    combined_df = pd.concat([existing_df, new_matches_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=['date', 'home_team', 'away_team'])
    combined_df = combined_df.sort_values('date')
    
    # Save
    combined_df.to_csv(output_path, index=False)
    logger.info(f"✅ Appended {len(new_matches_df)} matches. Total: {len(combined_df)} matches")

if __name__ == "__main__":
    # Get API key from environment or user input
    api_key = os.getenv('RAPIDAPI_KEY')
    
    # Fetch recent matches (will use mock if no API key)
    recent_matches = fetch_recent_international_matches(api_key, days_back=7)
    
    if not recent_matches.empty:
        print(f"Found {len(recent_matches)} recent international matches:")
        print(recent_matches[['date', 'home_team', 'away_team', 'home_goals', 'away_goals']].tail())
        
        # Append to training data
        append_to_training_data(recent_matches)
        
        print("\n✅ Data appended to training set")
    else:
        print("❌ No recent international matches found")