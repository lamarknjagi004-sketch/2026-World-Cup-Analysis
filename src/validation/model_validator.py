"""
Model Validation Module
Validates the ensemble model against actual historical prediction data
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import sys
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.ensemble import EnsemblePredictor
from src.features.build_features import FeatureEngineer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelValidator:
    """Validates model predictions against actual match results"""
    
    def __init__(self, model_predictions_data: List[Dict]):
        """
        Initialize validator with prediction data
        
        Args:
            model_predictions_data: List of prediction dicts with actual results
        """
        self.raw_data = model_predictions_data
        self.df = None
        self.ensemble = None
        self.results = {}
        self._prepare_data()
        self._initialize_model()
    
    def _prepare_data(self):
        """Convert raw prediction data to DataFrame format"""
        logger.info("🔄 Preparing validation dataset...")
        
        processed_records = []
        for item in self.raw_data:
            # Skip postponed matches
            if item.get('status') == 'postponed':
                continue
            
            try:
                # Parse result
                result_parts = str(item.get('result', '0 - 0')).split(' - ')
                if len(result_parts) != 2:
                    continue
                
                home_goals = int(result_parts[0].strip())
                away_goals = int(result_parts[1].strip())
                
                # Create standardized record
                record = {
                    'date': pd.to_datetime(item.get('start_date')),
                    'home_team': item.get('home_team', 'Unknown'),
                    'away_team': item.get('away_team', 'Unknown'),
                    'home_goals': home_goals,
                    'away_goals': away_goals,
                    'home_xg': 0.0,  # Not available, estimate from goals
                    'away_xg': 0.0,
                    'home_possession': 50.0,  # Estimate
                    'away_possession': 50.0,
                    'tournament': item.get('competition_cluster', 'Unknown'),
                    'status': 'Ended',
                    'actual_result': item.get('result'),
                    'prediction_type': item.get('prediction'),  # 1, X, 2, 1X, 12, X2
                    'odds': item.get('odds', {}),
                    'actual_status': item.get('status'),  # won/lost (vs prediction)
                }
                processed_records.append(record)
            except Exception as e:
                logger.warning(f"⚠️ Skipped record: {e}")
                continue
        
        self.df = pd.DataFrame(processed_records)
        logger.info(f"✅ Prepared {len(self.df)} matches for validation")
    
    def _initialize_model(self):
        """Initialize the ensemble predictor"""
        try:
            # Try to load historical data for model initialization
            historical_path = Path(__file__).parent.parent.parent / 'data' / 'historical_matches.csv'
            if historical_path.exists():
                df = pd.read_csv(historical_path)
                self.ensemble = EnsemblePredictor(df)
                logger.info(f"✅ Ensemble model initialized with {len(df)} historical matches")
            else:
                logger.warning(f"⚠️ Historical data not found at {historical_path}")
                logger.warning("⚠️ Model predictions will be unavailable")
                self.ensemble = None
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize model: {e}")
            self.ensemble = None
    
    def get_model_prediction(self, row: pd.Series) -> Dict:
        """Get model prediction for a match"""
        if self.ensemble is None:
            return {
                'model_prediction': None,
                'model_probs': {},
                'model_confidence': 0,
                'model_prediction_type': None
            }
        
        try:
            # Prepare match data
            match_data = {
                'home_team': row['home_team'],
                'away_team': row['away_team'],
                'home_goals': row['home_goals'],
                'away_goals': row['away_goals'],
                'tournament': row['tournament'],
                'date': row['date'],
                'status': 'Ended'
            }
            
            # Get prediction
            prediction = self.ensemble.predict(match_data)
            
            return {
                'model_prediction': prediction.get('prediction'),
                'model_probs': prediction.get('probabilities', {}),
                'model_confidence': prediction.get('confidence', 0),
                'model_prediction_type': self._get_prediction_type(prediction.get('probabilities', {}))
            }
        except Exception as e:
            logger.debug(f"Prediction error: {e}")
            return {
                'model_prediction': None,
                'model_probs': {},
                'model_confidence': 0,
                'model_prediction_type': None
            }
    
    @staticmethod
    def _get_prediction_type(probs: Dict) -> Optional[str]:
        """Convert probabilities to prediction type (1, X, 2, 1X, 12, X2)"""
        p1 = probs.get('1', 0)
        px = probs.get('X', 0)
        p2 = probs.get('2', 0)
        
        if p1 < 0.01 and px < 0.01 and p2 < 0.01:
            return None
        
        # Determine best prediction type
        max_prob = max(p1, px, p2)
        
        if max_prob == p1:
            if p1 > px and p1 > p2:
                return '1'
            elif p1 >= px:
                return '1X'
            else:
                return '12'
        elif max_prob == px:
            if px > p1 and px > p2:
                return 'X'
            elif px >= p1:
                return '1X'
            else:
                return 'X2'
        else:  # p2
            if p2 > p1 and p2 > px:
                return '2'
            elif p2 >= px:
                return 'X2'
            else:
                return '12'
    
    def _actual_result_to_type(self, home_goals: int, away_goals: int) -> str:
        """Convert match result to result type (1, X, 2)"""
        if home_goals > away_goals:
            return '1'
        elif home_goals == away_goals:
            return 'X'
        else:
            return '2'
    
    def _prediction_matches_result(self, pred_type: str, result_type: str) -> bool:
        """Check if prediction type matches actual result"""
        if not pred_type or not result_type:
            return False
        
        if pred_type == '1':
            return result_type == '1'
        elif pred_type == 'X':
            return result_type == 'X'
        elif pred_type == '2':
            return result_type == '2'
        elif pred_type == '1X':
            return result_type in ['1', 'X']
        elif pred_type == '12':
            return result_type in ['1', '2']
        elif pred_type == 'X2':
            return result_type in ['X', '2']
        return False
    
    def validate(self) -> pd.DataFrame:
        """Run validation and return results"""
        logger.info("🧪 Running model validation against dataset...")
        
        results = []
        for idx, row in self.df.iterrows():
            # Get actual result
            actual_result_type = self._actual_result_to_type(
                row['home_goals'], 
                row['away_goals']
            )
            
            # Get model prediction
            model_pred = self.get_model_prediction(row)
            
            # Determine if matches
            model_correct = self._prediction_matches_result(
                model_pred['model_prediction_type'],
                actual_result_type
            ) if model_pred['model_prediction_type'] else False
            
            # Check against betting prediction
            betting_pred_type = row['prediction_type']
            betting_correct = self._prediction_matches_result(
                betting_pred_type,
                actual_result_type
            ) if betting_pred_type else False
            
            results.append({
                'date': row['date'],
                'match': f"{row['home_team']} vs {row['away_team']}",
                'result': f"{row['home_goals']}-{row['away_goals']}",
                'actual_type': actual_result_type,
                'betting_pred': betting_pred_type,
                'betting_correct': betting_correct,
                'model_pred': model_pred['model_prediction_type'],
                'model_confidence': model_pred['model_confidence'],
                'model_correct': model_correct,
                'tournament': row['tournament'],
                'odds': row['odds'].get(betting_pred_type, 0) if betting_pred_type else 0
            })
        
        self.validation_results = pd.DataFrame(results)
        logger.info(f"✅ Validation complete: {len(self.validation_results)} matches analyzed")
        
        return self.validation_results
    
    def generate_report(self) -> Dict:
        """Generate comprehensive validation report"""
        if self.validation_results is None or len(self.validation_results) == 0:
            logger.warning("⚠️ No validation results. Run validate() first.")
            return {}
        
        df = self.validation_results
        
        # Overall metrics
        model_accuracy = (df['model_correct'].sum() / len(df) * 100) if len(df) > 0 else 0
        betting_accuracy = (df['betting_correct'].sum() / len(df) * 100) if len(df) > 0 else 0
        
        # By prediction type
        model_by_type = {}
        betting_by_type = {}
        
        for pred_type in ['1', 'X', '2', '1X', '12', 'X2']:
            model_subset = df[df['model_pred'] == pred_type]
            if len(model_subset) > 0:
                model_by_type[pred_type] = {
                    'count': len(model_subset),
                    'accuracy': (model_subset['model_correct'].sum() / len(model_subset) * 100)
                }
            
            betting_subset = df[df['betting_pred'] == pred_type]
            if len(betting_subset) > 0:
                betting_by_type[pred_type] = {
                    'count': len(betting_subset),
                    'accuracy': (betting_subset['betting_correct'].sum() / len(betting_subset) * 100)
                }
        
        # Agreement metrics
        agreement = (df['model_pred'] == df['betting_pred']).sum() / len(df) * 100
        both_correct = ((df['model_correct']) & (df['betting_correct'])).sum()
        both_wrong = ((~df['model_correct']) & (~df['betting_correct'])).sum()
        
        return {
            'total_matches': len(df),
            'model_accuracy': round(model_accuracy, 2),
            'betting_accuracy': round(betting_accuracy, 2),
            'accuracy_delta': round(model_accuracy - betting_accuracy, 2),
            'model_by_type': model_by_type,
            'betting_by_type': betting_by_type,
            'agreement_rate': round(agreement, 2),
            'both_correct': both_correct,
            'both_wrong': both_wrong,
            'avg_model_confidence': round(df['model_confidence'].mean(), 2),
            'high_confidence_accuracy': round(
                df[df['model_confidence'] > 0.7]['model_correct'].mean() * 100, 2
            ) if len(df[df['model_confidence'] > 0.7]) > 0 else 0
        }
    
    def print_report(self):
        """Print formatted validation report"""
        report = self.generate_report()
        
        print("\n" + "="*80)
        print("🤖 MODEL VALIDATION REPORT")
        print("="*80)
        
        if not report:
            print("❌ No validation data available")
            return
        
        if self.ensemble is None:
            print("\n⚠️  MODEL NOT INITIALIZED")
            print("─"*80)
            print("The ensemble model could not be initialized.")
            print("Showing BETTING PREDICTION ANALYSIS only:\n")
        
        print(f"\n📊 OVERALL PERFORMANCE")
        print(f"{'─'*80}")
        print(f"Total Matches Analyzed:        {report['total_matches']}")
        
        if self.ensemble is not None:
            print(f"Model Accuracy:                {report['model_accuracy']:.2f}%")
            print(f"Betting Predictions Accuracy:  {report['betting_accuracy']:.2f}%")
            print(f"Model vs Betting Delta:        {report['accuracy_delta']:+.2f}%")
            print(f"Agreement on Predictions:      {report['agreement_rate']:.2f}%")
            print(f"Avg Model Confidence:          {report['avg_model_confidence']:.2f}")
            print(f"High Confidence Accuracy:      {report['high_confidence_accuracy']:.2f}%")
        else:
            print(f"Betting Predictions Accuracy:  {report['betting_accuracy']:.2f}%")
        
        if self.ensemble is not None:
            print(f"\n🎯 MODEL PERFORMANCE BY PREDICTION TYPE")
            print(f"{'─'*80}")
            for pred_type in ['1', 'X', '2', '1X', '12', 'X2']:
                if pred_type in report['model_by_type']:
                    stats = report['model_by_type'][pred_type]
                    print(f"  {pred_type:>3} | Count: {stats['count']:>3} | Accuracy: {stats['accuracy']:>6.2f}%")
        
        print(f"\n📈 BETTING PREDICTIONS PERFORMANCE")
        print(f"{'─'*80}")
        for pred_type in ['1', 'X', '2', '1X', '12', 'X2']:
            if pred_type in report['betting_by_type']:
                stats = report['betting_by_type'][pred_type]
                print(f"  {pred_type:>3} | Count: {stats['count']:>3} | Accuracy: {stats['accuracy']:>6.2f}%")
        
        if self.ensemble is not None:
            print(f"\n🔄 AGREEMENT ANALYSIS")
            print(f"{'─'*80}")
            print(f"Predictions Agree:             {report['agreement_rate']:.2f}%")
            print(f"Both Models Correct:           {report['both_correct']} matches")
            print(f"Both Models Wrong:             {report['both_wrong']} matches")
            
            print(f"\n💡 INSIGHTS")
            print(f"{'─'*80}")
            if report['accuracy_delta'] > 0:
                print(f"  ✓ Model outperforms betting by {abs(report['accuracy_delta']):.2f}%")
            else:
                print(f"  ✗ Betting predictions outperform model by {abs(report['accuracy_delta']):.2f}%")
            
            if report['high_confidence_accuracy'] > report['model_accuracy']:
                print(f"  ✓ High confidence predictions are more reliable")
        
        print("\n" + "="*80 + "\n")
    
    def save_results(self, output_file: str):
        """Save validation results to CSV and JSON"""
        if self.validation_results is not None:
            # Save CSV
            csv_file = output_file.replace('.json', '.csv')
            self.validation_results.to_csv(csv_file, index=False)
            logger.info(f"✅ Results saved to {csv_file}")
            
            # Save JSON report
            report = self.generate_report()
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"✅ Report saved to {output_file}")


def validate_model(prediction_data: List[Dict], output_dir: str = 'data'):
    """
    Main function to validate model
    
    Args:
        prediction_data: List of prediction dictionaries
        output_dir: Directory to save results
    """
    validator = ModelValidator(prediction_data)
    validator.validate()
    validator.print_report()
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    validator.save_results(str(output_dir / 'validation_report.json'))
    
    return validator


if __name__ == "__main__":
    print("Model Validator Module")
    print("Usage: validator = ModelValidator(prediction_data)")
    print("       validator.validate()")
    print("       validator.print_report()")
