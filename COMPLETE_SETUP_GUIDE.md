# 🚀 Complete Setup & Usage Guide

## Prerequisites

- **Python**: 3.8 or higher (you have 3.13.6 ✓)
- **Git**: For version control (already installed ✓)
- **Time**: ~10 minutes for initial setup

---

## Step 1: Navigate to Your Project

Open PowerShell and navigate to your project directory:

```powershell
cd "C:\Users\user\OneDrive\Desktop\Predictive analysis"
```

Verify you're in the right directory:
```powershell
ls
```

You should see: `src/`, `tests/`, `data/`, `requirements.txt`, `README.md`, etc.

---

## Step 2: Create a Virtual Environment (Optional but Recommended)

**Why?** Keeps your project dependencies isolated from system Python.

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\Activate.ps1

# You should see (venv) at the start of your terminal prompt
```

---

## Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web framework
- `pandas` - Data handling
- `plotly` - Visualizations
- `scikit-learn` - ML models
- `pytest` - Testing
- And more...

**Expected output**: "Successfully installed [packages]"

---

## Step 4: Launch the Dashboard

```powershell
python run_dashboard.py
```

**Or directly with Streamlit:**
```powershell
streamlit run src/dashboard/app.py
```

**What happens:**
- Dashboard launches automatically in your default browser
- URL: `http://localhost:8501`
- If it doesn't open, manually copy the URL into your browser

---

## 📖 Using the Dashboard

The dashboard has **5 main tabs**:

### 🎯 Tab 1: Match Prediction

**Purpose**: Predict the outcome of a single match

**How to use:**
1. Select "Home Team" (e.g., Argentina)
2. Select "Away Team" (e.g., France)
3. Click "Generate Prediction"

**You'll see:**
- ✅ Win/Draw/Loss probabilities (pie chart)
- ✅ Expected Goals (xG) for each team
- ✅ Most likely score prediction
- ✅ Model confidence level
- ✅ Team form metrics
- ✅ Weather simulation

**Example**: Argentina vs France
- Argentina: 45% win probability
- Draw: 20% probability
- France: 35% win probability
- Expected score: 2-1

---

### 📊 Tab 2: Team Rankings

**Purpose**: See all 32 teams ranked by strength

**How to use:**
1. Click "Generate Rankings"
2. View the ranking table

**You'll see:**
- ✅ Global rankings (1-32)
- ✅ Strength scores (0-1 scale)
- ✅ Goal statistics
- ✅ Offensive/Defensive efficiency
- ✅ Recent form scores
- ✅ Visualization charts

**Interpretation:**
- **Rank 1** = Strongest team
- **Strength Score 0.8+** = Top tier
- **Off Efficiency > 1.0** = Good finishing
- **Def Efficiency < 1.0** = Good defense

---

### 🏟️ Tab 3: Head-to-Head Analysis

**Purpose**: Compare two teams in detail

**How to use:**
1. Select Team 1 (e.g., Brazil)
2. Select Team 2 (e.g., Germany)
3. Click "Analyze"

**You'll see (side-by-side):**
- ✅ Strength scores
- ✅ Offensive efficiency
- ✅ Defensive efficiency  
- ✅ Recent form (last 5 games)
- ✅ Historical head-to-head records
- ✅ Which team has the advantage

**Example comparison:**
```
Brazil                          Germany
Strength: 0.78         vs       Strength: 0.72
Off Eff: 1.15          vs       Off Eff: 1.08
Def Eff: 0.92          vs       Def Eff: 0.95
Form: 0.75             vs       Form: 0.68

=> Advantage: Brazil
```

---

### 🏆 Tab 4: Tournament Simulator

**Purpose**: Simulate the entire 2026 World Cup

**Three modes:**

#### Mode A: Group Stage
- Simulates all group matches
- Shows which teams advance
- View points, goals, goal difference

**Steps:**
1. Click "Simulate Group Stage"
2. View results for each group (A-L)
3. See which 2 teams from each group advance

#### Mode B: Full Tournament
- Simulates groups + knockout stages
- Runs from group stage to final
- Shows final champion

**Steps:**
1. Click "Simulate Full Tournament"
2. See the champion crowned
3. View defeated finalist

#### Mode C: Trophy Winner Odds
- **Most accurate** - Runs multiple simulations
- Shows probability distribution
- Generates accurate odds

**Steps:**
1. Select number of simulations (100-1000)
2. Click "Calculate Trophy Winner Odds"
3. View top 10 contenders
4. See winning probability for each team

**Example output:**
```
Top 10 Trophy Winners:
1. Argentina: 18.5%
2. France: 16.2%
3. Brazil: 15.8%
4. Germany: 12.3%
... etc
```

---

### 📈 Tab 5: Analytics

**Purpose**: Deep-dive analysis of individual teams

**How to use:**
1. Select a team (e.g., Spain)
2. Click "Analyze Team"

**You'll see:**
- ✅ Monthly performance trends
- ✅ Goals scored by month
- ✅ Goals conceded by month
- ✅ Performance patterns
- ✅ Line chart visualization

**Use for:** Understanding team seasonality and patterns

---

## 💡 Practical Examples

### Example 1: Predict Match & Get Team Stats

```
1. Go to "Match Prediction" tab
2. Select: Argentina vs France
3. Click "Generate Prediction"
4. Switch to "Team Rankings" 
5. See both teams' global rankings
6. Switch to "Head-to-Head"
7. See detailed comparison
8. Switch to "Analytics"
9. Check Argentina's monthly form
```

### Example 2: Simulate Tournament

```
1. Go to "Tournament Simulator" tab
2. Select "Trophy Winner Odds"
3. Set simulations to 500
4. Click "Calculate Trophy Winner Odds"
5. See probability distribution
6. Note which teams are favorites
7. Try 1000 simulations for even better accuracy
```

### Example 3: Compare Teams

```
1. Go to "Team Rankings"
2. Generate rankings
3. Identify top 5 teams
4. Go to "Head-to-Head"
5. Compare rank 1 vs rank 2
6. See who's favored in matchup
7. Repeat with different teams
```

---

## 🔧 Running Tests

Verify everything works correctly:

```powershell
# Run all tests
pytest tests/test_models.py -v

# Run specific test
pytest tests/test_models.py::TestPoissonModel -v

# See test coverage
pytest tests/test_models.py --cov=src
```

**Expected**: All 22 tests should pass ✅

---

## 📁 Project Files Reference

```
src/
├── dashboard/
│   └── app.py              ← Main Streamlit app
├── models/
│   ├── ensemble.py         ← Prediction engine
│   ├── poisson_model.py    ← Statistical model
│   ├── ml_model.py         ← ML model
│   ├── team_analytics.py   ← Rankings & analytics
│   └── tournament_simulator.py ← Tournament sim
├── features/
│   └── build_features.py   ← Feature engineering
└── data/
    ├── api_client.py       ← Mock API
    └── download_historical_data.py ← Data generation

tests/
└── test_models.py          ← All tests (22 tests)

Configuration files:
- requirements.txt          ← Python dependencies
- README.md                 ← Full documentation
- CONFIG.md                 ← Model parameters
- run_dashboard.py          ← Launch script
```

---

## 🎯 Key Features to Try

### 1. **Most Likely Score**
- Shows the most probable final score
- Based on xG calculations
- Shows confidence level

### 2. **Efficiency Metrics**
- Off Eff > 1.0 = Finishing above expected
- Def Eff < 1.0 = Defending better than expected
- Compare teams to see tactical strength

### 3. **Recent Form**
- 0.5 = Neutral/average
- > 0.5 = Good form
- < 0.5 = Poor form
- Weighted by recency (recent games matter more)

### 4. **Confidence Level**
- High = One team heavily favored (>40% probability difference)
- Medium-High = Clear winner (>20% difference)
- Medium = Competitive match (>10% difference)
- Low = Toss-up match (~even odds)

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` |
| Dashboard won't load | Run `streamlit cache clear` then try again |
| Tests fail | Run from project root: `cd "Predictive analysis"` |
| Python not found | Use full path: See environment config |
| Slow dashboard | Close other apps, reduce simulation count |

---

## 🌐 Accessing Remotely

If you want to access from another computer:

```powershell
streamlit run src/dashboard/app.py --server.address 0.0.0.0
```

Then access from: `http://<your-computer-ip>:8501`

---

## 📊 Data Explanation

The system uses **1000 historical matches** of synthetic data:
- 32 teams with realistic Elo ratings
- Goals generated from Poisson distribution
- xG values based on team strength
- Possession based on Elo difference

**Located at**: `data/historical_matches.csv` (auto-generated on first run)

---

## 🔄 Making Changes

To modify the project:

1. **Change model weights**: Edit `src/models/ensemble.py`
   ```python
   # Change these values (add to 1.0 total):
   POISSON_WEIGHT = 0.60  # Statistical model
   ML_WEIGHT = 0.40       # Machine learning model
   ```

2. **Change team groups**: Edit `src/dashboard/app.py`
   ```python
   GROUPS_2026 = {
       'A': ['Team1', 'Team2', 'Team3', 'Team4'],
       # ... more groups
   }
   ```

3. **Add teams**: Edit in `app.py` TEAMS list

4. **Change predictions**: Modify `src/models/poisson_model.py` or `ml_model.py`

---

## 📚 Documentation Files

Read these for reference:
- **README.md** - Full project documentation
- **QUICKSTART.md** - Quick reference
- **CONFIG.md** - Model parameters
- **BUILD_SUMMARY.md** - What was built

---

## 🎉 Quick Start Checklist

- [ ] Navigate to project directory
- [ ] Create virtual environment (optional)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Launch dashboard: `python run_dashboard.py`
- [ ] Browser opens to `localhost:8501`
- [ ] Try each of 5 tabs
- [ ] Run tests: `pytest tests/test_models.py -v`
- [ ] All 22 tests pass ✅

---

## 💬 Need Help?

All documentation is in the project folder:
- `README.md` - Comprehensive guide
- `QUICKSTART.md` - Quick reference
- `CONFIG.md` - Configuration options
- Source code comments - Detailed explanations

Good luck! 🚀
