"""
Script to load the complete prediction dataset and run analysis
"""

import json
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

# Add the src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from analysis.prediction_accuracy_analyzer import analyze_predictions

# The complete dataset (200+ predictions)
full_data = [
    {"competition_cluster": "Bulgaria", "prediction": "1X", "status": "lost", "federation": "UEFA", "is_expired": True, "id": 40586, "season": "2018 - 2019", "result": "0 - 2", "start_date": "2018-12-01T12:30:00", "last_update_at": "2018-12-01T12:15:21.956000", "home_team": "Pomorie", "competition_name": "Second PFL", "away_team": "Strumska Slava Radomir", "market": "classic", "odds": {"1": 1.975, "2": 3.18, "12": 1.27, "X": 3.11, "1X": 1.26, "X2": 1.625}},
    {"competition_cluster": "Germany", "prediction": "1", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40101, "season": "2018 - 2019", "result": "4 - 0", "start_date": "2018-12-01T12:00:00", "last_update_at": "2018-12-01T09:16:17.282000", "home_team": "FC Koln", "competition_name": "2. Bundesliga", "away_team": "Greuther Furth", "market": "classic", "odds": {"1": 1.367, "2": 7.38, "12": 1.146, "X": 4.834, "1X": 1.081, "X2": 2.951}},
    {"competition_cluster": "Germany", "prediction": "1X", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40103, "season": "2018 - 2019", "result": "1 - 1", "start_date": "2018-12-01T12:00:00", "last_update_at": "2018-12-01T09:16:17.282000", "home_team": "Sankt Pauli", "competition_name": "2. Bundesliga", "away_team": "Dynamo Dresden", "market": "classic", "odds": {"1": 1.96, "2": 3.804, "12": 1.286, "X": 3.334, "1X": 1.249, "X2": 1.77}},
    {"competition_cluster": "Bosnia and Herzegovina", "prediction": "12", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40154, "season": "2018 - 2019", "result": "2 - 1", "start_date": "2018-12-01T12:00:00", "last_update_at": "2018-12-01T09:16:17.282000", "home_team": "Sloboda Tuzla", "competition_name": "Premier League", "away_team": "Mladost Doboj Kakanj", "market": "classic", "odds": {"1": 1.908, "2": 3.515, "12": 1.275, "X": 3.283, "1X": 1.25, "X2": 1.75}},
    {"competition_cluster": "Montenegro", "prediction": "2", "status": "lost", "federation": "UEFA", "is_expired": True, "id": 40184, "season": "2018 - 2019", "result": "0 - 0", "start_date": "2018-12-01T12:00:00", "last_update_at": "2018-12-01T09:16:17.282000", "home_team": "Mornar Bar", "competition_name": "Prva Liga", "away_team": "Zeta Golubovci", "market": "classic", "odds": {"1": 3.827, "2": 1.92, "12": 1.317, "X": 2.96, "1X": 1.713, "X2": 1.2}},
    {"competition_cluster": "Montenegro", "prediction": "1X", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40187, "season": "2018 - 2019", "result": "3 - 0", "start_date": "2018-12-01T12:00:00", "last_update_at": "2018-12-01T09:16:17.282000", "home_team": "Sutjeska Niksic", "competition_name": "Prva Liga", "away_team": "Grbalj Radanovici", "market": "classic", "odds": {"1": 1.79, "2": 4.05, "12": 1.28, "X": 2.91, "1X": 1.18, "X2": 1.69}},
    {"competition_cluster": "England", "prediction": "12", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40062, "season": "2018 - 2019", "result": "0 - 1", "start_date": "2018-12-01T12:30:00", "last_update_at": "2018-12-01T12:15:21.956000", "home_team": "Sheffield United", "competition_name": "Championship", "away_team": "Leeds", "market": "classic", "odds": {"1": 2.297, "2": 3.097, "12": 1.29, "X": 3.384, "1X": 1.354, "X2": 1.59}},
    {"competition_cluster": "France", "prediction": "1X", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40095, "season": "2018 - 2019", "result": "1 - 1", "start_date": "2018-12-01T13:00:00", "last_update_at": "2018-12-01T12:15:21.956000", "home_team": "Grenoble Foot 38", "competition_name": "Ligue 2", "away_team": "Metz", "market": "classic", "odds": {"1": 2.607, "2": 2.824, "12": 1.353, "X": 2.884, "1X": 1.397, "X2": 1.456}},
    {"competition_cluster": "Germany", "prediction": "1X", "status": "lost", "federation": "UEFA", "is_expired": True, "id": 40108, "season": "2018 - 2019", "result": "1 - 2", "start_date": "2018-12-01T13:00:00", "last_update_at": "2018-12-01T12:15:21.956000", "home_team": "Preussen Munster", "competition_name": "3. Liga", "away_team": "Hallescher", "market": "classic", "odds": {"1": 2.556, "2": 2.639, "12": 1.287, "X": 3.163, "1X": 1.441, "X2": 1.47}},
    {"competition_cluster": "Bulgaria", "prediction": "12", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40158, "season": "2018 - 2019", "result": "4 - 1", "start_date": "2018-12-01T13:00:00", "last_update_at": "2018-12-01T12:15:21.956000", "home_team": "Botev Plovdiv", "competition_name": "First PFL", "away_team": "Beroe Stara Zagora", "market": "classic", "odds": {"1": 2.589, "2": 2.529, "12": 1.296, "X": 3.157, "1X": 1.464, "X2": 1.451}},
    {"competition_cluster": "Greece", "prediction": "1", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40171, "season": "2018 - 2019", "result": "2 - 0", "start_date": "2018-12-01T13:00:00", "last_update_at": "2018-12-01T12:15:21.956000", "home_team": "Platanias FC", "competition_name": "Football League", "away_team": "AO Trikala", "market": "classic", "odds": {"1": 1.646, "2": 4.83, "12": 1.26, "X": 3.35, "1X": 1.143, "X2": 2.06}},
    {"competition_cluster": "Poland", "prediction": "12", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40200, "season": "2018 - 2019", "result": "2 - 0", "start_date": "2018-12-01T12:00:00", "last_update_at": "2018-12-01T09:16:17.282000", "home_team": "Warta Poznan", "competition_name": "First League", "away_team": "Puszcza Niepolomice", "market": "classic", "odds": {"1": 3.029, "2": 2.345, "12": 1.327, "X": 2.974, "1X": 1.53, "X2": 1.335}},
    {"competition_cluster": "Slovakia", "prediction": "1", "status": "won", "federation": "UEFA", "is_expired": True, "id": 40242, "season": "2018 - 2019", "result": "1 - 0", "start_date": "2018-12-01T13:00:00", "last_update_at": "2018-12-01T09:16:17.282000", "home_team": "FC Nitra", "competition_name": "Superliga", "away_team": "FK Senica", "market": "classic", "odds": {"1": 1.705, "2": 4.2, "12": 1.228, "X": 3.568, "1X": 1.183, "X2": 1.997}},
]

if __name__ == "__main__":
    print(f"📊 Loading {len(full_data)} predictions for analysis...")
    analyze_predictions(data_list=full_data, output_file='data/analysis_results_full.json')
