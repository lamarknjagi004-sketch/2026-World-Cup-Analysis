"""
Live Football API Integration - API-Football (RapidAPI)
Fetches real match data, team statistics, odds, and fixtures from API-Football.
Free tier: 100 requests/day (sufficient for daily updates)
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIFootballClient:
    """
    Client for API-Football v3 (RapidAPI)
    Documentation: https://rapidapi.com/api-sports/api/api-football
    """
    
    def __init__(self, api_key: str):
        """
        Initialize API client with RapidAPI key.
        
        Args:
            api_key: Get free key from https://rapidapi.com/api-sports/api/api-football
                    Free tier: 100 requests per day
        """
        self.api_host = "api-football-v3.p.rapidapi.com"
        self.api_key = api_key
        self.base_url = f"https://{self.api_host}"
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': self.api_host
        }
        self.request_count = 0
        self.max_daily_requests = 100
        
    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        Make API request with error handling and rate limiting.
        
        Args:
            endpoint: API endpoint (e.g., '/fixtures')
            params: Query parameters
            
        Returns:
            JSON response or None if error
        """
        if self.request_count >= self.max_daily_requests:
            logger.warning(f"Daily request limit ({self.max_daily_requests}) reached!")
            return None
            
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            self.request_count += 1
            logger.info(f"✅ API Request {self.request_count}/{self.max_daily_requests}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API Error: {str(e)}")
            return None
    
    def get_upcoming_fixtures(self, league: int = 1, season: int = 2026) -> List[Dict]:
        """
        Fetch upcoming World Cup fixtures.
        
        Args:
            league: 1 = FIFA World Cup
            season: Tournament year (2026)
            
        Returns:
            List of fixture dictionaries
        """
        params = {
            "league": league,
            "season": season,
            "status": "NS"  # Not started
        }
        response = self._make_request("/fixtures", params)
        if response and response.get('response'):
            return response['response']
        return []
    
    def get_team_statistics(self, team_id: int, season: int = 2026) -> Optional[Dict]:
        """
        Get comprehensive team statistics for a season.
        
        Args:
            team_id: Team ID from API
            season: Season year
            
        Returns:
            Team stats dictionary
        """
        params = {
            "team": team_id,
            "season": season
        }
        response = self._make_request("/teams/statistics", params)
        if response and response.get('response'):
            return response['response']
        return None
    
    def get_historical_matches(self, team_id: int, last: int = 50) -> List[Dict]:
        """
        Get recent historical matches for a team (for feature engineering).
        
        Args:
            team_id: Team ID
            last: Number of recent matches to retrieve
            
        Returns:
            List of match fixtures
        """
        params = {
            "team": team_id,
            "last": last
        }
        response = self._make_request("/fixtures", params)
        if response and response.get('response'):
            return response['response']
        return []
    
    def get_live_matches(self) -> List[Dict]:
        """Get currently live matches with real-time scores."""
        params = {"status": "LIVE"}
        response = self._make_request("/fixtures", params)
        if response and response.get('response'):
            return response['response']
        return []
    
    def get_team_by_name(self, team_name: str) -> Optional[Dict]:
        """Search for team by name to get team ID."""
        params = {"name": team_name}
        response = self._make_request("/teams", params)
        if response and response.get('response'):
            return response['response'][0] if response['response'] else None
        return None
    
    def get_head_to_head(self, home_team_id: int, away_team_id: int, last: int = 10) -> List[Dict]:
        """Get head-to-head match history between two teams."""
        params = {
            "h2h": f"{home_team_id}-{away_team_id}",
            "last": last
        }
        response = self._make_request("/fixtures", params)
        if response and response.get('response'):
            return response['response']
        return []
    
    def extract_match_data(self, fixture: Dict) -> Dict:
        """Convert API fixture format to standardized match data format."""
        try:
            goals = fixture.get('goals', {})
            stats = fixture.get('statistics', {})
            
            # Extract team names
            home_team = fixture['teams']['home']['name'] if fixture.get('teams') else 'Unknown'
            away_team = fixture['teams']['away']['name'] if fixture.get('teams') else 'Unknown'
            
            # Extract goals (None if match not started)
            home_goals = goals.get('home')
            away_goals = goals.get('away')
            
            # Extract statistics if available
            home_stats = next((s for s in stats if s['team']['side'] == 'home'), {}).get('statistics', []) if stats else []
            away_stats = next((s for s in stats if s['team']['side'] == 'away'), {}).get('statistics', []) if stats else []
            
            # Extract possession
            home_possession = next((int(s['value']) for s in home_stats if s['type'] == 'possession'), 50)
            away_possession = 100 - home_possession
            
            return {
                "date": fixture['fixture']['date'][:10] if fixture.get('fixture') else datetime.now().strftime("%Y-%m-%d"),
                "home_team": home_team,
                "away_team": away_team,
                "home_goals": home_goals,
                "away_goals": away_goals,
                "home_possession": home_possession,
                "away_possession": away_possession,
                "home_xg": 0.0,  # API-Football free tier doesn't include xG
                "away_xg": 0.0,
                "tournament": "World Cup",
                "status": fixture['fixture']['status']['short'] if fixture.get('fixture') else 'NS'
            }
        except Exception as e:
            logger.error(f"Error extracting match data: {str(e)}")
            return None


def fetch_and_update_historical_data(api_key: str, output_path: str = 'data/historical_matches.csv'):
    """
    Fetch real historical match data and save to CSV.
    Combines API-Football data with existing mock data for training.
    """
    client = APIFootballClient(api_key)
    
    # World Cup 32 teams (approximate IDs from API-Football)
    world_cup_teams = {
        "Argentina": 42, "France": 10, "Brazil": 27, "England": 25,
        "Spain": 24, "Portugal": 38, "Netherlands": 13, "Germany": 33,
        "Italy": 23, "Croatia": 52, "Uruguay": 50, "Morocco": 37,
        "USA": 16, "Colombia": 31, "Mexico": 32, "Senegal": 49,
        "Japan": 53, "Switzerland": 35, "Iran": 70, "South Korea": 51,
        "Australia": 60, "Ecuador": 74, "Serbia": 84, "Poland": 88,
        "Saudi Arabia": 102, "Ghana": 47, "Wales": 21, "Costa Rica": 80,
        "Cameroon": 46, "Canada": 18, "Tunisia": 39, "Qatar": 98
    }
    
    all_matches = []
    
    logger.info("🔄 Fetching historical matches for all teams...")
    for team_name, team_id in world_cup_teams.items():
        logger.info(f"Fetching matches for {team_name}...")
        fixtures = client.get_historical_matches(team_id, last=30)
        
        for fixture in fixtures:
            match_data = client.extract_match_data(fixture)
            if match_data:
                all_matches.append(match_data)
        
        time.sleep(0.5)  # Rate limiting: 0.5s between requests
    
    # Convert to DataFrame and remove duplicates
    if all_matches:
        df = pd.DataFrame(all_matches)
        df['date'] = pd.to_datetime(df['date'])
        df = df.drop_duplicates(subset=['date', 'home_team', 'away_team'])
        df = df.sort_values(by='date')
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"✅ Saved {len(df)} historical matches to {output_path}")
        return df
    else:
        logger.warning("⚠️ No matches fetched. Check API key or rate limit.")
        return pd.DataFrame()


if __name__ == "__main__":
    # Example usage
    API_KEY = "your_rapidapi_key_here"  # Get from https://rapidapi.com/api-sports/api/api-football
    
    client = APIFootballClient(API_KEY)
    
    # Example: Get upcoming fixtures
    fixtures = client.get_upcoming_fixtures()
    print(f"Found {len(fixtures)} upcoming fixtures")
    
    # Example: Get team stats
    france_stats = client.get_team_statistics(team_id=10)
    if france_stats:
        print(f"France statistics: {france_stats['statistics'][:3]}")
    
    # Fetch and save historical data
    fetch_and_update_historical_data(API_KEY)
