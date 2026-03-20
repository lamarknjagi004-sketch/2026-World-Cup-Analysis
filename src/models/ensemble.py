from .poisson_model import PoissonMatchModel
from .ml_model import GradientBoostingModel

class EnsemblePredictor:
    """
    The calibration layer and ensemble framework. 
    Combines outputs from multiple models to issue the final probabilistic determination.
    """
    def __init__(self, df):
        self.poisson = PoissonMatchModel(df)
        self.ml_model = GradientBoostingModel(df)
        
    def generate_prediction(self, home_team, away_team, home_features, away_features, market_odds=None):
        poisson_preds = self.poisson.predict_match(home_team, away_team)
        ml_preds = self.ml_model.predict_probabilities(home_features, away_features)
        
        # Weighted ensemble: 60% Statistical (Poisson), 40% ML Pattern Recognition
        ens_home = (poisson_preds['home_win'] * 0.6) + (ml_preds['home_win'] * 0.4)
        ens_draw = (poisson_preds['draw'] * 0.6) + (ml_preds['draw'] * 0.4)
        ens_away = (poisson_preds['away_win'] * 0.6) + (ml_preds['away_win'] * 0.4)
        
        # Market Alignment Factor (Optional calibration if odds deviate significantly)
        if market_odds:
            # Shift 10% weight towards implied market odds to reduce systemic model bias
            ens_home = (ens_home * 0.9) + (market_odds['implied_home_win'] * 0.1)
            ens_draw = (ens_draw * 0.9) + (market_odds['implied_draw'] * 0.1)
            ens_away = (ens_away * 0.9) + (market_odds['implied_away_win'] * 0.1)
            
        # Final Normalization
        total = ens_home + ens_draw + ens_away
        
        return {
            'home_win_prob': round(ens_home / total, 3),
            'draw_prob': round(ens_draw / total, 3),
            'away_win_prob': round(ens_away / total, 3),
            'home_xg': poisson_preds['home_xg'],
            'away_xg': poisson_preds['away_xg'],
            'expected_score': poisson_preds['expected_score'],
            'confidence_level': self._calculate_confidence(ens_home, ens_away)
        }
        
    def _calculate_confidence(self, p_home, p_away):
        # A simple heuristic for explainability: higher variance implies greater certainty.
        diff = abs(p_home - p_away)
        if diff > 0.4: return "High"
        if diff > 0.2: return "Medium-High"
        if diff > 0.1: return "Medium"
        return "Low (Toss-up)"
