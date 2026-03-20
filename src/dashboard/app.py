import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import sys
from datetime import datetime

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data.download_historical_data import generate_mock_historical_data
from src.features.build_features import FeatureEngineer
from src.models.ensemble import EnsemblePredictor
from src.models.team_analytics import TeamAnalytics
from src.models.tournament_simulator import TournamentSimulator
from src.data.api_client import LiveMatchAPI

TEAMS = [
    "Argentina", "France", "Brazil", "England", "Spain", "Portugal", "Netherlands", "Germany",
    "Italy", "Croatia", "Uruguay", "Morocco", "USA", "Colombia", "Mexico", "Senegal",
    "Japan", "Switzerland", "Iran", "South Korea", "Australia", "Ecuador", "Serbia", "Poland",
    "Saudi Arabia", "Ghana", "Wales", "Costa Rica", "Cameroon", "Canada", "Tunisia", "Qatar"
]

# 2026 World Cup Group Stage - 12 groups of 4 teams
GROUPS_2026 = {
    'A': ['Argentina', 'France', 'Brazil', 'England'],
    'B': ['Spain', 'Portugal', 'Netherlands', 'Germany'],
    'C': ['Italy', 'Croatia', 'Uruguay', 'Morocco'],
    'D': ['USA', 'Colombia', 'Mexico', 'Senegal'],
    'E': ['Japan', 'Switzerland', 'Iran', 'South Korea'],
    'F': ['Australia', 'Ecuador', 'Serbia', 'Poland'],
    'G': ['Saudi Arabia', 'Ghana', 'Wales', 'Costa Rica'],
    'H': ['Cameroon', 'Canada', 'Tunisia', 'Qatar'],
    'I': ['Argentina', 'Belgium', 'Canada', 'Morocco'],
    'J': ['France', 'Denmark', 'Peru', 'Australia'],
    'K': ['Spain', 'Germany', 'Costa Rica', 'Japan'],
    'L': ['Brazil', 'Switzerland', 'Serbia', 'Cameroon']
}

st.set_page_config(page_title="2026 FIFA World Cup Predictive Engine", layout="wide")

st.title("🏆 2026 FIFA World Cup Predictive Engine")
st.markdown("Advanced sports analytics and predictive modeling system using statistical and machine learning ensembles.")

@st.cache_data
def load_historical_data():
    file_path = "data/historical_matches.csv"
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        generate_mock_historical_data(1000, file_path)
    return pd.read_csv(file_path)

try:
    df = load_historical_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

@st.cache_data
def load_historical_data():
    file_path = "data/historical_matches.csv"
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        generate_mock_historical_data(1000, file_path)
    return pd.read_csv(file_path)

try:
    df = load_historical_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Initialize models
@st.cache_resource
def init_models():
    return {
        'feature_engineer': FeatureEngineer(df),
        'ensemble': EnsemblePredictor(df),
        'team_analytics': TeamAnalytics(df),
        'tournament_sim': TournamentSimulator(df, GROUPS_2026)
    }

models = init_models()

# Create tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Match Prediction", 
    "📊 Team Rankings", 
    "🏟️ Head-to-Head",
    "🏆 Tournament Simulator",
    "📈 Analytics"
])

# TAB 1: MATCH PREDICTION
with tab1:
    st.header("Match Prediction Engine")
    st.markdown("Predict the outcome of individual matches between two teams.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        home_team = st.selectbox("🏠 Home Team", sorted(TEAMS), index=0)
    
    with col2:
        away_team = st.selectbox("✈️ Away Team", sorted(TEAMS), index=1)
    
    if home_team == away_team:
        st.error("Please select different teams.")
    else:
        if st.button("Generate Prediction", type="primary", use_container_width=True):
            with st.spinner("Initializing models and calculating probabilities..."):
                fe = models['feature_engineer']
                ensemble = models['ensemble']
                
                # Features
                h_form = fe.get_team_recent_form(home_team, datetime.now().strftime("%Y-%m-%d"))
                a_form = fe.get_team_recent_form(away_team, datetime.now().strftime("%Y-%m-%d"))
                
                h_off_eff, h_def_eff = fe.get_efficiencies(home_team)
                a_off_eff, a_def_eff = fe.get_efficiencies(away_team)
                
                h_features = {'form': h_form, 'off_eff': h_off_eff, 'def_eff': h_def_eff}
                a_features = {'form': a_form, 'off_eff': a_off_eff, 'def_eff': a_def_eff}
                
                # Odds
                market_odds = LiveMatchAPI.get_prematch_odds(home_team, away_team)
                
                # Predict
                preds = ensemble.generate_prediction(home_team, away_team, h_features, a_features, market_odds)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f"📊 {home_team} vs {away_team}")
                    
                    labels = [f'{home_team} Win', 'Draw', f'{away_team} Win']
                    values = [preds['home_win_prob'], preds['draw_prob'], preds['away_win_prob']]
                    
                    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, 
                                                 marker_colors=['#4C78A8', '#9DB2BF', '#E45756'])])
                    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
                    st.plotly_chart(fig, use_container_width=True)
                    
                with col2:
                    st.subheader("🎯 Key Metrics & Explainability")
                    
                    st.metric(label="Expected Goals (xG)", value=f"{home_team}: {preds['home_xg']}  |  {away_team}: {preds['away_xg']}")
                    st.metric(label="Most Likely Score", value=preds['expected_score'])
                    st.metric(label="Model Confidence Level", value=preds['confidence_level'])
                    
                    st.markdown("### Explanatory Factors")
                    st.info(f"**{home_team} Form:** {h_form:.2f} | **{away_team} Form:** {a_form:.2f} *(Recent 5-game rolling performance)*")
                    st.info(f"**Market Alignment:** Adjusted via simulated dynamic betting lines.")
                
                st.divider()
                
                st.subheader("📈 Real-time Contextual Data Simulation")
                c1, c2, c3 = st.columns(3)
                weather = LiveMatchAPI.get_weather_conditions()
                c1.metric("Simulated Weather", weather['condition'])
                c2.metric("Temperature", f"{weather['temp_f']}°F")
                c3.metric("Stadium Altitude", f"{weather['altitude_m']}m")
                
                # Detailed comparison
                st.divider()
                st.subheader("📉 Team Comparison")
                comp_col1, comp_col2, comp_col3, comp_col4 = st.columns(4)
                
                with comp_col1:
                    st.metric(f"{home_team} Off. Eff", h_off_eff)
                with comp_col2:
                    st.metric(f"{home_team} Def. Eff", h_def_eff)
                with comp_col3:
                    st.metric(f"{away_team} Off. Eff", a_off_eff)
                with comp_col4:
                    st.metric(f"{away_team} Def. Eff", a_def_eff)

# TAB 2: TEAM RANKINGS
with tab2:
    st.header("Team Rankings & Strength Analysis")
    st.markdown("Comprehensive global rankings based on multiple statistical indicators.")
    
    if st.button("Generate Rankings", type="primary", use_container_width=True):
        with st.spinner("Calculating team strength scores..."):
            rankings_df = models['team_analytics'].generate_team_rankings(sorted(TEAMS))
            
            st.subheader("Global Rankings")
            st.dataframe(rankings_df, use_container_width=True, hide_index=True)
            
            # Visualizations
            st.subheader("Strength Score Distribution")
            fig = px.bar(rankings_df, x='Team', y='Strength Score', 
                         title="Team Strength Scores", 
                         color='Strength Score',
                         color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Offensive vs Defensive Efficiency")
            fig2 = px.scatter(rankings_df, x='Off Efficiency', y='Def Efficiency', 
                             size='Strength Score', hover_name='Team',
                             title="Offensive vs Defensive Efficiency",
                             labels={'Off Efficiency': 'Offensive Efficiency', 'Def Efficiency': 'Defensive Efficiency'})
            st.plotly_chart(fig2, use_container_width=True)

# TAB 3: HEAD-TO-HEAD
with tab3:
    st.header("Head-to-Head Analysis")
    st.markdown("Detailed comparison between two teams across multiple metrics.")
    
    h2h_col1, h2h_col2 = st.columns(2)
    
    with h2h_col1:
        team1 = st.selectbox("Team 1", sorted(TEAMS), key="h2h_team1")
    
    with h2h_col2:
        team2 = st.selectbox("Team 2", sorted(TEAMS), index=1, key="h2h_team2")
    
    if team1 == team2:
        st.error("Please select different teams.")
    else:
        if st.button("Analyze", type="primary", use_container_width=True, key="h2h_analyze"):
            with st.spinner("Comparing teams..."):
                comparison = models['team_analytics'].compare_teams(team1, team2)
                
                comp_col1, comp_col2 = st.columns(2)
                
                with comp_col1:
                    st.subheader(team1)
                    st.metric("Strength Score", comparison[team1]['strength_score'])
                    st.metric("Offensive Efficiency", comparison[team1]['offensive_efficiency'])
                    st.metric("Defensive Efficiency", comparison[team1]['defensive_efficiency'])
                    st.metric("Recent Form", comparison[team1]['recent_form'])
                    st.metric("H2H Record", f"{comparison[team1]['h2h_record']['wins']}W-{comparison[team1]['h2h_record']['draws']}D")
                
                with comp_col2:
                    st.subheader(team2)
                    st.metric("Strength Score", comparison[team2]['strength_score'])
                    st.metric("Offensive Efficiency", comparison[team2]['offensive_efficiency'])
                    st.metric("Defensive Efficiency", comparison[team2]['defensive_efficiency'])
                    st.metric("Recent Form", comparison[team2]['recent_form'])
                    st.metric("H2H Record", f"{comparison[team2]['h2h_record']['wins']}W-{comparison[team2]['h2h_record']['draws']}D")
                
                st.divider()
                st.info(f"**Advantage: {comparison['advantage']}**")

# TAB 4: TOURNAMENT SIMULATOR
with tab4:
    st.header("Tournament Simulator")
    st.markdown("Simulate the entire 2026 World Cup tournament and predict champions.")
    
    sim_mode = st.radio("Select Mode", ["Group Stage", "Full Tournament", "Trophy Winner Odds"])
    
    if sim_mode == "Group Stage":
        if st.button("Simulate Group Stage", type="primary", use_container_width=True):
            with st.spinner("Simulating group stage matches..."):
                simulator = models['tournament_sim']
                group_standings = simulator.simulate_group_stage(num_simulations=1)
                
                for group_name, standings in sorted(group_standings.items()):
                    st.subheader(f"Group {group_name}")
                    standings_data = []
                    for i, (team, stats) in enumerate(standings[:2], 1):  # Show top 2
                        standings_data.append({
                            'Position': i,
                            'Team': team,
                            'Points': stats.get('points', 0),
                            'GF': stats.get('gf', 0),
                            'GA': stats.get('ga', 0),
                            'GD': stats.get('gd', 0)
                        })
                    st.dataframe(pd.DataFrame(standings_data), use_container_width=True, hide_index=True)
    
    elif sim_mode == "Full Tournament":
        if st.button("Simulate Full Tournament", type="primary", use_container_width=True):
            with st.spinner("Simulating full tournament..."):
                simulator = models['tournament_sim']
                group_standings = simulator.simulate_group_stage(num_simulations=1)
                knockout_results = simulator.simulate_knockout_stage(group_standings)
                
                st.subheader("🏆 Final")
                final = knockout_results['Final'][0]
                st.success(f"🎉 Champion: **{final['winner']}**")
                st.info(f"Defeated: {final['home'] if final['winner'] == final['away'] else final['away']}")
    
    else:  # Trophy Winner Odds
        num_simulations = st.slider("Number of simulations", 100, 1000, 500, step=100)
        
        if st.button("Calculate Trophy Winner Odds", type="primary", use_container_width=True):
            with st.spinner(f"Running {num_simulations} tournament simulations..."):
                simulator = models['tournament_sim']
                trophy_probs = simulator.get_trophy_winners_probabilities(num_simulations=num_simulations)
                
                # Top 10 contenders
                top_10 = dict(list(trophy_probs.items())[:10])
                
                st.subheader("🏆 Trophy Winner Odds (Top 10)")
                odds_df = pd.DataFrame([
                    {'Team': team, 'Probability': prob, 'Odds': f"{prob*100:.1f}%"}
                    for team, prob in top_10.items()
                ])
                st.dataframe(odds_df, use_container_width=True, hide_index=True)
                
                fig = px.bar(odds_df, x='Team', y='Probability', 
                            title="World Cup Winner Probabilities",
                            labels={'Probability': 'Probability of Winning'},
                            color='Probability',
                            color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)

# TAB 5: ANALYTICS
with tab5:
    st.header("Advanced Analytics")
    st.markdown("Deep-dive statistical analysis and team performance metrics.")
    
    analytics_team = st.selectbox("Select Team for Analysis", sorted(TEAMS), key="analytics_team")
    
    if st.button("Analyze Team", type="primary", use_container_width=True):
        with st.spinner("Analyzing team statistics..."):
            team_analytics = models['team_analytics']
            seasonality = team_analytics.get_team_seasonality(analytics_team)
            
            if seasonality:
                st.subheader(f"{analytics_team} - Seasonal Performance")
                
                months = list(seasonality.keys())
                gf_values = [seasonality[m]['goals_for'] for m in months]
                ga_values = [seasonality[m]['goals_against'] for m in months]
                
                month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=[month_names[m-1] for m in months], y=gf_values,
                                        mode='lines+markers', name='Goals For',
                                        line=dict(color='#4C78A8')))
                fig.add_trace(go.Scatter(x=[month_names[m-1] for m in months], y=ga_values,
                                        mode='lines+markers', name='Goals Against',
                                        line=dict(color='#E45756')))
                fig.update_layout(title=f"{analytics_team} - Monthly Performance Trend",
                                 xaxis_title="Month", yaxis_title="Goals per Match")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"No seasonal data available for {analytics_team}")

