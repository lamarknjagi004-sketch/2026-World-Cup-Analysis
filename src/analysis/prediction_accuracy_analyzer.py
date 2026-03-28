"""
Prediction Accuracy Analysis Module
Analyzes historical prediction data to evaluate model performance
"""

import pandas as pd
import json
from typing import Dict, List, Tuple
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PredictionAccuracyAnalyzer:
    """Analyzes prediction accuracy and performance metrics"""
    
    def __init__(self, data_file: str = None, data_list: List[Dict] = None):
        """
        Initialize analyzer with data source
        
        Args:
            data_file: Path to JSON file with predictions
            data_list: List of prediction dictionaries
        """
        if data_file:
            with open(data_file, 'r') as f:
                data = json.load(f)
                self.data = data if isinstance(data, list) else data.get('data', [])
        elif data_list:
            self.data = data_list
        else:
            raise ValueError("Must provide either data_file or data_list")
        
        self.df = None
        self._prepare_dataframe()
    
    def _prepare_dataframe(self):
        """Prepare DataFrame from data"""
        self.df = pd.DataFrame(self.data)
        
        # Convert start_date to datetime
        self.df['start_date'] = pd.to_datetime(self.df['start_date'])
        
        # Extract result parts
        self.df[['home_result', 'away_result']] = self.df['result'].str.split(' - ', expand=True)
        self.df['home_result'] = pd.to_numeric(self.df['home_result'], errors='coerce')
        self.df['away_result'] = pd.to_numeric(self.df['away_result'], errors='coerce')
        
        logger.info(f"✅ Loaded {len(self.df)} predictions")
    
    def get_overall_stats(self) -> Dict:
        """Calculate overall statistics"""
        total = len(self.df)
        won = len(self.df[self.df['status'] == 'won'])
        lost = len(self.df[self.df['status'] == 'lost'])
        postponed = len(self.df[self.df['status'] == 'postponed'])
        
        win_rate = (won / (total - postponed)) * 100 if (total - postponed) > 0 else 0
        
        return {
            'total_predictions': total,
            'won': won,
            'lost': lost,
            'postponed': postponed,
            'valid_predictions': total - postponed,
            'win_rate': win_rate,
        }
    
    def get_stats_by_prediction_type(self) -> pd.DataFrame:
        """Break down stats by prediction type (1, X, 2, 1X, 12, X2)"""
        stats = []
        
        for pred_type in self.df['prediction'].unique():
            subset = self.df[self.df['prediction'] == pred_type]
            total = len(subset)
            won = len(subset[subset['status'] == 'won'])
            postponed = len(subset[subset['status'] == 'postponed'])
            valid = total - postponed
            
            win_rate = (won / valid * 100) if valid > 0 else 0
            
            stats.append({
                'Prediction Type': pred_type,
                'Total': total,
                'Won': won,
                'Lost': total - won - postponed,
                'Postponed': postponed,
                'Valid': valid,
                'Win Rate %': round(win_rate, 2)
            })
        
        return pd.DataFrame(stats).sort_values('Win Rate %', ascending=False)
    
    def get_stats_by_competition(self) -> pd.DataFrame:
        """Break down stats by competition cluster"""
        stats = []
        
        for comp in sorted(self.df['competition_cluster'].unique()):
            subset = self.df[self.df['competition_cluster'] == comp]
            total = len(subset)
            won = len(subset[subset['status'] == 'won'])
            postponed = len(subset[subset['status'] == 'postponed'])
            valid = total - postponed
            
            win_rate = (won / valid * 100) if valid > 0 else 0
            
            stats.append({
                'Competition': comp,
                'Total': total,
                'Won': won,
                'Lost': total - won - postponed,
                'Postponed': postponed,
                'Valid': valid,
                'Win Rate %': round(win_rate, 2)
            })
        
        return pd.DataFrame(stats).sort_values('Win Rate %', ascending=False)
    
    def get_roi_analysis(self) -> Dict:
        """Calculate ROI based on betting odds"""
        total_stake = 0
        total_return = 0
        
        for _, row in self.df.iterrows():
            if row['status'] == 'postponed':
                continue
            
            # Assume 1 unit stake per prediction
            stake = 1.0
            total_stake += stake
            
            # If won, add odds * stake; if lost, add 0
            if row['status'] == 'won':
                odds = row['odds'].get(row['prediction'], 1.0)
                if odds:
                    total_return += odds * stake
        
        roi = ((total_return - total_stake) / total_stake * 100) if total_stake > 0 else 0
        
        return {
            'total_stake': total_stake,
            'total_return': round(total_return, 2),
            'net_profit': round(total_return - total_stake, 2),
            'roi_percent': round(roi, 2)
        }
    
    def print_analysis(self):
        """Print comprehensive analysis report"""
        print("\n" + "="*80)
        print("🎯 PREDICTION ACCURACY ANALYSIS REPORT")
        print("="*80)
        
        # Overall Stats
        overall = self.get_overall_stats()
        print(f"\n📊 OVERALL STATISTICS")
        print(f"{'─'*80}")
        print(f"Total Predictions:        {overall['total_predictions']}")
        print(f"Valid (Non-postponed):    {overall['valid_predictions']}")
        print(f"Won:                      {overall['won']}")
        print(f"Lost:                     {overall['lost']}")
        print(f"Postponed:                {overall['postponed']}")
        print(f"\n✨ WIN RATE: {overall['win_rate']:.2f}%")
        
        # By Prediction Type
        print(f"\n📈 PERFORMANCE BY PREDICTION TYPE")
        print(f"{'─'*80}")
        pred_stats = self.get_stats_by_prediction_type()
        print(pred_stats.to_string(index=False))
        
        # By Competition
        print(f"\n🏆 PERFORMANCE BY COMPETITION")
        print(f"{'─'*80}")
        comp_stats = self.get_stats_by_competition()
        print(comp_stats.to_string(index=False))
        
        # ROI Analysis
        print(f"\n💰 ROI ANALYSIS (1 unit per prediction)")
        print(f"{'─'*80}")
        roi = self.get_roi_analysis()
        print(f"Total Stake:              {roi['total_stake']:.2f} units")
        print(f"Total Return:             {roi['total_return']:.2f} units")
        print(f"Net Profit/Loss:          {roi['net_profit']:+.2f} units")
        print(f"ROI:                      {roi['roi_percent']:+.2f}%")
        
        # Top and Bottom Performers
        print(f"\n⭐ TOP 5 COMPETITIONS BY WIN RATE")
        print(f"{'─'*80}")
        top_5 = comp_stats.head(5)
        for idx, row in top_5.iterrows():
            print(f"  {row['Competition']:<25} {row['Win Rate %']:>6.2f}% ({row['Won']}/{row['Valid']})")
        
        print(f"\n❌ BOTTOM 5 COMPETITIONS BY WIN RATE")
        print(f"{'─'*80}")
        bottom_5 = comp_stats.tail(5)
        for idx, row in bottom_5.iterrows():
            print(f"  {row['Competition']:<25} {row['Win Rate %']:>6.2f}% ({row['Won']}/{row['Valid']})")
        
        # Insights
        print(f"\n💡 KEY INSIGHTS")
        print(f"{'─'*80}")
        
        # Best prediction type
        best_pred = pred_stats.iloc[0]
        print(f"  ✓ Best prediction type: {best_pred['Prediction Type']} ({best_pred['Win Rate %']:.2f}%)")
        
        # Worst prediction type
        worst_pred = pred_stats.iloc[-1]
        print(f"  ✗ Worst prediction type: {worst_pred['Prediction Type']} ({worst_pred['Win Rate %']:.2f}%)")
        
        # Most profitable competition
        best_comp = comp_stats.iloc[0]
        print(f"  💰 Most reliable: {best_comp['Competition']} ({best_comp['Win Rate %']:.2f}%)")
        
        print("\n" + "="*80 + "\n")
    
    def save_analysis(self, output_file: str = 'prediction_analysis.json'):
        """Save analysis results to JSON"""
        analysis = {
            'overall': self.get_overall_stats(),
            'by_prediction_type': self.get_stats_by_prediction_type().to_dict('records'),
            'by_competition': self.get_stats_by_competition().to_dict('records'),
            'roi': self.get_roi_analysis()
        }
        
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        logger.info(f"✅ Analysis saved to {output_file}")


def analyze_predictions(data_file: str = None, data_list: List[Dict] = None, output_file: str = None):
    """
    Main function to analyze predictions
    
    Args:
        data_file: Path to JSON file
        data_list: List of prediction dictionaries
        output_file: Optional file to save results
    """
    analyzer = PredictionAccuracyAnalyzer(data_file=data_file, data_list=data_list)
    analyzer.print_analysis()
    
    if output_file:
        analyzer.save_analysis(output_file)
    
    return analyzer


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run from command line with JSON file
        data_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        analyze_predictions(data_file=data_file, output_file=output_file)
    else:
        print("Usage: python prediction_accuracy_analyzer.py <data_file.json> [output_file.json]")
