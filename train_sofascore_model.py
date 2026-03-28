"""
Train model with real Sofascore match data
Converts Chelsea match data to training format and trains ensemble
"""

import pandas as pd
import json
import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

# Add to path
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data.sofascore_client import SofascoreParser, save_sofascore_training_data
from src.features.build_features import FeatureEngineer
from src.models.ensemble import EnsemblePredictor

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_with_sofascore_data(sofascore_json_file: str = 'chelsea_data.json', 
                              output_csv: str = 'data/historical_matches.csv'):
    """
    Complete training pipeline with real Sofascore data.
    
    Args:
        sofascore_json_file: Path to saved Sofascore JSON response
        output_csv: Output path for training CSV
    """
    
    logger.info("="*60)
    logger.info("🚀 TRAINING WITH REAL SOFASCORE DATA")
    logger.info("="*60)
    
    # Load and parse Sofascore data
    logger.info(f"\n📥 Loading Sofascore data from {sofascore_json_file}...")
    
    try:
        df = SofascoreParser.load_from_json_file(sofascore_json_file)
        
        if len(df) == 0:
            logger.error("❌ No data loaded!")
            return False
        
        logger.info(f"✅ Loaded {len(df)} real matches")
        logger.info(f"\nData Summary:")
        logger.info(f"  Date range: {df['date'].min()} to {df['date'].max()}")
        logger.info(f"  Tournaments: {df['tournament'].unique().tolist()}")
        logger.info(f"  Teams: {len(df['home_team'].unique())} unique teams")
        
        # Save to CSV for reuse
        os.makedirs(os.path.dirname(output_csv) or '.', exist_ok=True)
        df.to_csv(output_csv, index=False)
        logger.info(f"✅ Saved training data to {output_csv}")
        
        # Initialize feature engineer
        logger.info("\n🔧 Building features...")
        feature_engineer = FeatureEngineer(df)
        
        # Test predictions on a few matches
        logger.info("\n🧪 Testing predictions on sample matches:")
        
        for idx in range(min(3, len(df))):
            match = df.iloc[idx]
            home_team = match['home_team']
            away_team = match['away_team']
            
            try:
                # Ensemble prediction
                ensemble = EnsemblePredictor(feature_engineer, df)
                probs = ensemble.predict_match(home_team, away_team)
                
                logger.info(f"\n  Match: {home_team} vs {away_team}")
                logger.info(f"    Actual: {match['home_goals']}-{match['away_goals']}")
                logger.info(f"    Predicted: Home {probs[0]:.1%} | Draw {probs[1]:.1%} | Away {probs[2]:.1%}")
            except Exception as e:
                logger.warning(f"    Error on prediction: {str(e)}")
        
        logger.info("\n" + "="*60)
        logger.info("✅ TRAINING COMPLETE")
        logger.info("="*60)
        logger.info(f"\n✓ {len(df)} real matches loaded and ready for predictions")
        logger.info(f"✓ Data saved to {output_csv}")
        logger.info(f"✓ Dashboard will use this data automatically")
        
        return True
        
    except FileNotFoundError:
        logger.error(f"❌ File not found: {sofascore_json_file}")
        logger.info("Run: python save_sofascore_data.py first to create the JSON file")
        return False
    except Exception as e:
        logger.error(f"❌ Training failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Default: Look for chealsea_data.json in current directory
    import argparse
    parser = argparse.ArgumentParser(description='Train model with Sofascore data')
    parser.add_argument('--file', default='chelsea_data.json', help='Path to Sofascore JSON file')
    parser.add_argument('--output', default='data/historical_matches.csv', help='Output CSV path')
    
    args = parser.parse_args()
    
    success = train_with_sofascore_data(args.file, args.output)
    sys.exit(0 if success else 1)
