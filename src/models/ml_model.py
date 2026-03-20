# ML prediction wrapper

class GradientBoostingModel:
    """
    Represents the Machine Learning portion of the predicting engine.
    In a fully trained environment, this wraps XGBoost/LightGBM. 
    Here we represent the inference block mapping engineered features to probabilities.
    """
    def __init__(self, historical_df):
        # self.model = xgb.XGBClassifier()
        # self.model.fit(X, y)
        self.is_trained = True
        
    def predict_probabilities(self, home_features, away_features):
        """
        Simulates ML probabilities based on input feature vectors.
        """
        # Form diff evaluates momentum heading into a match
        form_diff = home_features.get('form', 0.5) - away_features.get('form', 0.5)
        
        # Tactical efficiency differential
        off_eff_diff = home_features.get('off_eff', 1.0) - away_features.get('def_eff', 1.0)
        
        p_home = 0.35 + (form_diff * 0.15) + (off_eff_diff * 0.05)
        p_away = 0.35 - (form_diff * 0.15) - (off_eff_diff * 0.05)
        p_draw = 1.0 - (p_home + p_away)
        
        # Normalize to ensure validity
        p_home_adj = max(0.01, p_home)
        p_away_adj = max(0.01, p_away)
        p_draw_adj = max(0.01, p_draw)
        total = p_home_adj + p_away_adj + p_draw_adj
        
        return {
            'home_win': round(p_home_adj / total, 3),
            'draw': round(p_draw_adj / total, 3),
            'away_win': round(p_away_adj / total, 3)
        }
