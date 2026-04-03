import pandas as pd
import sys
sys.path.append('src')
from src.models.ensemble import EnsemblePredictor
from src.features.build_features import FeatureEngineer

print('Loading data...')
df = pd.read_csv('data/historical_matches.csv')
print(f'Loaded {len(df)} matches')

print('Initializing models...')
fe = FeatureEngineer(df)
predictor = EnsemblePredictor(fe, df)

print('Testing prediction...')
probs = predictor.predict_match('Argentina', 'Brazil')
print('Prediction for Argentina vs Brazil:')
print(f'Home win: {probs["home_win_prob"]}, Draw: {probs["draw_prob"]}, Away win: {probs["away_win_prob"]}')
print(f'Expected score: {probs["expected_score"]}')
print(f'Confidence: {probs["confidence_level"]}')

print('\nTesting with recent teams...')
probs2 = predictor.predict_match('Spain', 'Italy')
print('Prediction for Spain vs Italy:')
print(f'Home win: {probs2["home_win_prob"]}, Draw: {probs2["draw_prob"]}, Away win: {probs2["away_win_prob"]}')
print(f'Expected score: {probs2["expected_score"]}')
print(f'Confidence: {probs2["confidence_level"]}')