# Feature Engineering Guide

## 🔧 Feature Engineering Overview

Features are the **input signals** that power predictive models. This document details all features used in the ensemble system.

---

## 📊 Feature Categories

### 1. Team-Level Features

#### 1.1 Form Score (Momentum)
```
Range: 0.0 - 1.0
Formula: 
  form = (recent_performance) / (max_possible_performance)
  
Example:
  Last 5 matches: W-W-D-W-L = 3.5 points/5 = 0.7 form score
```

**Calculation in `build_features.py`:**
```python
def compute_team_form(team, matches, lookback=5):
    recent_matches = matches[-lookback:]
    points = 0
    for match in recent_matches:
        if match['winner'] == team:
            points += 3
        elif match['result'] == 'draw':
            points += 1
    
    form_score = points / (lookback * 3)  # Normalize to 0-1
    return min(1.0, form_score)
```

**Interpretation:**
- 0.0 - Very poor form (winless streak)
- 0.3 - Below average (1 win per 5)
- 0.5 - Average (consistent draws and losses)
- 0.7 - Good form (3+ points per 5)
- 1.0 - Excellent form (winning every match)

**Why it matters:** Recent momentum is stronger predictor than season average

---

#### 1.2 Offensive Efficiency (Goals/Opportunities)
```
Range: 0.5 - 2.0
Formula:
  off_eff = (goals_scored_recent) / (average_shots_on_target)
```

**Calculation:**
```python
def compute_offensive_efficiency(team, matches, lookback=10):
    recent_matches = [m for m in matches if team in m][-lookback:]
    
    total_goals = sum(m['team_goals'] for m in recent_matches if m['team'] == team)
    total_shots_on_target = sum(m['shots_on_target'] for m in recent_matches if m['team'] == team)
    
    if total_shots_on_target == 0:
        return 1.0  # Default efficiency
    
    efficiency = total_goals / total_shots_on_target
    return efficiency
```

**Interpretation:**
- < 0.5: Clinical finishing (> 2 shots needed per goal) 
- 0.7 - 0.8: Efficient (1.25-1.4 shots per goal)
- 1.0: Average (1 shot = 1 goal on average)
- 1.5+: Wasteful (less than 1 goal per shot)

**Why it matters:** Two teams scoring same shots but different goals = different strengths

---

#### 1.3 Defensive Efficiency (Shots Allowed/Goals Conceded)
```
Range: 0.5 - 2.0
Formula:
  def_eff = (opponent_shots_on_target_allowed) / (goals_conceded_recent)
```

**Calculation:**
```python
def compute_defensive_efficiency(team, matches, lookback=10):
    recent_matches = [m for m in matches if team in m][-lookback:]
    
    total_shots_against = sum(m['opponent_shots'] for m in recent_matches if m['team'] == team)
    total_goals_conceded = sum(m['opponent_goals'] for m in recent_matches if m['team'] == team)
    
    if total_goals_conceded == 0:
        return 0.5  # Perfect defense edge case
    
    efficiency = total_shots_against / total_goals_conceded
    return efficiency
```

**Interpretation:**
- 0.5: Leaky defense (2 goals per shot allowed)
- 1.0: Average defense (1 goal per shot)
- 2.0: Solid defense (1 goal per 2 shots)
- 3.0+: Exceptional defense (rare)

**Why it matters:** Defense efficiency determines goal-to-opportunity conversion rate

---

#### 1.4 Home Advantage Factor
```
Range: 0.85 - 1.15
Formula:
  home_adv = (avg_points_at_home) / (avg_points_away)
```

**Calculation:**
```python
def compute_home_advantage(team, historical_matches):
    home_matches = [m for m in historical_matches if m['home_team'] == team]
    away_matches = [m for m in historical_matches if m['away_team'] == team]
    
    avg_home_points = sum([m['points_earned'] for m in home_matches]) / len(home_matches)
    avg_away_points = sum([m['points_earned'] for m in away_matches]) / len(away_matches)
    
    if avg_away_points == 0:
        return 1.0
    
    advantage = avg_home_points / avg_away_points
    return min(1.15, max(0.85, advantage))  # Clamp to realistic range
```

**Interpretation:**
- 0.85: Away team stronger at home (rare)
- 1.0: No home advantage
- 1.1: Strong home advantage (+2-4 points)
- 1.15: Very strong home advantage (rare)

**Why it matters:** Accounts for venue-specific factors (familiarity, travel fatigue, crowd support)

---

#### 1.5 Head-to-Head Statistics
```
Range: 0.0 - 1.0 (win rate)
Formula:
  h2h_advantage = (wins_in_direct_matches) / (total_direct_matches)
```

**Calculation:**
```python
def get_head_to_head(team1, team2, historical_matches, lookback=20):
    direct_matches = [m for m in historical_matches 
                     if (m['home_team'] == team1 and m['away_team'] == team2) or
                        (m['home_team'] == team2 and m['away_team'] == team1)][-lookback:]
    
    team1_wins = sum(1 for m in direct_matches if m['winner'] == team1)
    total = len(direct_matches)
    
    if total == 0:
        return 0.5  # No history, neutral
    
    return team1_wins / total
```

**Interpretation:**
- 0.0: Team always loses to opponent
- 0.33: Team loses 2 of 3 to opponent
- 0.50: Neutral head-to-head record
- 0.67: Team wins 2 of 3 to opponent
- 1.0: Team always beats opponent

**Why it matters:** Tactical familiarity and psychological factors affect relative performance

---

### 2. Match Context Features

#### 2.1 Tournament Tier
```
Categorical: 'World Cup' > 'Continental Cup' > 'League'
Weight: World Cup matches typically higher quality
```

#### 2.2 Time Since Last Match
```
Range: 1 - 200 days
Effect: 
  - < 3 days: Potential fatigue
  - 5-7 days: Optimal recovery
  - > 14 days: Potential rust
```

---

## 🔄 Feature Engineering Pipeline

### Stage 1: Data Collection
```
Raw Match Data
├── Historical results CSV
├── Team statistics database
├── Odds/lines data
└── Injury/suspension info
```

### Stage 2: Aggregation
```
Per-Team Computation
├── Form (last 5 matches)
├── Offensive efficiency (last 10)
├── Defensive efficiency (last 10)
├── Home advantage (season-long)
└── H2H record (recent matches)
```

### Stage 3: Normalization
```
Scale Features to [0, 1] or [-1, +1]
├── Min-max scaling for bounded features
├── Z-score normalization for unbounded
└── Ensuring no NaN values
```

### Stage 4: Feature Selection
```
Filter/Select for Model Input
├── Drop highly correlated features
├── Keep interpretable features
├── Validate against training data
└── Output feature vectors
```

---

## 💾 Feature Storage Format

### DataFrame Structure
```python
DataFrame columns: [
    'home_team': str,
    'away_team': str,
    'date': datetime,
    'home_form': float [0, 1],
    'away_form': float [0, 1],
    'home_off_eff': float [0, 2],
    'away_off_eff': float [0, 2],
    'home_def_eff': float [0.5, 3],
    'away_def_eff': float [0.5, 3],
    'home_advantage': float [0.85, 1.15],
    'h2h_advantage': float [0, 1],
    'home_goals': int,
    'away_goals': int,
    'result_type': str ('1', 'X', '2')
]
```

### Feature Vector for Models
```python
home_features = {
    'form': 0.7,
    'off_eff': 1.05,
    'def_eff': 1.80,
    'home_advantage': 1.10,
    'h2h': 0.60
}

away_features = {
    'form': 0.55,
    'off_eff': 0.95,
    'def_eff': 1.60,
    'home_advantage': 0.95,
    'h2h': 0.40
}
```

---

## 🎯 Feature Importance in Ensemble

| Feature | Poisson Weight | ML Weight | Ensemble Weight | Impact |
|---------|----------------|-----------|-----------------|--------|
| Form | 0% | 15% | 6% | Medium |
| Offensive Efficiency | 40% | 5% | 26% | High |
| Defensive Efficiency | 40% | 5% | 26% | High |
| Home Advantage | 20% | 0% | 12% | Medium |
| H2H | 0% | 5% | 2% | Low |

---

## 🔍 Feature Engineering Examples

### Example 1: England vs Scotland

#### Raw Data
```
England (Home):
  Last 5: W-D-L-W-W (2.6 pts/5)
  Shots on target (10 games): 45 goals in 35 shots
  Goals conceded (10 games): 8 in 32 shots against
  Home record: 6W-2D-2L = 20 pts in 10
  
Scotland (Away):
  Last 5: L-L-D-W-L (1.0 pts/5)
  Shots on target (10 games): 28 goals in 40 shots
  Goals conceded (10 games): 12 in 38 shots against
  Away record: 1W-3D-6L = 6 pts in 10
```

#### Feature Computation
```
England:
  form = 2.6 / 5 = 0.52 (average form)
  off_eff = 45 / 35 = 1.29 (wasteful)
  def_eff = 32 / 8 = 4.0 (excellent defense)
  home_adv = 20 / 6 = 3.33 → clamped to 1.15
  h2h (recent) = 1/1 = 1.0 (recent win)

Scotland:
  form = 1.0 / 5 = 0.20 (poor form)
  off_eff = 28 / 40 = 0.70 (very efficient)
  def_eff = 38 / 12 = 3.17 (strong defense)
  home_adv = 0.90 (away team)
  h2h (recent) = 0 (recent loss)
```

#### Model Input
```python
home_features = {
    'form': 0.52,
    'off_eff': 1.29,
    'def_eff': 4.0,
    'h2h': 1.0
}

away_features = {
    'form': 0.20,
    'off_eff': 0.70,
    'def_eff': 3.17,
    'h2h': 0.0
}
```

---

## ⚙️ Configuration Points

### Lookback Periods
```python
FORM_LOOKBACK = 5      # Last 5 matches for form
EFFICIENCY_LOOKBACK = 10  # Last 10 matches for offdef
H2H_LOOKBACK = 20      # Last 20 head-to-head
SEASON_LOOKBACK = None # Entire season for home_adv
```

### Clipping Ranges
```python
OFF_EFF_MIN, OFF_EFF_MAX = 0.5, 2.0
DEF_EFF_MIN, DEF_EFF_MAX = 0.5, 3.0
HOME_ADV_MIN, HOME_ADV_MAX = 0.85, 1.15
FORM_MIN, FORM_MAX = 0.0, 1.0
```

### Handling Missing Data
```python
Default for new team: 
  form = 0.5 (neutral)
  off_eff = 1.0 (average)
  def_eff = 1.0 (average)
  h2h = 0.5 (no history)
```

---

## 🧪 Feature Validation Checks

### Data Quality Checks
```python
assert all(0 <= form <= 1 for form in forms)
assert all(0.5 <= off_eff <= 2.0 for off_eff in off_effs)
assert all(0.5 <= def_eff <= 3.0 for def_eff in def_effs)
assert all(no NaN values)
assert feature_count == expected_count
```

### Sanity Checks
```python
# Form should be correlated with outcomes
correlation(form, win_rate) > 0.3

# Efficiency should track goal production
correlation(off_eff, goals_scored) > 0.5

# No individual feature dominates
max_feature_importance < 0.4
```

---

## 🚀 Advanced Feature Engineering

### Potential Future Features

#### Temporal Features
- Day of week effect (matches on weekends vs midweek)
- Seasonal patterns (form varies by competition stage)
- Travel distance (affects fatigue)

#### Network Features
- Team strength ranking (iterative rating)
- Strength of schedule (SOS ratio)
- League rank position

#### Advanced Metrics
- Expected goals (xG) from shot data
- Possession efficiency ratio
- Press success rate
- Pressing intensity metrics

#### Injury Adjustments
- Star player absence multiplier (-5% to xG)
- Squad depth factor
- Recent injury trends

---

## 📚 References

### Feature Engineering Best Practices
1. **Keep It Simple**: Interpretable > Complex
2. **Avoid Leakage**: Don't use future information
3. **Handle Missing Data**: Default sensibly or interpolate
4. **Scale Appropriately**: Match ranges for each feature
5. **Validate Importance**: Use correlation and feature importance

### Feature Engineering for Soccer
- Constantinou, A. C. (2019). "Towards smart-data utilisation for automated prediction of football match outcomes"
- Lucey, P., et al. (2014). "Quality vs Quantity: Improved Shot Prediction in Soccer using Strategic Features from Spatiotemporal Data"

---

**Version**: 1.0  
**Last Updated**: March 20, 2026
