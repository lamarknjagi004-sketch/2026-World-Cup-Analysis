# Quick Reference Guide

## 🚀 Getting Started (5 Minutes)

### 1. Install & Setup
```bash
# Navigate to project
cd "Predictive analysis"

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Option A: Use the launch script
python run_dashboard.py

# Option B: Direct Streamlit command
streamlit run src/dashboard/app.py
```

### 3. Access Dashboard
Open browser to: **http://localhost:8501**

---

## 📖 Using Each Feature

### 🎯 Match Prediction Tab
1. Select two teams from dropdowns
2. Click "Generate Prediction"
3. View:
   - Win/Draw/Loss probabilities (pie chart)
   - Expected goals (xG) for each team
   - Most likely score prediction
   - Model confidence level
   - Team form metrics

**Pro Tips:**
- Higher confidence = more reliable prediction
- xG shows underlying match quality
- Form score 0.5 = neutral, > 0.5 = good form

### 📊 Team Rankings Tab
1. Click "Generate Rankings"
2. View:
   - Global strength rankings (1-32)
   - Strength score details
   - Efficiency metrics comparison
   - Interactive scatter plot

**Interpretation:**
- Rank 1 = strongest team overall
- Strength Score: 0-1 scale (higher = better)
- Off Efficiency > 1.0 = above average finishing
- Def Efficiency < 1.0 = good defense

### 🏟️ Head-to-Head Tab
1. Select Team 1 and Team 2
2. Click "Analyze"
3. View side-by-side comparison:
   - Strength scores
   - Offensive/Defensive efficiency
   - Recent form (5 games)
   - Historical head-to-head record
   - Advantage indicator

### 🏆 Tournament Simulator Tab

**Mode 1: Group Stage**
- Simulate all group matches
- See which teams advance from each group
- View points, goals for/against for each team

**Mode 2: Full Tournament**
- Simulate groups + knockout stages
- See final champion
- Single deterministic outcome

**Mode 3: Trophy Winner Odds**
1. Set number of simulations (100-1000)
2. Run simulation
3. View:
   - Top 10 contenders
   - Win probability for each team
   - Interactive bar chart

**💡 More Simulations = More Accurate** (but slower)

### 📈 Analytics Tab
1. Select a team
2. Click "Analyze Team"
3. View seasonal performance:
   - Goals scored by month
   - Goals conceded by month
   - Performance trends

---

## 🔧 Advanced Configuration

### Change Tournament Groups
Edit `GROUPS_2026` in `src/dashboard/app.py`:
```python
GROUPS_2026 = {
    'A': ['Team1', 'Team2', 'Team3', 'Team4'],
    'B': ['Team5', 'Team6', 'Team7', 'Team8'],
    # ... etc
}
```

### Adjust Model Weights
Edit `src/models/ensemble.py`:
```python
# Change these lines:
ens_home = (poisson_preds['home_win'] * 0.60) + (ml_preds['home_win'] * 0.40)
# Try: 0.70 and 0.30 for more statistical focus
# Try: 0.50 and 0.50 for balanced approach
```

### Modify Feature Importance
In `src/models/team_analytics.py`, adjust weights in `calculate_team_strength()`:
```python
strength_score = (
    (win_rate * 0.30) +           # Current: 30% 
    (normalized_gd * 0.25) +      # Current: 25%
    (recent_form * 0.25) +        # Current: 25%
    (off_eff * 0.10) +            # Current: 10%
    (def_eff * 0.10)              # Current: 10%
)
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_models.py::TestPoissonModel -v
```

### Check Test Coverage
```bash
pytest tests/ --cov=src
```

---

## 📊 Key Metrics Explained

| Metric | Range | What It Means |
|--------|-------|---------------|
| Strength Score | 0-1 | Team quality (0.5 = average) |
| Form | 0-1 | Recent momentum (0.5 = neutral) |
| Off Efficiency | 0.5-2.0 | Finishing quality (1.0 = expected) |
| Def Efficiency | 0.5-2.0 | Defensive solidity (1.0 = expected) |
| xG | 0.1-5.0+ | Expected goals (quality of chances) |
| Win Probability | 0-1 | Chance team wins (as decimal) |
| Confidence | High/Med/Low | Model certainty level |

---

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Clear Streamlit cache
streamlit cache clear

# Verify installation
pip list | grep streamlit

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Missing data errors
```bash
# Delete old data
rm data/historical_matches.csv

# Run dashboard to regenerate
streamlit run src/dashboard/app.py
```

### Import errors
```bash
# Ensure you're in project root directory
# Verify PYTHONPATH if needed
python -c "from src.models.ensemble import EnsemblePredictor"
```

### Slow performance
- Reduce simulation count in Tournament Simulator
- Close other applications
- Check CPU/memory usage

---

## 📚 Understanding the Models

### Three-Layer Prediction System

```
┌─────────────────────────────────┐
│  Ensemble Predictor (Final)     │ ← Best predictions
├─────────────────────────────────┤
│  Poisson (60%)  │  ML Model (40%)│ ← Two parallel models
├─────────────────────────────────┤
│  Historical Data + Features      │ ← Raw inputs
└─────────────────────────────────┘
```

### Prediction Flow
1. **Feature Engineering**: Calculate form, efficiency, xG
2. **Poisson Model**: Statistical probability calculation
3. **ML Model**: Pattern recognition from features
4. **Ensemble**: Weighted combination (60% + 40%)
5. **Market Calibration**: Optional odds adjustment
6. **Final Output**: Win/Draw/Loss probabilities

---

## 💡 Pro Tips

1. **For Match Predictions**
   - Check team recent form before betting on confidence
   - xG difference shows true quality gap
   - High confidence matches are usually safer

2. **For Rankings**
   - Compare teams in same position to see balance
   - Goal differential (GD) shows historical performance
   - Efficiency metrics reveal tactical strength

3. **For Tournament Simulation**
   - Run 500+ simulations for reliable odds
   - Check multiple runs to see variance
   - Trophy odds show true probabilities

4. **For Analysis**
   - Seasonal patterns important for tournament timing
   - Recent form more predictive than career averages
   - Teams with similar strength scores = unpredictable

---

## 📞 Common Questions

**Q: Which prediction should I trust most?**
A: "High" confidence level predictions from the Match Prediction tab are most reliable. Match probability > 70% are usually decisive.

**Q: How accurate are the predictions?**
A: Model aims for 65-70% accuracy on 3-way predictions (W/D/L). Individual matches have inherent randomness.

**Q: Can I use this to bet?**
A: This is for scientific analysis and education. Probability-based betting has significant variance and risk.

**Q: How often should I update the data?**
A: Update monthly with real tournament data for best accuracy. System learns better with more real matches.

**Q: Why do predictions sometimes seem wrong?**
A: Football has inherent randomness. Probabilities ≠ certainties. Even 80% probability events fail 20% of the time.

---

## 🔗 File Locations Reference

```
Quick reference for finding code:
- Match prediction logic     → src/models/ensemble.py
- Team analytics            → src/models/team_analytics.py
- Tournament simulation     → src/models/tournament_simulator.py
- Feature engineering       → src/features/build_features.py
- Poisson model            → src/models/poisson_model.py
- Statistical model        → src/models/ml_model.py
- Dashboard interface      → src/dashboard/app.py
- Data generation          → src/data/download_historical_data.py
- Configuration            → CONFIG.md
- Tests                    → tests/test_models.py
```

---

## 🎬 Keyboard Shortcuts (Streamlit)

| Shortcut | Action |
|----------|--------|
| `R` | Rerun script |
| `C` | Clear cache |
| `S` | Show settings |
| `Q` | Quit |

---

**Need more help?** Check the full README.md for comprehensive documentation.

**Last Updated**: Build 1.0.0
