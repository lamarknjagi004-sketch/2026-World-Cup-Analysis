import numpy as np
import pandas as pd
from scipy.stats import poisson

class PoissonMatchModel:
    """
    A foundational statistical model simulating match outcomes based on average expected scoring parameters.
    Based on underlying Poisson distributions as seen in standard Dixon-Coles modeling.
    """
    def __init__(self, historical_df):
        self.df = historical_df
        # Calculate offensive/defensive strengths based on historical average goals
        self.team_stats = self._calculate_strengths()
        if self.df is not None and not self.df.empty:
            self.global_avg_goals = (self.df['home_goals'].sum() + self.df['away_goals'].sum()) / (2 * len(self.df))
        else:
            self.global_avg_goals = 1.4

    def _calculate_strengths(self):
        if self.df is None or self.df.empty:
            return {}
            
        stats = {}
        teams = pd.concat([self.df['home_team'], self.df['away_team']]).unique()
        for t in teams:
            home_scored = self.df[self.df['home_team'] == t]['home_goals'].mean()
            away_scored = self.df[self.df['away_team'] == t]['away_goals'].mean()
            stats[t] = {'att_strength': (home_scored + away_scored) / 2.0}
        return stats

    def predict_match(self, home_team, away_team):
        home_att = self.team_stats.get(home_team, {}).get('att_strength', self.global_avg_goals)
        away_att = self.team_stats.get(away_team, {}).get('att_strength', self.global_avg_goals)
        
        # Base xG calculations directly tie into historical attacking performance
        home_xg = max(0.1, home_att * 1.1) # Small structural home/tier advantage 
        away_xg = max(0.1, away_att * 0.9)
        
        # Calculate matrix of exact outcome probabilities using Poisson processes
        max_goals = 10
        score_matrix = np.zeros((max_goals, max_goals))
        for h in range(max_goals):
            for a in range(max_goals):
                score_matrix[h, a] = poisson.pmf(h, home_xg) * poisson.pmf(a, away_xg)
                
        # Aggregate the matrices into Win / Draw / Loss probabilities
        home_win_prob = np.sum(np.tril(score_matrix, -1))
        draw_prob = np.sum(np.diag(score_matrix))
        away_win_prob = np.sum(np.triu(score_matrix, 1))
        
        # Find the most likely exact expected score
        flat_idx = np.argmax(score_matrix)
        most_likely_h, most_likely_a = np.unravel_index(flat_idx, score_matrix.shape)
        
        return {
            'home_win': round(home_win_prob, 3),
            'draw': round(draw_prob, 3),
            'away_win': round(away_win_prob, 3),
            'home_xg': round(home_xg, 2),
            'away_xg': round(away_xg, 2),
            'expected_score': f"{most_likely_h} - {most_likely_a}"
        }
