# Model Configuration & Parameters

## Ensemble Weighting

```python
# Prediction weights in EnsemblePredictor
POISSON_WEIGHT = 0.60      # Statistical model contribution
ML_WEIGHT = 0.40           # Machine learning model contribution
MARKET_ODDS_WEIGHT = 0.10  # (Optional) Market calibration
```

## Feature Engineering Parameters

### Form Calculation
```python
FORM_WINDOW = 5            # Recent N matches for form
FORM_WEIGHT_FACTOR = linear  # More recent matches weighted higher
FORM_DEFAULT = 0.5         # Neutral form for new teams
```

**Calculation**: Points averaged over recent matches with exponential weighting

### Efficiency Metrics
```python
OFF_EFF = Goals / Expected_Goals
DEF_EFF = Goals_Conceded / Expected_Goals_Against

# Normalization
OFF_EFF_BASELINE = 1.0     # Perfect conversion = 1.0
DEF_EFF_BASELINE = 1.0     # Perfect defense = 1.0
```

### Expected Goals (xG)
```python
HOME_XG = max(0.1, home_att_strength * 1.1)  # 1.1 = home advantage
AWAY_XG = max(0.1, away_att_strength * 0.9)  # 0.9 = away disadvantage
```

## Team Strength Scoring

```python
STRENGTH_FORMULA = (
    WIN_RATE * 0.30 +
    NORMALIZED_GD * 0.25 +
    RECENT_FORM * 0.25 +
    OFFENSIVE_EFF * 0.10 +
    (1 - DEFENSIVE_EFF) * 0.10
)

# Weights Rationale:
# - Win Rate (30%):       Most direct measure of team quality
# - Goal Differential (25%): Long-term performance indicator
# - Recent Form (25%):    Momentum and current state
# - Offensive (10%):      Finishing quality
# - Defensive (10%):      Solidity at back (inverted)
```

## Poisson Model Parameters

```python
# Match outcome simulation
MAX_GOALS = 10             # Maximum goals modeled in matrix
HOME_ADVANTAGE = 1.1       # Home team xG multiplier
AWAY_DISADVANTAGE = 0.9    # Away team xG multiplier
MIN_XG = 0.1               # Minimum expected goals threshold
```

## Tournament Simulation Settings

```python
# Group stage
GROUPS_PER_TOURNAMENT = 12
TEAMS_PER_GROUP = 4
MATCHES_PER_TEAM = 3       # Round-robin

# Knockout rounds
ROUND_16_MATCHES = 8
QUARTERFINAL_MATCHES = 4
SEMIFINAL_MATCHES = 2
FINAL_MATCHES = 1

# Knockout rules
EXTRA_TIME_ENABLED = True
PENALTY_SHOOTOUT_PROBABILITY = 0.5  # If tied after extra time
```

## Historical Data Generation

```python
DEFAULT_DATASET_SIZE = 1000  # Number of synthetic matches
TRAINING_WINDOW = 1500       # Days of historical data (~4 years)
TEAMS_COUNT = 32            # Number of simulated teams

# Elo rating ranges
TEAM_ELO_MIN = 1450
TEAM_ELO_MAX = 2100
TEAM_ELO_MEAN = 1750
```

## Model Hyperparameters (ML Component)

```python
# GradientBoostingModel
FORM_DIFFERENTIAL_WEIGHT = 0.15
EFFICIENCY_DIFFERENTIAL_WEIGHT = 0.05
BASE_HOME_PROB = 0.35
BASE_AWAY_PROB = 0.35
MIN_PROBABILITY = 0.01

# Feature ranges
FORM_MIN = 0.0
FORM_MAX = 1.0
EFFICIENCY_MIN = 0.5
EFFICIENCY_MAX = 2.0
```

## Confidence Levels

```python
CONFIDENCE_HIGH = (probability_difference > 0.40)      # >40% difference
CONFIDENCE_MEDIUM_HIGH = (probability_difference > 0.20) # >20% difference
CONFIDENCE_MEDIUM = (probability_difference > 0.10)    # >10% difference
CONFIDENCE_LOW = (probability_difference <= 0.10)      # Toss-up
```

## API Client Settings

```python
# Market odds simulation
BASE_HOME_ODDS_PROBABILITY = 0.40
BASE_DRAW_ODDS_PROBABILITY = 0.25
BASE_AWAY_ODDS_PROBABILITY = 0.35
MARKET_VOLATILITY = 0.05  # ±5% random variation

# Weather conditions
WEATHER_CONDITIONS = ['Clear', 'Rain', 'Overcast', 'Humid']
TEMPERATURE_RANGE = (60, 85)  # Fahrenheit
ALTITUDE_RANGE = (10, 500)     # Meters
```

## Performance Targets

### Accuracy Metrics
```
Calibration: |predicted_prob - observed_freq| < 0.05
Brier Score: MSE(predictions, outcomes) < 0.20
ROC-AUC: > 0.70
Accuracy: > 65% for 3-way prediction (W/D/L)
```

### Speed Targets
```
Single prediction: < 100ms
Group stage sim (1 run): < 500ms
Full tournament sim: < 1000ms
Trophy odds (1000 runs): < 30 seconds
```

## Calibration & Adjustment

### Market Odds Integration
```python
if market_odds provided:
    # Blend model predictions with market-implied probabilities
    ensemble_prob = (model_prob * 0.90) + (market_prob * 0.10)
    # 90/10 split prevents over-reliance on markets
```

### Recalibration Schedule
```
Daily: Monitor actual vs predicted
Weekly: Adjust feature weights if drift detected
Monthly: Retrain if new data available
Quarterly: Full model validation and audit
```

## Edge Cases & Constraints

```python
# Minimum matches for valid statistics
MIN_MATCHES_FOR_ANALYSIS = 5
MIN_MATCHES_FOR_RANKING = 10

# Data validation
VALID_GOALS_RANGE = (0, 15)
VALID_POSSESSION_RANGE = (25, 75)
VALID_XG_RANGE = (0.1, 10.0)

# Team handling
TEAM_NAME_CASE_SENSITIVE = True
INVALID_TEAM_DEFAULT_FORM = 0.5
INVALID_TEAM_DEFAULT_EFFICIENCY = (1.0, 1.0)
```

## Dashboard Settings

```python
# Streamlit configuration
PAGE_WIDTH = "wide"
PLOT_HEIGHT_SMALL = 350
PLOT_HEIGHT_MEDIUM = 500
PLOT_HEIGHT_LARGE = 700

# Default selections
DEFAULT_HOME_TEAM_INDEX = 0
DEFAULT_AWAY_TEAM_INDEX = 1
DEFAULT_SIMULATIONS = 500
```

## Testing Parameters

```python
# Test dataset
TEST_SAMPLE_SIZE = 100
TEST_TEAM_COUNT = 6
TEST_DATE_RANGE = "2023-01-01 to 2023-12-31"

# Validation thresholds
PROBABILITY_TOLERANCE = 0.01
STRUCTURE_CHECK_REQUIRED = True
INTEGRATION_TEST_REQUIRED = True
```

## Logging & Monitoring

```python
LOG_LEVEL = "INFO"
LOG_FILE = "logs/prediction_engine.log"

# Metrics tracked
METRICS_TO_LOG = [
    'prediction_time',
    'model_confidence',
    'market_deviation',
    'tournament_sim_variance',
    'prediction_accuracy'
]
```

---

## Notes for Tuning

1. **Increasing Poisson Weight** (>0.60):
   - Better for stable, well-established teams
   - More conservative predictions
   - Less responsive to recent form

2. **Increasing ML Weight** (>0.40):
   - Better for volatile, changing team form
   - Captures tactical trends
   - More variable predictions

3. **Adding Market Odds** (enable if available):
   - Reduces systematic model bias
   - Incorporates real market information
   - Requires reliable odds source

4. **Adjusting Form Window**:
   - Smaller window (3): More reactive, higher variance
   - Larger window (7): More stable, slower adaptation

5. **Strength Score Weighting**:
   - For emphasizing defense: increase DEF_EFF weight
   - For emphasizing attack: increase OFF_EFF weight
   - For recent focus: increase RECENT_FORM weight

---

**Last Updated**: Development Build
**Version**: 1.0.0
