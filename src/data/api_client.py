import random

class LiveMatchAPI:
    """
    Mock API Client to simulate fetching live data feeds and betting odds during matches.
    In production, this would connect to providers like API-Football or Sportmonks.
    """
    
    @staticmethod
    def get_prematch_odds(home_team, away_team):
        """Returns mock implied probabilities from betting markets."""
        # Hardcoding a rough default, in reality the model checks this against market deviation
        base_home = 0.40
        base_draw = 0.25
        base_away = 0.35 
        
        # Random noise to simulate market deviation from absolute truth
        noise = random.uniform(-0.05, 0.05)
        
        return {
            "implied_home_win": round(base_home + noise, 3),
            "implied_draw": round(base_draw, 3),
            "implied_away_win": round(base_away - noise, 3)
        }
        
    @staticmethod
    def get_weather_conditions(stadium="MetLife Stadium"):
        """Simulate retrieving real-time weather APIs which affect match fatigue."""
        conditions = [
            {"condition": "Clear", "temp_f": 75, "altitude_m": 10},
            {"condition": "Rain", "temp_f": 60, "altitude_m": 10},
            {"condition": "Overcast", "temp_f": 70, "altitude_m": 10},
            {"condition": "Humid", "temp_f": 85, "altitude_m": 500}
        ]
        return random.choice(conditions)
