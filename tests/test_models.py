import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.ensemble import EnsemblePredictor
from src.models.poisson_model import PoissonMatchModel
from src.models.ml_model import GradientBoostingModel
from src.features.build_features import FeatureEngineer
from src.models.team_analytics import TeamAnalytics
from src.models.tournament_simulator import TournamentSimulator


# Fixtures
@pytest.fixture
def sample_historical_data():
    """Generate sample historical match data for testing."""
    teams = ["Argentina", "France", "Brazil", "England", "Spain", "Germany"]
    data = []
    for i in range(100):
        home_team = np.random.choice(teams)
        away_team = np.random.choice([t for t in teams if t != home_team])
        
        data.append({
            'date': f'2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}',
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': np.random.randint(0, 5),
            'away_goals': np.random.randint(0, 5),
            'home_xg': round(np.random.uniform(0.5, 3.0), 2),
            'away_xg': round(np.random.uniform(0.5, 3.0), 2),
            'home_possession': np.random.randint(30, 70),
            'away_possession': np.random.randint(30, 70),
            'tournament': 'Friendly'
        })
    
    return pd.DataFrame(data)


class TestPoissonModel:
    """Tests for Poisson statistical model."""
    
    def test_poisson_model_initialization(self, sample_historical_data):
        """Test that Poisson model initializes correctly."""
        model = PoissonMatchModel(sample_historical_data)
        assert model is not None
        assert model.global_avg_goals > 0
    
    def test_poisson_prediction_output_structure(self, sample_historical_data):
        """Test that Poisson predictions return correct structure."""
        model = PoissonMatchModel(sample_historical_data)
        preds = model.predict_match("Argentina", "France")
        
        required_keys = ['home_win', 'draw', 'away_win', 'home_xg', 'away_xg', 'expected_score']
        for key in required_keys:
            assert key in preds, f"Missing key: {key}"
    
    def test_poisson_probabilities_sum_to_one(self, sample_historical_data):
        """Test that win/draw/loss probabilities sum to ~1.0."""
        model = PoissonMatchModel(sample_historical_data)
        preds = model.predict_match("Argentina", "France")
        
        total_prob = preds['home_win'] + preds['draw'] + preds['away_win']
        assert abs(total_prob - 1.0) < 0.01, "Probabilities do not sum to 1.0"
    
    def test_poisson_xg_positive(self, sample_historical_data):
        """Test that expected goals are positive."""
        model = PoissonMatchModel(sample_historical_data)
        preds = model.predict_match("Argentina", "France")
        
        assert preds['home_xg'] > 0, "Home xG should be positive"
        assert preds['away_xg'] > 0, "Away xG should be positive"


class TestMLModel:
    """Tests for Machine Learning model."""
    
    def test_ml_model_initialization(self, sample_historical_data):
        """Test that ML model initializes correctly."""
        model = GradientBoostingModel(sample_historical_data)
        assert model.is_trained is True
    
    def test_ml_model_prediction_structure(self, sample_historical_data):
        """Test ML model prediction output structure."""
        model = GradientBoostingModel(sample_historical_data)
        home_features = {'form': 0.6, 'off_eff': 1.1, 'def_eff': 0.9}
        away_features = {'form': 0.4, 'off_eff': 0.9, 'def_eff': 1.1}
        
        preds = model.predict_probabilities(home_features, away_features)
        
        required_keys = ['home_win', 'draw', 'away_win']
        for key in required_keys:
            assert key in preds, f"Missing key: {key}"
    
    def test_ml_probabilities_valid_range(self, sample_historical_data):
        """Test that probabilities are between 0 and 1."""
        model = GradientBoostingModel(sample_historical_data)
        home_features = {'form': 0.6, 'off_eff': 1.1, 'def_eff': 0.9}
        away_features = {'form': 0.4, 'off_eff': 0.9, 'def_eff': 1.1}
        
        preds = model.predict_probabilities(home_features, away_features)
        
        for prob in preds.values():
            assert 0 <= prob <= 1, f"Probability {prob} out of valid range"


class TestEnsemblePredictor:
    """Tests for Ensemble prediction model."""
    
    def test_ensemble_initialization(self, sample_historical_data):
        """Test ensemble model initializes correctly."""
        ensemble = EnsemblePredictor(sample_historical_data)
        assert ensemble.poisson is not None
        assert ensemble.ml_model is not None
    
    def test_ensemble_prediction_structure(self, sample_historical_data):
        """Test ensemble prediction output structure."""
        ensemble = EnsemblePredictor(sample_historical_data)
        home_features = {'form': 0.6, 'off_eff': 1.1, 'def_eff': 0.9}
        away_features = {'form': 0.4, 'off_eff': 0.9, 'def_eff': 1.1}
        
        preds = ensemble.generate_prediction("Argentina", "France", home_features, away_features)
        
        required_keys = ['home_win_prob', 'draw_prob', 'away_win_prob', 'home_xg', 'away_xg', 'confidence_level']
        for key in required_keys:
            assert key in preds, f"Missing key: {key}"
    
    def test_ensemble_probabilities_sum_to_one(self, sample_historical_data):
        """Test that ensemble probabilities sum to 1.0."""
        ensemble = EnsemblePredictor(sample_historical_data)
        home_features = {'form': 0.6, 'off_eff': 1.1, 'def_eff': 0.9}
        away_features = {'form': 0.4, 'off_eff': 0.9, 'def_eff': 1.1}
        
        preds = ensemble.generate_prediction("Argentina", "France", home_features, away_features)
        
        total_prob = preds['home_win_prob'] + preds['draw_prob'] + preds['away_win_prob']
        assert abs(total_prob - 1.0) < 0.01, "Probabilities do not sum to 1.0"


class TestFeatureEngineer:
    """Tests for Feature Engineering."""
    
    def test_feature_engineer_initialization(self, sample_historical_data):
        """Test feature engineer initializes correctly."""
        fe = FeatureEngineer(sample_historical_data)
        assert fe.df is not None
    
    def test_recent_form_calculation(self, sample_historical_data):
        """Test recent form calculation returns valid value."""
        fe = FeatureEngineer(sample_historical_data)
        form = fe.get_team_recent_form("Argentina", "2023-06-15")
        
        assert 0 <= form <= 1, f"Form {form} out of valid range [0, 1]"
    
    def test_efficiency_calculation(self, sample_historical_data):
        """Test efficiency calculation returns positive values."""
        fe = FeatureEngineer(sample_historical_data)
        off_eff, def_eff = fe.get_efficiencies("Argentina")
        
        assert off_eff > 0, "Offensive efficiency should be positive"
        assert def_eff > 0, "Defensive efficiency should be positive"
    
    def test_empty_team_handling(self, sample_historical_data):
        """Test that missing teams return neutral/default values."""
        fe = FeatureEngineer(sample_historical_data)
        form = fe.get_team_recent_form("NonexistentTeam", "2023-06-15")
        off_eff, def_eff = fe.get_efficiencies("NonexistentTeam")
        
        assert form == 0.5, "Missing team should return neutral form"
        assert off_eff == 1.0 and def_eff == 1.0, "Missing team should return neutral efficiencies"


class TestTeamAnalytics:
    """Tests for Team Analytics module."""
    
    def test_team_analytics_initialization(self, sample_historical_data):
        """Test team analytics initializes correctly."""
        ta = TeamAnalytics(sample_historical_data)
        assert ta.df is not None
    
    def test_strength_score_calculation(self, sample_historical_data):
        """Test team strength score calculation."""
        ta = TeamAnalytics(sample_historical_data)
        teams = ["Argentina", "France", "Brazil"]
        strength_scores = ta.calculate_team_strength(teams)
        
        assert len(strength_scores) == 3, "Should return strength scores for all teams"
        for score in strength_scores.values():
            assert 0 <= score <= 1, f"Strength score {score} out of valid range"
    
    def test_rankings_generation(self, sample_historical_data):
        """Test rankings dataframe generation."""
        ta = TeamAnalytics(sample_historical_data)
        teams = ["Argentina", "France", "Brazil", "England", "Spain", "Germany"]
        rankings = ta.generate_team_rankings(teams)
        
        assert len(rankings) == len(teams), "Rankings should include all teams"
        assert 'Rank' in rankings.columns, "Rankings should include Rank column"
        assert rankings['Rank'].iloc[0] == 1, "Top ranked team should have rank 1"
    
    def test_team_comparison(self, sample_historical_data):
        """Test head-to-head team comparison."""
        ta = TeamAnalytics(sample_historical_data)
        comparison = ta.compare_teams("Argentina", "France")
        
        assert "Argentina" in comparison, "Comparison should include Argentina"
        assert "France" in comparison, "Comparison should include France"
        assert "advantage" in comparison, "Comparison should determine advantage"


class TestTournamentSimulator:
    """Tests for Tournament Simulator."""
    
    def test_tournament_sim_initialization(self, sample_historical_data):
        """Test tournament simulator initializes correctly."""
        groups = {
            'A': ['Argentina', 'France', 'Brazil', 'England'],
            'B': ['Spain', 'Germany', 'Italy', 'Portugal']
        }
        sim = TournamentSimulator(sample_historical_data, groups)
        assert sim.groups == groups
    
    def test_group_stage_simulation(self, sample_historical_data):
        """Test group stage simulation."""
        groups = {
            'A': ['Argentina', 'France', 'Brazil', 'England'],
            'B': ['Spain', 'Germany', 'Italy', 'Portugal']
        }
        sim = TournamentSimulator(sample_historical_data, groups)
        group_standings = sim.simulate_group_stage(num_simulations=1)
        
        assert 'A' in group_standings, "Should have Group A standings"
        assert 'B' in group_standings, "Should have Group B standings"
        assert len(group_standings['A']) >= 2, "Group should have at least 2 teams"
    
    def test_knockout_stage_simulation(self, sample_historical_data):
        """Test knockout stage simulation."""
        groups = {
            'A': ['Argentina', 'France', 'Brazil', 'England'],
            'B': ['Spain', 'Germany', 'Italy', 'Portugal']
        }
        sim = TournamentSimulator(sample_historical_data, groups)
        group_standings = sim.simulate_group_stage(num_simulations=1)
        knockout_results = sim.simulate_knockout_stage(group_standings)
        
        required_rounds = ['Round of 16', 'Quarterfinals', 'Semifinals', 'Final']
        for round_name in required_rounds:
            assert round_name in knockout_results, f"Missing {round_name}"


class TestIntegration:
    """Integration tests for the entire pipeline."""
    
    def test_full_prediction_pipeline(self, sample_historical_data):
        """Test the complete prediction pipeline."""
        fe = FeatureEngineer(sample_historical_data)
        ensemble = EnsemblePredictor(sample_historical_data)
        
        # Get features
        h_form = fe.get_team_recent_form("Argentina", "2023-06-15")
        a_form = fe.get_team_recent_form("France", "2023-06-15")
        h_off_eff, h_def_eff = fe.get_efficiencies("Argentina")
        a_off_eff, a_def_eff = fe.get_efficiencies("France")
        
        # Make prediction
        h_features = {'form': h_form, 'off_eff': h_off_eff, 'def_eff': h_def_eff}
        a_features = {'form': a_form, 'off_eff': a_off_eff, 'def_eff': a_def_eff}
        
        preds = ensemble.generate_prediction("Argentina", "France", h_features, a_features)
        
        # Verify prediction
        total_prob = preds['home_win_prob'] + preds['draw_prob'] + preds['away_win_prob']
        assert abs(total_prob - 1.0) < 0.01, "Pipeline output should have valid probabilities"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
