# Development Guide

## 🛠️ Contributing to the Predictive Analysis Engine

This guide covers development workflows, code standards, testing procedures, and extension patterns for contributors.

---

## 🚀 Getting Started as a Developer

### Development Environment Setup

```bash
# Clone repository
cd "Predictive analysis"

# Create development venv
python -m venv .venv-dev
.venv-dev\Scripts\activate

# Install with dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy sphinx
```

### Project Structure for Developers

```
src/
├── dashboard/          # Streamlit UI (modify cautiously)
├── data/               # Data loading/API integration (extend here)
├── features/           # Feature engineering (priority for improvement)
├── models/             # Prediction models (main development area)
│   ├── ensemble.py     # Primary file for weight tuning
│   ├── ml_model.py     # Priority: Implement training
│   ├── poisson_model.py # Stable - avoid major changes
│   └── ...
└── validation/         # Testing framework (extend for new metrics)
```

---

## 📋 Code Standards

### Naming Conventions

```python
# Variables
team_name = "Argentina"           # snake_case
GLOBAL_CONSTANT = 1.5             # UPPER_CASE
TournamentGradeEnum = "Group"    # PascalCase for classes

# Functions
def compute_team_form():          # snake_case
def _private_helper():            # Leading underscore for private

# Files
ensemble.py                       # snake_case
build_features.py                 # Descriptive names
```

### Documentation Standards

```python
def compute_offensive_efficiency(team: str, matches: List[Dict]) -> float:
    """
    Calculate offensive efficiency for a team.
    
    Offensive efficiency = Goals / Shots on Target
    Measures finishing quality.
    
    Args:
        team: Team name (str)
        matches: List of match dictionaries with team stats
        
    Returns:
        float: Efficiency score [0.5, 2.0]
        
    Example:
        >>> eff = compute_offensive_efficiency('Argentina', matches)
        >>> print(eff)
        1.25
        
    Notes:
        - Returns 1.0 if insufficient data
        - Clipped to [0.5, 2.0] range
    """
    ...
```

### Type Hints

```python
from typing import Dict, List, Optional, Tuple

def generate_prediction(
    home_team: str,
    away_team: str,
    home_features: Dict[str, float],
    away_features: Optional[Dict[str, float]] = None,
    market_odds: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """Generate match outcome prediction."""
    ...
```

### Code Formatting

```bash
# Format with Black
black src/

# Check with Flake8
flake8 src/ --max-line-length=100

# Type checking with Mypy
mypy src/models/ --ignore-missing-imports

# All three: Pre-commit hook
git add .
git commit -m "Feature: Add injury adjustments to model"
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
# tests/test_ensemble.py
import pytest
from src.models.ensemble import EnsemblePredictor

@pytest.fixture
def ensemble_model():
    """Fixture: Initialize ensemble with test data"""
    df = pd.read_csv('data/historical_matches_test.csv')
    return EnsemblePredictor(df)

def test_prediction_normalization(ensemble_model):
    """Test: Probabilities sum to 1.0"""
    pred = ensemble_model.generate_prediction('Team1', 'Team2', {}, {})
    total = pred['home_win_prob'] + pred['draw_prob'] + pred['away_win_prob']
    assert abs(total - 1.0) < 0.01, "Probabilities don't sum to 1.0"

def test_confidence_assignment():
    """Test: Confidence levels assigned correctly"""
    conf = ensemble._calculate_confidence(0.70, 0.15)
    assert conf == "High", "Diff > 0.40 should be High"
    
    conf = ensemble._calculate_confidence(0.55, 0.35)
    assert conf == "Medium-High", "Diff 0.20-0.40 should be Medium-High"

def test_edge_cases():
    """Test: Handle missing data gracefully"""
    # New team (no history)
    pred = ensemble.generate_prediction('UnknownTeam', 'Argentina', {}, {})
    assert pred is not None, "Should handle new teams"
    
    # Empty features
    pred = ensemble.generate_prediction('Team1', 'Team2', {}, {})
    assert pred is not None, "Should handle missing features"
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_ensemble.py::test_prediction_normalization

# Run with coverage
pytest tests/ --cov=src/ --cov-report=html

# Run only fast tests
pytest tests/ -m "not slow"
```

### Integration Tests

```python
# tests/test_integration.py
def test_end_to_end_prediction():
    """Integration: Full pipeline from data to prediction"""
    # Load data
    df = pd.read_csv('data/historical_matches.csv')
    
    # Initialize ensemble
    ensemble = EnsemblePredictor(df)
    
    # Generate prediction
    pred = ensemble.generate_prediction(
        'Argentina', 'France',
        {'form': 0.8, 'off_eff': 1.2, 'def_eff': 0.9},
        {'form': 0.75, 'off_eff': 1.15, 'def_eff': 0.95}
    )
    
    # Validate output
    assert pred['home_win_prob'] > 0
    assert pred['confidence_level'] in ['High', 'Medium-High', 'Medium', 'Low (Toss-up)']

def test_validation_pipeline():
    """Integration: Full validation process"""
    from src.validation.model_validator import validate_model
    
    predictions = [
        {'prediction': '1', 'result': '2-1', ...},
        {'prediction': '1X', 'result': '1-1', ...}
    ]
    
    validator = validate_model(predictions, 'data')
    report = validator.generate_report()
    
    assert report['total_matches'] == 2
    assert 'betting_accuracy' in report
```

---

## 🔄 Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/ml-model-training
# or
git checkout -b fix/confidence-calculation
# or
git checkout -b docs/add-architecture-guide
```

### 2. Make Changes

```python
# example: Implement XGBoost training (src/models/ml_model.py)

import xgboost as xgb
from sklearn.preprocessing import StandardScaler

class GradientBoostingModel:
    def __init__(self, historical_df):
        """Train XGBoost model on historical data"""
        # Extract features and target
        X = self._extract_features(historical_df)
        y = self._extract_target(historical_df)
        
        # Normalize features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            random_state=42,
            verbosity=1
        )
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict_probabilities(self, home_features, away_features):
        """Generate prediction from trained model"""
        feature_vector = self._combine_features(home_features, away_features)
        feature_scaled = self.scaler.transform([feature_vector])
        probs = self.model.predict_proba(feature_scaled)[0]
        
        return {
            'home_win': round(probs[0], 3),
            'draw': round(probs[1], 3),
            'away_win': round(probs[2], 3)
        }
```

### 3. Write Tests

```python
# tests/test_ml_model_training.py
import pytest
from src.models.ml_model import GradientBoostingModel

@pytest.fixture
def sample_data():
    """Create test dataset"""
    df = pd.DataFrame({
        'home_team': ['Team1', 'Team2', 'Team3'] * 10,
        'away_team': ['TeamA', 'TeamB', 'TeamC'] * 10,
        'result': [1, 0, 2] * 10,  # 1=home, 0=draw, 2=away
        'home_form': [0.7] * 30,
        'away_form': [0.6] * 30,
    })
    return df

def test_ml_model_training(sample_data):
    """Test: Model trains without errors"""
    model = GradientBoostingModel(sample_data)
    assert model.is_trained is True
    assert model.model is not None

def test_ml_predictions_after_training(sample_data):
    """Test: Predictions valid after training"""
    model = GradientBoostingModel(sample_data)
    probs = model.predict_probabilities({'form': 0.7}, {'form': 0.6})
    
    assert sum(probs.values()) == pytest.approx(1.0, abs=0.01)
    assert all(0 <= p <= 1 for p in probs.values())
```

### 4. Run Tests & Format

```bash
# Test
pytest tests/test_ml_model_training.py -v

# Format
black src/models/ml_model.py

# Lint
flake8 src/models/ml_model.py

# Type check
mypy src/models/ml_model.py --ignore-missing-imports
```

### 5. Commit & Push

```bash
git add src/models/ml_model.py tests/test_ml_model_training.py
git commit -m "feat: Implement XGBoost model training with sklearn integration"
git push origin feature/ml-model-training
```

### 6. Create Pull Request

```
Title: Implement ML Model Training with XGBoost
Description:
- Trains GradientBoostingModel on historical matches
- Improves model accuracy from 0% → 65%+
- Includes comprehensive tests
- All checks passing

Related: #42 (Improve ML accuracy)
```

---

## 🔧 Common Development Tasks

### Task 1: Add New Feature

```python
# src/features/build_features.py

def compute_recent_injuries(team: str, matches: List[Dict], lookback: int = 5) -> float:
    """
    Compute injury impact factor.
    
    Star player (5% xG reduction)
    Key player (3% xG reduction)
    Backup player (1% xG reduction)
    """
    recent = matches[-lookback:]
    injury_impact = 0.0
    
    for match in recent:
        if team in match.get('injuries', {}):
            injuries = match['injuries'][team]
            if injuries.get('star_player'):
                injury_impact -= 0.05
            if injuries.get('key_player'):
                injury_impact -= 0.03
    
    return max(-0.10, injury_impact)  # Cap reduction


# Use in ensemble.py
injury_adjustment = compute_recent_injuries(home_team, matches)
home_xg = home_xg * (1 + injury_adjustment)
```

### Task 2: Tune Model Hyperparameters

```python
# src/models/ensemble.py - Modify weights

"""Before (current)"""
ens_home = (poisson_preds['home_win'] * 0.6) + (ml_preds['home_win'] * 0.4)

"""After (tuned via validation)"""
# Increase Poisson weight (68% vs 40%)
ens_home = (poisson_preds['home_win'] * 0.68) + (ml_preds['home_win'] * 0.32)

"""Validation"""
# Run: python validate_full_dataset.py
# Measure: Betting accuracy improved from 70.07% → 71.5%?
```

### Task 3: Add Dashboard Section

```python
# src/dashboard/app.py - Add new tab

import streamlit as st

# Create tabs (after existing tabs)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Home", "Analytics", "Tournament", "Validation", "NEW_TAB"
])

with tab5:
    st.header("New Analysis Section")
    st.markdown("Description of new feature")
    
    # Add visualizations
    chart_data = df[['date', 'accuracy']].set_index('date')
    st.line_chart(chart_data)
    
    # Add controls
    metric = st.selectbox('Select metric', ['Accuracy', 'Confidence', 'Volume'])
    
    # Display results
    st.metric("Average Accuracy", f"{accuracy_pct:.1f}%")
```

---

## 🐛 Debugging

### Debug with Print Statements

```python
def generate_prediction(self, home_team, away_team, home_features, away_features):
    # Enable debugging
    DEBUG = True
    
    if DEBUG:
        print(f"Input: {home_team} vs {away_team}")
        print(f"Home features: {home_features}")
    
    poisson_preds = self.poisson.predict_match(home_team, away_team)
    if DEBUG:
        print(f"Poisson probs: {poisson_preds}")
    
    ml_preds = self.ml_model.predict_probabilities(home_features, away_features)
    if DEBUG:
        print(f"ML probs: {ml_preds}")
    
    # ... combine ...
    
    if DEBUG:
        print(f"Final prediction: {final_prediction}")
    
    return final_prediction
```

### Debug with Breakpoints

```python
import pdb

def generate_prediction(self, home_team, away_team, home_features, away_features):
    poisson_preds = self.poisson.predict_match(home_team, away_team)
    
    # Set breakpoint
    pdb.set_trace()  # Execution pauses here
    # In debugger: print(poisson_preds), c (continue), etc.
    
    ml_preds = self.ml_model.predict_probabilities(home_features, away_features)
    ...
```

### Debug with Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_prediction(self, home_team, away_team, home_features, away_features):
    logger.debug(f"Generating prediction for {home_team} vs {away_team}")
    logger.debug(f"Home features: {home_features}")
    
    poisson_preds = self.poisson.predict_match(home_team, away_team)
    logger.debug(f"Poisson result: {poisson_preds}")
    
    ...
```

---

## 📚 Extension Patterns

### Pattern 1: Add New Prediction Type

```python
# src/models/ensemble.py

def get_prediction_type_from_probabilities(self, p1, px, p2):
    """Predict bet type (1, X, 2, 1X, 12, X2)"""
    
    # Example: New type "High Scoring" (>2.5 goals)
    # Would need goal probability distribution
    
    max_prob = max(p1, px, p2)
    if max_prob == p1:
        return '1' if p1 > px else '1X'
    # ... etc
    
    # Future: return additional types like:
    # 'O2.5' (Over 2.5 goals)
    # 'BTS' (Both Teams Score)
    # 'BTTS' (Either team scores)
```

### Pattern 2: Add Market Integration

```python
# src/data/api_client.py

class LiveMatchAPI:
    def __init__(self):
        self.providers = ['Bet365', 'DraftKings', 'BetRivers']
    
    def get_live_odds(self, team1, team2, provider='all'):
        """Fetch live odds from different sportsbooks"""
        
        if provider == 'all':
            return self._get_consensus_odds(team1, team2)
        else:
            return self._get_provider_odds(team1, team2, provider)
    
    def _get_consensus_odds(self, team1, team2):
        """Average odds across all providers"""
        odds_list = []
        for provider in self.providers:
            odds = self._get_provider_odds(team1, team2, provider)
            odds_list.append(odds)
        
        # Average consensus
        return self._average_odds(odds_list)
```

### Pattern 3: Add Historical Analysis

```python
# src/models/team_analytics.py - New class

class HistoricalTrendAnalysis:
    def __init__(self, historical_df):
        self.df = historical_df
    
    def compute_improvement_trend(self, team, window=10):
        """Compute if team is improving or declining"""
        recent = self.df[self.df['home_team'] == team].tail(window)
        
        # Early performance
        early_accuracy = recent.head(5)['wins'].sum() / 5
        
        # Recent performance
        recent_accuracy = recent.tail(5)['wins'].sum() / 5
        
        # Trend
        trend = recent_accuracy - early_accuracy
        return 'Improving' if trend > 0 else 'Declining' if trend < 0 else 'Stable'
```

---

## 📊 Performance Profiling

### Identify Bottlenecks

```python
import cProfile
import pstats

def profile_prediction_generation():
    ensemble = EnsemblePredictor(df)
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    for i in range(100):
        ensemble.generate_prediction('Team1', 'Team2', {}, {})
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 slowest functions

if __name__ == "__main__":
    profile_prediction_generation()
```

### Optimization Example

```python
# Before: Slow (recalculates each time)
def generate_prediction(self, home_team, away_team, ...):
    team_stats = self._calculate_strengths()  # SLOW
    poisson_pred = self.poisson.predict_match(home_team, away_team)
    ...

# After: Fast (cache computed stats)
@lru_cache(maxsize=1000)
def _get_team_strength(self, team):
    return self.team_stats.get(team, {}).get('att_strength', 1.0)

def generate_prediction(self, home_team, away_team, ...):
    # Uses cached values
    poisson_pred = self.poisson.predict_match(home_team, away_team)
    ...
```

---

## 📝 Documentation Standards

### Docstring Format

```python
def compute_metric(param1: str, param2: List[int]) -> float:
    """
    One-line summary.
    
    Longer description if needed. Explain the "why"
    behind the implementation approach.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When input is invalid
        
    Example:
        >>> result = compute_metric('test', [1, 2, 3])
        >>> print(result)
        2.0
        
    References:
        https://example.com/paper.pdf
        
    See Also:
        related_function: For related computation
    """
```

---

## 🔐 Security Considerations

### Input Validation

```python
def generate_prediction(self, home_team: str, away_team: str, ...):
    """Validate all inputs"""
    
    # Validate team names
    if not isinstance(home_team, str) or len(home_team) == 0:
        raise ValueError("Invalid home_team")
    if home_team == away_team:
        raise ValueError("home_team and away_team must be different")
    
    # Validate feature ranges
    for features in [home_features, away_features]:
        if features.get('form', 0) < 0 or features.get('form') > 1:
            raise ValueError("form must be in [0, 1]")
    
    # Sanitize strings (prevent injection)
    home_team = home_team.strip().lower()
    away_team = away_team.strip().lower()
```

---

## 📋 Release Checklist

Before releasing new version:

- [ ] All tests passing (`pytest tests/ -v`)
- [ ] Code formatted with Black
- [ ] Linting passes (`flake8 src/`)
- [ ] Type checking passes (`mypy src/`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in setup.py
- [ ] Backward compatibility verified
- [ ] Performance benchmarked
- [ ] Security reviewed

---

## 🎓 Learning Resources

### Recommended Reading

1. **Sports Analytics**:
   - Dixon & Coles (1997) - Poisson models
   - Constantinou (2019) - Soccer prediction models

2. **Python Best Practices**:
   - PEP 8 - Style Guide
   - Clean Code - Robert Martin
   - Design Patterns - Gang of Four

3. **ML Engineering**:
   - XGBoost Documentation
   - Scikit-learn User Guide
   - mlflow for model tracking

---

**Version**: 1.0  
**Last Updated**: March 20, 2026  
**Maintainer**: Development Team
