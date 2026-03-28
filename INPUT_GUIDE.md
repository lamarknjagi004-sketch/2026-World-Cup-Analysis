# 📝 Input Guide - 2026 World Cup Predictive Analysis

## Overview

This guide explains what inputs you need to provide for each feature of the dashboard.

---

## 🎯 Tab 1: Match Prediction

### Inputs Required:
1. **Home Team** (required)
   - Select from dropdown list of 32 teams
   - Examples: Argentina, France, Brazil, England, Spain, Germany, etc.
   
2. **Away Team** (required)
   - Select from dropdown list of 32 teams
   - Must be different from Home Team
   - System will show error if same team selected

### What Happens:
- Calculates recent form (5-game rolling average)
- Analyzes offensive and defensive efficiency
- Generates win/draw/loss probabilities
- Provides expected goals (xG) estimate
- Shows team comparisons

### Example:
```
Home Team: Argentina
Away Team: France
↓
Output: 
- Argentina Win: 45%
- Draw: 28%
- France Win: 27%
- Expected Score: 1-1
- Model Confidence: Medium-High
```

### Teams Available (32 total):
- Argentina, France, Brazil, England, Spain, Portugal
- Netherlands, Germany, Italy, Croatia, Uruguay, Morocco
- USA, Colombia, Mexico, Senegal, Japan, Switzerland
- Iran, South Korea, Australia, Ecuador, Serbia, Poland
- Saudi Arabia, Ghana, Wales, Costa Rica, Cameroon
- Canada, Tunisia, Qatar

---

## 📊 Tab 2: Team Rankings

### Inputs Required:
**No inputs needed** - Just click "Generate Rankings"

### What Happens:
- Analyzes all 32 teams
- Calculates strength score for each
- Ranks teams by overall quality
- Shows offensive/defensive efficiency metrics
- Creates interactive visualizations

### Output Data:
For each team you'll see:
- **Rank**: 1-32 (1 = strongest)
- **Team Name**
- **Strength Score**: 0-1 scale (higher = better)
- **Matches Played**: Total historical matches
- **Goals For**: Total goals scored
- **Goals Against**: Total goals conceded
- **Goal Difference**: GF - GA
- **Offensive Efficiency**: Goals/Expected Goals
- **Defensive Efficiency**: Goals Conceded/Expected Goals Against
- **Recent Form**: Last 5 games average (0-1 scale)

### Visualizations:
1. **Bar Chart**: Strength scores for all 32 teams
2. **Scatter Plot**: Offensive vs Defensive efficiency

### Example Output:
```
Rank 1: Argentina    | Strength: 0.82 | Off.Eff: 1.15 | Def.Eff: 0.85
Rank 2: France       | Strength: 0.80 | Off.Eff: 1.12 | Def.Eff: 0.88
Rank 3: Brazil       | Strength: 0.78 | Off.Eff: 1.10 | Def.Eff: 0.90
...
```

---

## 🏟️ Tab 3: Head-to-Head Analysis

### Inputs Required:
1. **Team 1** (required)
   - Select first team from dropdown
   - Example: Germany
   
2. **Team 2** (required)
   - Select second team from dropdown
   - Must be different from Team 1
   - Example: Spain

### What Happens:
- Compares two teams across multiple metrics
- Analyzes historical head-to-head record
- Shows form comparison
- Determines which team has advantage

### Output Data for Each Team:
- **Strength Score**: Overall team quality (0-1)
- **Offensive Efficiency**: How well team scores (>1.0 = above average)
- **Defensive Efficiency**: How well team defends (<1.0 = better defense)
- **Recent Form**: Last 5 games performance (0-1)
- **H2H Record**: Head-to-head wins/draws/games played
- **Advantage**: Which team is stronger

### Example:
```
Team 1: Germany
├─ Strength Score: 0.79
├─ Offensive Efficiency: 1.08
├─ Defensive Efficiency: 0.92
├─ Recent Form: 0.65
└─ H2H Record: 5W-2D (vs Spain)

Team 2: Spain
├─ Strength Score: 0.75
├─ Offensive Efficiency: 1.05
├─ Defensive Efficiency: 0.95
├─ Recent Form: 0.58
└─ H2H Record: 2W-2D (vs Germany)

>>> ADVANTAGE: Germany
```

---

## 🏆 Tab 4: Tournament Simulator

### Mode 1: Group Stage Simulation

**Inputs Required:**
- Click "Simulate Group Stage" button (no manual inputs)

**What Happens:**
- Simulates all group stage matches
- All 12 groups play round-robin
- Each team plays 3 matches
- Top 2 teams from each group advance

**Output:**
For each group (A-L):
```
Group A Standings:
Position | Team      | Points | GF | GA | GD
---------|-----------|--------|----|----|----
1        | Argentina | 9      | 8  | 2  | +6
2        | France    | 6      | 5  | 3  | +2
3        | Brazil    | 3      | 4  | 6  | -2
4        | England   | 0      | 2  | 8  | -6
```

---

### Mode 2: Full Tournament Simulation

**Inputs Required:**
- Click "Simulate Full Tournament" button

**What Happens:**
- Simulates group stage (all 12 groups)
- Simulates round of 16 (16→8 teams)
- Simulates quarterfinals (8→4 teams)
- Simulates semifinals (4→2 teams)
- Simulates final (2→1 champion)

**Output:**
```
Champion: 🏆 Argentina
Defeated in Final: France
```

---

### Mode 3: Trophy Winner Odds

**Inputs Required:**
1. **Number of Simulations** (slider)
   - Range: 100 to 1,000
   - Default: 500
   - Higher = more accurate but slower
   - Recommended: 500-1000 for best results

**What Happens:**
- Runs complete tournament simulation N times
- Calculates probability each team wins
- Shows top 10 contenders
- Generates visualization

**Output Example:**
```
Simulations Run: 500

Trophy Winner Odds (Top 10):
Rank | Team       | Probability | Odds
-----|------------|-------------|-------
1    | Argentina  | 18.5%      | 18.5%
2    | France     | 15.2%      | 15.2%
3    | Brazil     | 14.8%      | 14.8%
4    | England    | 12.3%      | 12.3%
5    | Germany    | 10.5%      | 10.5%
...
```

---

## 📈 Tab 5: Analytics

### Inputs Required:
1. **Select Team** (required)
   - Choose team from dropdown
   - Example: Argentina

### What Happens:
- Analyzes team's historical performance
- Detects seasonal patterns
- Shows monthly goal-scoring trends
- Displays goals conceded by month

### Output Data:

**Monthly Performance:**
```
Month    | Goals For | Goals Against | Performance
---------|-----------|---------------|----------
January  | 1.8       | 0.9           | Strong
February | 1.5       | 1.1           | Moderate
March    | 1.9       | 0.8           | Excellent
April    | 1.6       | 1.0           | Moderate
May      | 2.1       | 0.7           | Excellent
June     | 1.4       | 1.2           | Weak
...
```

**Visualization:**
- Line graph showing goals for (offensive trend)
- Line graph showing goals against (defensive trend)
- X-axis: Months (Jan-Dec)
- Y-axis: Goals per match

### Insights You Can Gain:
- When does the team perform best?
- When is the team weakest?
- Is there seasonal variation?
- How consistent is the team?

---

## 🎯 Input Validation

### What Happens if You Enter Invalid Data:

#### Same team for both fields (Match/H2H):
```
Error: "Please select different teams."
[System prevents submission]
```

#### Missing team selection:
```
All dropdowns are pre-populated with default teams
[System automatically selects first option]
```

#### Invalid simulation count:
```
Slider constrains input: 100-1000
[System prevents values outside range]
```

---

## 💡 Tips for Best Results

### For Match Predictions:
1. Choose teams with similar strength scores (more interesting)
2. Check "Recent Form" to understand current momentum
3. Higher confidence means more reliable prediction
4. Expected score shows most likely exact result

### For Rankings:
1. Look at top 10 teams for main contenders
2. Compare efficiency scores to understand team style
3. Watch goal difference to see historical dominance

### For Head-to-Head:
1. Use for direct tournament matchup analysis
2. Check H2H record for historical patterns
3. Compare efficiency to predict style clash

### For Tournament Simulation:
1. Run 500+ simulations for 500+ simulations for accurate odds
2. Run multiple times to see variance
3. Top 3 teams usually have 40%+ combined probability
4. Dark horses (low probability) are exciting possibilities

### For Analytics:
1. Check seasonal patterns before tournament
2. June matches are most important (month of tournament)
3. Look for trends before key months

---

## 📊 Understanding Output Metrics

### Strength Score (0-1 scale)
- **0.85+**: Elite team (top contenders)
- **0.75-0.85**: Strong team (likely qualification)
- **0.65-0.75**: Competitive team (possible qualification)
- **0.55-0.65**: Moderate team (might not qualify)
- **<0.55**: Weak team (unlikely to advance)

### Efficiency Metrics
- **Offensive Efficiency (>1.0)**: Scores more than expected (good finishing)
- **Offensive Efficiency (<1.0)**: Scores less than expected (poor finishing)
- **Defensive Efficiency (>1.0)**: Concedes more than expected (poor defense)
- **Defensive Efficiency (<1.0)**: Concedes less than expected (good defense)

### Form Score (0-1 scale)
- **0.7+**: Excellent form (winning streaks)
- **0.5-0.7**: Good form (mixed results)
- **0.4-0.5**: Struggling (losses building)
- **<0.4**: Poor form (losing streaks)

### Probabilities
- **>70%**: Very likely outcome
- **50-70%**: Favored outcome
- **30-50%**: Competitive match
- **<30%**: Underdog outcome

---

## 🔄 Workflow Example

**Complete Scenario:**

```
Step 1: Check Rankings
→ Open "Team Rankings" tab
→ Click "Generate Rankings"
→ Identify top 5 teams (Argentina, France, Brazil, England, Spain)

Step 2: Compare Top Teams
→ Go to "Head-to-Head" tab
→ Select Team 1: Argentina
→ Select Team 2: France
→ See Argentina has advantage (0.82 vs 0.80 strength)

Step 3: Predict Their Match
→ Go to "Match Prediction" tab
→ Select Argentina (Home) vs France (Away)
→ See: Argentina 45%, Draw 28%, France 27%
→ Expected Score: 1-1

Step 4: Analyze Seasonality
→ Go to "Analytics" tab
→ Select: Argentina
→ See: Strong in June (tournament month), weaker in winter

Step 5: Simulate Tournament
→ Go to "Tournament Simulator" tab
→ Select "Trophy Winner Odds"
→ Set to 500 simulations
→ See: Argentina 18.5%, France 15.2%, Brazil 14.8%
→ Argentina favored but not guaranteed
```

---

## 📋 Quick Reference - All 32 Teams

**Available Teams for Selection:**

Group A: Argentina, France, Brazil, England  
Group B: Spain, Portugal, Netherlands, Germany  
Group C: Italy, Croatia, Uruguay, Morocco  
Group D: USA, Colombia, Mexico, Senegal  
Group E: Japan, Switzerland, Iran, South Korea  
Group F: Australia, Ecuador, Serbia, Poland  
Group G: Saudi Arabia, Ghana, Wales, Costa Rica  
Group H: Cameroon, Canada, Tunisia, Qatar  

---

## ❓ FAQs About Inputs

**Q: Can I select the same team twice?**  
A: No, the system shows an error and prevents submission.

**Q: What if a team isn't in the dropdown?**  
A: All 32 teams are included. Check spelling of team name.

**Q: Can I customize the groups for tournament simulation?**  
A: Yes, edit `GROUPS_2026` in `src/dashboard/app.py` to change groups.

**Q: How many simulations should I run?**  
A: 
- 100-200: Quick estimate (less accurate)
- 500: Good balance (recommended)
- 1000: High accuracy (slower, 15-20 seconds)

**Q: Can I compare more than 2 teams at once?**  
A: Head-to-Head only compares 2 teams. Use Rankings to see all 32.

**Q: What happens if simulation finds a tie in final?**  
A: System uses penalty shootout (50-50 random winner).

---

## 🚀 Ready to Start?

1. Launch the dashboard: `python run_dashboard.py`
2. Open: `http://localhost:8501`
3. Start with "Team Rankings" tab (no inputs needed)
4. Try "Match Prediction" with any 2 teams
5. Run "Tournament Simulator" with 500 simulations
6. Explore all 5 tabs!

**Enjoy your 2026 World Cup analysis!** ⚽🏆
