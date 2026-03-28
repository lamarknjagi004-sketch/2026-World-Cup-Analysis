"""
Sofascore Data Parser
Converts Sofascore JSON match data to standardized training format.
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SofascoreParser:
    """Parse Sofascore API JSON response to pandas DataFrame"""
    
    @staticmethod
    def parse_fixture(fixture: Dict) -> Optional[Dict]:
        """
        Convert Sofascore fixture object to standardized match format.
        
        Args:
            fixture: Single event dict from Sofascore events array
            
        Returns:
            Standardized match dict or None if parse fails
        """
        try:
            # Extract team data
            home_team = fixture['homeTeam']['name']
            away_team = fixture['awayTeam']['name']
            
            # Extract scores
            home_goals = fixture['homeScore']['current']
            away_goals = fixture['awayScore']['current']
            
            # Extract tournament
            tournament = fixture['tournament']['name'] if fixture.get('tournament') else 'Unknown'
            
            # Extract date
            date_str = datetime.fromtimestamp(fixture['startTimestamp']).strftime("%Y-%m-%d")
            
            # Parse possession from statistics if available
            home_possession = 50  # Default
            away_possession = 50
            
            if fixture.get('statistics'):
                for stat in fixture['statistics']:
                    if stat.get('team', {}).get('side') == 'home':
                        for s in stat.get('statistics', []):
                            if s.get('type') == 'possession':
                                try:
                                    home_possession = int(s.get('value', 50))
                                except:
                                    pass
            
            away_possession = 100 - home_possession
            
            return {
                "date": date_str,
                "home_team": home_team,
                "away_team": away_team,
                "home_goals": home_goals,
                "away_goals": away_goals,
                "home_xg": 0.0,  # Sofascore free endpoint doesn't expose xG
                "away_xg": 0.0,
                "home_possession": home_possession,
                "away_possession": away_possession,
                "tournament": tournament,
                "status": fixture['status']['description'] if fixture.get('status') else 'Unknown'
            }
        except Exception as e:
            logger.error(f"Error parsing fixture: {str(e)}")
            return None
    
    @staticmethod
    def parse_response(response_json: Dict) -> pd.DataFrame:
        """
        Convert full Sofascore API response to DataFrame.
        
        Args:
            response_json: Full API response with 'events' array
            
        Returns:
            DataFrame with standardized match data
        """
        matches = []
        
        if 'events' in response_json:
            for fixture in response_json['events']:
                match_data = SofascoreParser.parse_fixture(fixture)
                if match_data:
                    matches.append(match_data)
        
        df = pd.DataFrame(matches)
        if len(df) > 0:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            logger.info(f"✅ Parsed {len(df)} matches from Sofascore data")
        else:
            logger.warning("⚠️ No matches parsed from Sofascore response")
        
        return df
    
    @staticmethod
    def load_from_json_file(filepath: str) -> pd.DataFrame:
        """Load Sofascore data from JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return SofascoreParser.parse_response(data)
        except Exception as e:
            logger.error(f"Error loading JSON file: {str(e)}")
            return pd.DataFrame()


def save_sofascore_training_data(response_json: Dict, output_path: str = 'data/historical_matches.csv'):
    """
    Save Sofascore matches to training data file.
    
    Args:
        response_json: Sofascore API response (events array)
        output_path: Path to save CSV
    """
    df = SofascoreParser.parse_response(response_json)
    
    if len(df) > 0:
        df.to_csv(output_path, index=False)
        logger.info(f"✅ Saved {len(df)} matches to {output_path}")
        return df
    else:
        logger.warning("No data to save")
        return df


if __name__ == "__main__":
    # Example: Load from JSON file
    # df = SofascoreParser.load_from_json_file('chelsea_data.json')
    # print(df.head())
    pass
