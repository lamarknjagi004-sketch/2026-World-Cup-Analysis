import pandas as pd
import numpy as np
from .ensemble import EnsemblePredictor
from ..features.build_features import FeatureEngineer


class TeamAnalytics:
    """
    Comprehensive team analytics and ranking system for the 2026 World Cup.
    Provides team strength rankings, key performance indicators, and comparisons.
    """
    
    def __init__(self, historical_df):
        self.df = historical_df
        self.ensemble = EnsemblePredictor(historical_df)
        self.feature_engineer = FeatureEngineer(historical_df)
        
    def calculate_team_strength(self, teams):
        """
        Calculates a composite strength score for each team based on:
        - Historical win rate
        - Goal differential
        - Recent form
        - Offensive and defensive efficiency
        """
        team_strengths = {}
        
        for team in teams:
            # Historical statistics
            home_matches = self.df[self.df['home_team'] == team]
            away_matches = self.df[self.df['away_team'] == team]
            
            total_matches = len(home_matches) + len(away_matches)
            
            if total_matches == 0:
                team_strengths[team] = 0.5
                continue
            
            # Win rate
            home_wins = len(home_matches[home_matches['home_goals'] > home_matches['away_goals']])
            away_wins = len(away_matches[away_matches['away_goals'] > away_matches['home_goals']])
            total_wins = home_wins + away_wins
            win_rate = total_wins / total_matches
            
            # Goal differential
            home_gd = (home_matches['home_goals'].sum() - home_matches['away_goals'].sum())
            away_gd = (away_matches['away_goals'].sum() - away_matches['home_goals'].sum())
            total_gd = home_gd + away_gd
            normalized_gd = total_gd / max(total_matches, 1)
            
            # Recent form (last 5 matches)
            recent_form = self.feature_engineer.get_team_recent_form(
                team, pd.Timestamp.now().strftime("%Y-%m-%d"), last_n=5
            )
            
            # Efficiencies
            off_eff, def_eff = self.feature_engineer.get_efficiencies(team)
            
            # Composite strength score (weighted average)
            strength_score = (
                (win_rate * 0.30) +
                (min(normalized_gd / 3 + 0.5, 1.0) * 0.25) +  # Normalized GD
                (recent_form * 0.25) +
                (min(off_eff / 1.2, 1.0) * 0.10) +
                (max(1.0 - def_eff, 0) * 0.10)  # Lower defense efficiency is better
            )
            
            team_strengths[team] = round(strength_score, 3)
        
        return team_strengths
    
    def generate_team_rankings(self, teams):
        """
        Generates a detailed ranking table with team strength metrics.
        """
        rankings = []
        strength_scores = self.calculate_team_strength(teams)
        
        for team in teams:
            home_matches = self.df[self.df['home_team'] == team]
            away_matches = self.df[self.df['away_team'] == team]
            
            total_matches = len(home_matches) + len(away_matches)
            total_goals_for = home_matches['home_goals'].sum() + away_matches['away_goals'].sum()
            total_goals_against = home_matches['away_goals'].sum() + away_matches['home_goals'].sum()
            
            off_eff, def_eff = self.feature_engineer.get_efficiencies(team)
            recent_form = self.feature_engineer.get_team_recent_form(
                team, pd.Timestamp.now().strftime("%Y-%m-%d"), last_n=5
            )
            
            rankings.append({
                'Team': team,
                'Strength Score': strength_scores[team],
                'Matches': total_matches,
                'Goals For': total_goals_for,
                'Goals Against': total_goals_against,
                'Goal Diff': total_goals_for - total_goals_against,
                'Off Efficiency': off_eff,
                'Def Efficiency': def_eff,
                'Recent Form': round(recent_form, 2)
            })
        
        rankings_df = pd.DataFrame(rankings).sort_values('Strength Score', ascending=False).reset_index(drop=True)
        rankings_df['Rank'] = range(1, len(rankings_df) + 1)
        
        return rankings_df[['Rank', 'Team', 'Strength Score', 'Matches', 'Goals For', 
                           'Goals Against', 'Goal Diff', 'Off Efficiency', 'Def Efficiency', 'Recent Form']]
    
    def compare_teams(self, team1, team2):
        """
        Provides a detailed head-to-head comparison between two teams.
        """
        strength_scores = self.calculate_team_strength([team1, team2])
        
        # Historical records
        t1_vs_t2 = len(self.df[
            ((self.df['home_team'] == team1) & (self.df['away_team'] == team2)) |
            ((self.df['home_team'] == team2) & (self.df['away_team'] == team1))
        ])
        
        # Head-to-head results
        t1_home_vs_t2_away = self.df[
            (self.df['home_team'] == team1) & (self.df['away_team'] == team2)
        ]
        t1_home_wins = len(t1_home_vs_t2_away[t1_home_vs_t2_away['home_goals'] > t1_home_vs_t2_away['away_goals']])
        t1_home_draws = len(t1_home_vs_t2_away[t1_home_vs_t2_away['home_goals'] == t1_home_vs_t2_away['away_goals']])
        
        # Team statistics
        off_eff1, def_eff1 = self.feature_engineer.get_efficiencies(team1)
        off_eff2, def_eff2 = self.feature_engineer.get_efficiencies(team2)
        
        form1 = self.feature_engineer.get_team_recent_form(
            team1, pd.Timestamp.now().strftime("%Y-%m-%d"), last_n=5
        )
        form2 = self.feature_engineer.get_team_recent_form(
            team2, pd.Timestamp.now().strftime("%Y-%m-%d"), last_n=5
        )
        
        return {
            f'{team1}': {
                'strength_score': strength_scores[team1],
                'offensive_efficiency': off_eff1,
                'defensive_efficiency': def_eff1,
                'recent_form': round(form1, 2),
                'h2h_record': {'wins': t1_home_wins, 'draws': t1_home_draws, 'games': t1_vs_t2}
            },
            f'{team2}': {
                'strength_score': strength_scores[team2],
                'offensive_efficiency': off_eff2,
                'defensive_efficiency': def_eff2,
                'recent_form': round(form2, 2),
                'h2h_record': {'wins': len(t1_home_vs_t2_away) - t1_home_wins - t1_home_draws,
                               'draws': t1_home_draws, 'games': t1_vs_t2}
            },
            'advantage': team1 if strength_scores[team1] > strength_scores[team2] else team2
        }
    
    def get_team_seasonality(self, team, window=10):
        """
        Analyzes team performance across the dataset to identify any seasonal patterns.
        Returns average goals scored/conceded in each month.
        """
        team_matches = pd.concat([
            self.df[self.df['home_team'] == team],
            self.df[self.df['away_team'] == team]
        ])
        
        if len(team_matches) == 0:
            return {}
        
        team_matches['date'] = pd.to_datetime(team_matches['date'])
        team_matches['month'] = team_matches['date'].dt.month
        
        # Calculate goals for and against by month
        monthly_stats = {}
        for month in range(1, 13):
            month_matches = team_matches[team_matches['month'] == month]
            if len(month_matches) > 0:
                gf = (month_matches[month_matches['home_team'] == team]['home_goals'].sum() +
                      month_matches[month_matches['away_team'] == team]['away_goals'].sum())
                ga = (month_matches[month_matches['home_team'] == team]['away_goals'].sum() +
                      month_matches[month_matches['away_team'] == team]['home_goals'].sum())
                
                monthly_stats[month] = {
                    'goals_for': round(gf / len(month_matches), 2),
                    'goals_against': round(ga / len(month_matches), 2),
                    'games': len(month_matches)
                }
        
        return monthly_stats
