import pandas as pd
import numpy as np

class FeatureEngineer:
    """
    Processes raw match data to generate advanced predictive features for modeling.
    """
    def __init__(self, historical_df):
        self.df = historical_df
        
    def get_team_recent_form(self, team_name, match_date_str, last_n=5):
        """
        Calculates the Dynamic Form Indicator.
        Matches closer to the current date are weighted more heavily.
        """
        if self.df is None or self.df.empty:
            return 0.5
            
        past_matches = self.df[
            ((self.df['home_team'] == team_name) | (self.df['away_team'] == team_name)) & 
            (self.df['date'] < match_date_str)
        ].tail(last_n)
        
        if past_matches.empty:
            return 0.5 # Neutral form
            
        points = 0
        total_weight = 0
        
        for i, row in enumerate(past_matches.itertuples()):
            weight = (i + 1) / last_n  # More recent = higher weight
            total_weight += weight
            
            if row.home_team == team_name:
                if row.home_goals > row.away_goals:
                    points += 3 * weight
                elif row.home_goals == row.away_goals:
                    points += 1 * weight
            else:
                if row.away_goals > row.home_goals:
                    points += 3 * weight
                elif row.away_goals == row.home_goals:
                    points += 1 * weight
                    
        return points / (3 * total_weight) if total_weight > 0 else 0.5
        
    def get_efficiencies(self, team_name):
        """
        Returns Offensive Efficiency (Goals over xG) and Defensive Stability (Conceded vs xGA)
        """
        if self.df is None or self.df.empty:
            return 1.0, 1.0
            
        home_matches = self.df[self.df['home_team'] == team_name]
        away_matches = self.df[self.df['away_team'] == team_name]
        
        # If team has no matches, return neutral efficiency
        if len(home_matches) == 0 and len(away_matches) == 0:
            return 1.0, 1.0
        
        total_goals = home_matches['home_goals'].sum() + away_matches['away_goals'].sum()
        total_xg = home_matches['home_xg'].sum() + away_matches['away_xg'].sum()
        
        total_conceded = home_matches['away_goals'].sum() + away_matches['home_goals'].sum()
        total_xga = home_matches['away_xg'].sum() + away_matches['home_xg'].sum()
        
        off_eff = total_goals / max(total_xg, 1.0)
        def_eff = total_conceded / max(total_xga, 1.0) # Lower is better
        
        return round(off_eff, 2), round(def_eff, 2)
