import random
import numpy as np
import pandas as pd
from itertools import combinations
from .ensemble import EnsemblePredictor
from ..features.build_features import FeatureEngineer




class TournamentSimulator:
    """
    Simulates the 2026 FIFA World Cup tournament structure:
    - 12 groups of 4 teams
    - Group stage with round-robin matches
    - Knockout stages (Round of 16, Quarterfinals, Semifinals, Final)
    """
    
    def __init__(self, historical_df, groups):
        """
        Args:
            historical_df: Historical match data for model training
            groups: Dictionary with group names as keys and list of 4 teams as values
                   Example: {'A': ['Argentina', 'France', 'Brazil', 'England']}
        """
        self.historical_df = historical_df
        self.groups = groups
        self.ensemble = EnsemblePredictor(historical_df)
        self.feature_engineer = FeatureEngineer(historical_df)
        self.results = {}
        self.group_standings = {}
        
    def simulate_group_stage(self, num_simulations=1):
        """
        Simulates the group stage round-robin matches.
        Returns group standings and qualified teams.
        """
        group_qualifiers = {}
        
        for group_name, teams in self.groups.items():
            if num_simulations == 1:
                standings = self._simulate_single_group(teams)
            else:
                standings = self._simulate_group_aggregate(teams, num_simulations)
            
            group_qualifiers[group_name] = standings
            self.group_standings[group_name] = standings
            
        return group_qualifiers
    
    def _simulate_single_group(self, teams):
        """Simulates all matches within a group once."""
        standings = {team: {'points': 0, 'gf': 0, 'ga': 0, 'gd': 0} for team in teams}
        
        # All combinations of home/away matches
        for home_team, away_team in combinations(teams, 2):
            preds = self._predict_match(home_team, away_team)
            home_goals = np.random.poisson(preds['home_xg'])
            away_goals = np.random.poisson(preds['away_xg'])
            
            standings[home_team]['gf'] += home_goals
            standings[home_team]['ga'] += away_goals
            standings[away_team]['gf'] += away_goals
            standings[away_team]['ga'] += home_goals
            standings[home_team]['gd'] = standings[home_team]['gf'] - standings[home_team]['ga']
            standings[away_team]['gd'] = standings[away_team]['gf'] - standings[away_team]['ga']
            
            if home_goals > away_goals:
                standings[home_team]['points'] += 3
            elif home_goals < away_goals:
                standings[away_team]['points'] += 3
            else:
                standings[home_team]['points'] += 1
                standings[away_team]['points'] += 1
        
        # Sort by points, then goal difference, then goals for
        sorted_teams = sorted(
            standings.items(),
            key=lambda x: (-x[1]['points'], -x[1]['gd'], -x[1]['gf'])
        )
        
        return sorted_teams
    
    def _simulate_group_aggregate(self, teams, num_simulations):
        """Runs multiple simulations and aggregates the probability distribution."""
        qualification_counts = {team: 0 for team in teams}
        
        for _ in range(num_simulations):
            standings = self._simulate_single_group(teams)
            qualified = standings[:2]  # Top 2 teams advance
            for team, _ in qualified:
                qualification_counts[team] += 1
        
        # Convert to probabilities and return as standings-like format
        standings = [
            (team, {
                'qual_prob': qualification_counts[team] / num_simulations,
                'points': 999  # Placeholder for sorting
            })
            for team in teams
        ]
        
        return sorted(standings, key=lambda x: -x[1]['qual_prob'])
    
    def simulate_knockout_stage(self, qualified_teams, from_group_stage=True):
        """
        Simulates Round of 16 through Final.
        Uses UEFA knockout structure: 1st place teams play 2nd place teams with bracket seeding.
        """
        # Create Round of 16 matchups based on group standings
        round_16_matches = self._create_knockout_matchups(qualified_teams)
        knockout_results = {'Round of 16': [], 'Quarterfinals': [], 'Semifinals': [], 'Final': []}
        
        next_round_matches = round_16_matches
        round_names = ['Round of 16', 'Quarterfinals', 'Semifinals', 'Final']
        
        for round_name in round_names:
            current_round_results = []
            next_round_teams = []
            
            for home_team, away_team in next_round_matches:
                winner = self._simulate_knockout_match(home_team, away_team)
                current_round_results.append({
                    'home': home_team,
                    'away': away_team,
                    'winner': winner
                })
                next_round_teams.append(winner)
            
            knockout_results[round_name] = current_round_results
            
            if round_name != 'Final':
                next_round_matches = [(next_round_teams[i], next_round_teams[i+1]) 
                                     for i in range(0, len(next_round_teams), 2)]
        
        self.results['knockout'] = knockout_results
        return knockout_results
    
    def _create_knockout_matchups(self, qualified_teams):
        """Creates Round of 16 matchups based on 2026 World Cup structure."""
        # Separate 1st and 2nd place teams
        first_place = []
        second_place = []
        
        for group_name in sorted(self.groups.keys()):
            standings = qualified_teams[group_name]
            if len(standings) >= 2:
                first_place.append(standings[0][0])
                second_place.append(standings[1][0])
        
        # Standard knockout seeding (1st places paired with 2nd places)
        matches = [
            (first_place[0], second_place[1]),
            (first_place[1], second_place[0]),
            (first_place[2], second_place[3]),
            (first_place[3], second_place[2]),
            (first_place[4], second_place[5]),
            (first_place[5], second_place[4]),
            (first_place[6], second_place[7]),
            (first_place[7], second_place[6]),
        ]
        
        return matches
    
    def _simulate_knockout_match(self, home_team, away_team, max_attempts=2):
        """
        Simulates a knockout match. If draw after regular time, goes to extra time/penalties.
        max_attempts: Number of periods (initially 90 min, then extra time if tied)
        """
        for attempt in range(max_attempts):
            preds = self._predict_match(home_team, away_team)
            home_goals = np.random.poisson(preds['home_xg'])
            away_goals = np.random.poisson(preds['away_xg'])
            
            if home_goals > away_goals:
                return home_team
            elif away_goals > home_goals:
                return away_team
            # If tied, try extra time (second attempt)
        
        # If still tied after extra time, go to penalties (50-50 coin flip)
        return home_team if random.random() > 0.5 else away_team
    
    def _predict_match(self, home_team, away_team):
        """Gets prediction from ensemble model."""
        h_form = self.feature_engineer.get_team_recent_form(
            home_team, pd.Timestamp.now().strftime("%Y-%m-%d")
        )
        a_form = self.feature_engineer.get_team_recent_form(
            away_team, pd.Timestamp.now().strftime("%Y-%m-%d")
        )
        
        h_off_eff, h_def_eff = self.feature_engineer.get_efficiencies(home_team)
        a_off_eff, a_def_eff = self.feature_engineer.get_efficiencies(away_team)
        
        h_features = {'form': h_form, 'off_eff': h_off_eff, 'def_eff': h_def_eff}
        a_features = {'form': a_form, 'off_eff': a_off_eff, 'def_eff': a_def_eff}
        
        preds = self.ensemble.generate_prediction(home_team, away_team, h_features, a_features)
        return preds
    
    def get_trophy_winners_probabilities(self, num_simulations=1000):
        """
        Monte Carlo simulation to generate tournament winner probabilities.
        """
        trophy_winners = {team: 0 for group_teams in self.groups.values() for team in group_teams}
        
        for _ in range(num_simulations):
            group_qualifiers = self.simulate_group_stage(num_simulations=1)
            knockout_results = self.simulate_knockout_stage(group_qualifiers, from_group_stage=True)
            
            final_result = knockout_results['Final'][0]
            champion = final_result['winner']
            trophy_winners[champion] += 1
        
        # Convert to probabilities and sort
        trophy_probs = {
            team: count / num_simulations 
            for team, count in trophy_winners.items()
        }
        
        return dict(sorted(trophy_probs.items(), key=lambda x: -x[1]))
