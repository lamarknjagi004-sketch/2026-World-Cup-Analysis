# Project Structure & Architecture

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      STREAMLIT DASHBOARD                     │
│         (Interactive UI for predictions & analytics)         │
└─────────────────────────────────────────────────────────────┘
                              ↓
            ┌─────────────────────────────────┐
            │   ENSEMBLE PREDICTION ENGINE    │
            │    (Calibration & Weighting)    │
            └─────────────────────────────────┘
                 ↓                    ↓
        ┌──────────────┐      ┌──────────────┐
        │ Poisson Model │      │  ML Model    │
        │ (60% weight)  │      │ (40% weight) │
        └──────────────┘      └──────────────┘
             ↓                     ↓
     ┌───────────────┐    ┌──────────────────┐
     │ Team Stats    │    │ Feature Engineer │
     │ Historical    │    │ Form, Efficiency │
     │ Goals Average │    │ Head-to-Head     │
     └───────────────┘    └──────────────────┘
             ↓                     ↓
     ┌────────────────────────────────────┐
     │  DATA LAYER (API + Historical)     │
     │  - Historical matches database     │
     │  - Live API integration            │
     │  - Odds synchronization            │
     └────────────────────────────────────┘
```

## 📂 Directory Structure

### Root Level
```
Predictive analysis/
├── README.md                          # Main documentation
├── PROJECT_STRUCTURE.md               # This file
├── MODEL_DOCUMENTATION.md             # Model specifications
├── FEATURES.md                        # Feature engineering
├── INSTALLATION_AND_SETUP.md          # Setup guide
├── API_DOCUMENTATION.md               # API reference
├── VALIDATION_RESULTS.md              # Validation analysis
├── DEVELOPMENT_GUIDE.md               # Contributing guide
├── requirements.txt                   # Dependencies
├── validate_full_dataset.py           # Validation script
└── .venv/                             # Virtual environment
```

### `/data` - Data Directory
```
data/
├── historical_matches.csv             # Training dataset (optional)
├── validation_report.json             # Validation results (generated)
├── validation_report.csv              # Validation export (generated)
└── [generated reports]                # Analysis outputs
```

### `/src` - Source Code

#### `/src/dashboard` - User Interface
```
src/dashboard/
└── app.py                             # Streamlit application
    ├── Page: Home (Match Predictions)
    ├── Page: Analytics (Team Rankings)
    ├── Page: Tournament Sim
    ├── Page: Validation Stats
    └── Utilities: Caching, Visualization
```

#### `/src/data` - Data Management
```
src/data/
├── api_client.py                      # Live match API
│   ├── LiveMatchAPI class
│   ├── fetch_live_matches()
│   ├── get_odds()
│   └── sync_market_data()
│
└── download_historical_data.py        # Historical data loading
    ├── generate_mock_historical_data()
    ├── load_csv()
    └── data_validation()
```

#### `/src/features` - Feature Engineering
```
src/features/
└── build_features.py                  # Feature computation
    ├── FeatureEngineer class
    ├── compute_team_form()
    ├── compute_offensive_efficiency()
    ├── compute_defensive_efficiency()
    ├── compute_home_advantage()
    └── get_head_to_head()
```

#### `/src/models` - Prediction Models
```
src/models/
├── ensemble.py                        # Main ensemble framework
│   ├── EnsemblePredictor class
│   ├── generate_prediction()
│   ├── _calculate_confidence()
│   └── market_calibration (optional)
│
├── poisson_model.py                   # Statistical model
│   ├── PoissonMatchModel class
│   ├── _calculate_strengths()
│   ├── predict_match()
│   └── goal_matrix calculation
│
├── ml_model.py                        # ML wrapper
│   ├── GradientBoostingModel class
│   ├── predict_probabilities()
│   └── feature-based scoring
│
├── team_analytics.py                  # Team strength analysis
│   ├── TeamAnalytics class
│   ├── compute_rankings()
│   ├── recent_form()
│   └── comparative_metrics()
│
└── tournament_simulator.py            # Tournament predictions
    ├── TournamentSimulator class
    ├── simulate_group_stage()
    ├── simulate_knockout()
    ├── monte_carlo_sampling()
    └── scenario_analysis()
```

#### `/src/validation` - Validation Framework
```
src/validation/
└── model_validator.py                 # Validation module
    ├── ModelValidator class
    ├── _prepare_data()
    ├── validate()
    ├── generate_report()
    ├── print_report()
    ├── save_results()
    └── validate_model() [main]
```

## 🔄 Data Flow

### Prediction Pipeline
```
1. MATCH INPUT
   ├─ home_team, away_team
   ├─ home_features, away_features
   └─ optional: market_odds

2. FEATURE RETRIEVAL
   ├─ Form score (recent performance)
   ├─ Offensive efficiency
   ├─ Defensive efficiency
   └─ Historical matchup data

3. MODEL PREDICTION
   ├─ Poisson: team_stats → goal_matrix → probabilities
   └─ ML: features → pattern_scoring → probabilities

4. ENSEMBLE COMBINATION
   ├─ Weight: 60% Poisson + 40% ML
   ├─ Market calibration: ±10% adjustment (optional)
   └─ Normalization: P1 + PX + P2 = 1.0

5. CONFIDENCE ASSESSMENT
   ├─ Calculate probability differential
   ├─ Assign confidence level
   └─ Output: High/Medium/Low/Toss-up

6. OUTPUT
   ├─ home_win_prob, draw_prob, away_win_prob
   ├─ confidence_level
   ├─ home_xg, away_xg (from Poisson)
   └─ expected_score (most likely outcome)
```

### Validation Pipeline
```
1. DATA PREPARATION
   ├─ Load 138+ historical predictions
   ├─ Skip postponed matches
   ├─ Parse results (home_goals, away_goals)
   └─ Create standardized records

2. MODEL INITIALIZATION
   ├─ Initialize ensemble with historical subset
   ├─ Train Poisson model
   ├─ Initialize ML model
   └─ Warn if insufficient training data

3. PREDICTION VALIDATION
   ├─ For each prediction:
   │  ├─ Generate model prediction
   │  ├─ Compare to actual result
   │  ├─ Check vs betting prediction
   │  └─ Record accuracy metrics
   └─ Aggregate statistics

4. REPORT GENERATION
   ├─ Overall performance metrics
   ├─ Accuracy by prediction type
   ├─ Model vs betting comparison
   ├─ Agreement analysis
   └─ Insights & recommendations

5. OUTPUT
   ├─ JSON report: validation_report.json
   ├─ CSV export: validation_report.csv
   └─ Console print: formatted report
```

## 🔌 Component Interactions

### Ensemble ↔ Poisson Model
```
Ensemble.generate_prediction()
    ↓
EnsemblePredictor
    ├─ poisson.predict_match(home, away)
    │  └─ Uses: team_stats, global_avg_goals
    └─ Returns: home_win, draw, away_win, home_xg, away_xg, expected_score
```

### Ensemble ↔ ML Model
```
Ensemble.generate_prediction()
    ↓
GradientBoostingModel
    ├─ predict_probabilities(home_features, away_features)
    │  └─ Uses: form_diff, off_eff_diff
    └─ Returns: home_win, draw, away_win
```

### Dashboard ↔ Ensemble
```
Streamlit App
    ├─ Tab: Home → generate_prediction() for each match
    ├─ Tab: Analytics → TeamAnalytics.compute_rankings()
    ├─ Tab: Tournament → TournamentSimulator.simulate_group_stage()
    └─ Tab: Validation → ModelValidator.validate()
```

## 📊 Data Structures

### Prediction Dictionary
```python
{
    'home_win_prob': 0.45,           # Probability home team wins
    'draw_prob': 0.28,               # Probability of draw
    'away_win_prob': 0.27,           # Probability away team wins
    'home_xg': 1.65,                 # Expected goals for home
    'away_xg': 1.40,                 # Expected goals for away
    'expected_score': '2 - 1',       # Most likely exact score
    'confidence_level': 'Medium-High' # Certainty assessment
}
```

### Validation Result Dictionary
```python
{
    'date': datetime,                # Match date
    'match': 'Team A vs Team B',     # Match string
    'result': '2-1',                 # Actual result
    'actual_type': '1',              # Actual outcome type
    'betting_pred': '1X',            # Betting prediction
    'betting_correct': True,         # Betting accuracy
    'model_pred': 'X',               # Model prediction
    'model_confidence': 0.25,        # Model confidence score
    'model_correct': False,          # Model accuracy
    'tournament': 'Group A',         # Competition
    'odds': 1.25                     # Betting odds for prediction
}
```

### Validation Report Dictionary
```python
{
    'total_matches': 137,
    'model_accuracy': 0.00,
    'betting_accuracy': 70.07,
    'accuracy_delta': -70.07,
    'agreement_rate': 0.00,
    'avg_model_confidence': 0.25,
    'high_confidence_accuracy': 0.00,
    'model_by_type': {
        '1': {'count': 0, 'accuracy': 0.00},
        'X': {'count': 0, 'accuracy': 0.00},
        ...
    },
    'betting_by_type': {
        '1': {'count': 37, 'accuracy': 72.97},
        '1X': {'count': 49, 'accuracy': 73.47},
        '12': {'count': 30, 'accuracy': 83.33},
        ...
    },
    'both_correct': 0,
    'both_wrong': 41
}
```

## 🔗 External Dependencies

### APIs
- **Live Match API**: Real-time odds and match data
- **Historical Data**: CSV-based historical matches

### Python Libraries
```
Data:           pandas, numpy
Statistics:     scipy (Poisson), statsmodels
ML:             scikit-learn, xgboost
UI:             streamlit, plotly
Scheduling:     schedule
Web:            requests
```

## 🎯 Prediction Types Supported

| Type | Meaning | Example | Accuracy |
|------|---------|---------|----------|
| **1** | Home Win | Argentina beats France | 72.97% |
| **X** | Draw | Both teams score equal | N/A |
| **2** | Away Win | France beats Argentina | 38.10% |
| **1X** | Home/Draw (Not Away) | Argentina wins or draws | 73.47% |
| **12** | Home or Away (Not Draw) | Argentina or France wins | **83.33%** |
| **X2** | Draw or Away | Draw or France wins | N/A |

## 🎓 Model Hierarchy

```
GeneralPredictionFramework (Interface)
    ├── EnsemblePredictor (Current Implementation)
    │   ├── 60% PoissonMatchModel (Statistical)
    │   ├── 40% GradientBoostingModel (ML)
    │   └── Market Calibration (Optional)
    │
    └── [Future Implementations]
        ├── BayesianHierarchicalModel
        ├── LSTMSeqToSeq
        └── TransformerAttentionModel
```

## 📈 Configuration Points

### Weights & Thresholds
| Setting | Location | Current Value | Purpose |
|---------|----------|---------------|---------|
| Poisson Weight | `ensemble.py` | 0.60 | Poisson model influence |
| ML Weight | `ensemble.py` | 0.40 | ML model influence |
| Market Adjustment | `ensemble.py` | 0.10 | Odds calibration factor |
| High Confidence | `ensemble.py` | > 0.40 | Probability differential threshold |
| Medium-High | `ensemble.py` | > 0.20 | Threshold |
| Medium | `ensemble.py` | > 0.10 | Threshold |
| Low Threshold | `ensemble.py` | ≤ 0.10 | Toss-up classification |

## 🔐 Data Consistency

### DataFrame Standards
All model operations expect DataFrames with:
- `home_team`: str (team name)
- `away_team`: str (team name)
- `home_goals`: int (goals scored)
- `away_goals`: int (goals conceded)
- `date`: datetime (match date)
- `home_xg`: float (expected goals)
- `away_xg`: float (expected goals)
- `tournament`: str (competition name)
- `status`: str ('Ended', 'In Progress', etc.)

### Feature Vector Standards
Features passed to models must include:
- `form`: float [0.0, 1.0] (recent performance)
- `off_eff`: float (offensive efficiency)
- `def_eff`: float (defensive efficiency)

### Probability Constraints
All probability outputs:
- Range: [0.0, 1.0]
- Sum: P1 + PX + P2 = 1.0 ± 0.001
- No negative values
- Minimum per outcome: 0.001

## 🧪 Testing Strategy

### Unit Testing
- Model initialization with edge cases
- Feature computation accuracy
- Probability normalization
- Confidence level assignment

### Integration Testing
- End-to-end prediction pipeline
- Ensemble weighting combination
- Validation against historical data
- Dashboard interactivity

### Regression Testing
- Consistent results on same inputs
- Historical accuracy benchmarks
- Edge case handling (empty data, null values)

---

**Version**: 1.0  
**Last Updated**: March 20, 2026
