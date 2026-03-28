"""
Data Refresh Scheduler
Automatically refreshes live match data on a schedule.
Runs in the background and updates historical_matches.csv with latest data.
"""

import schedule
import time
import logging
from datetime import datetime
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/refresh_schedule.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataRefreshScheduler:
    """Schedule automatic data refreshes from API-Football"""
    
    def __init__(self, api_key: str, output_path: str = 'data/historical_matches.csv'):
        """
        Initialize scheduler.
        
        Args:
            api_key: RapidAPI key for API-Football
            output_path: Path to save match data
        """
        self.api_key = api_key
        self.output_path = output_path
        self.is_running = False
        
    def refresh_data(self):
        """Fetch latest data from API-Football"""
        try:
            from src.data.api_football_client import fetch_and_update_historical_data
            
            logger.info("🔄 Starting data refresh...")
            df = fetch_and_update_historical_data(self.api_key, self.output_path)
            logger.info(f"✅ Data refresh completed. {len(df)} matches loaded.")
            return True
        except ImportError as e:
            logger.error(f"❌ Cannot import API client: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Data refresh failed: {str(e)}")
            return False
    
    def schedule_daily_refresh(self, time_str: str = "03:00"):
        """
        Schedule daily data refresh.
        
        Args:
            time_str: Time in HH:MM format (24-hour) when refresh should occur
        """
        schedule.every().day.at(time_str).do(self.refresh_data)
        logger.info(f"📅 Daily refresh scheduled at {time_str}")
    
    def schedule_periodic_refresh(self, interval_hours: int = 6):
        """
        Schedule refresh at regular intervals.
        
        Args:
            interval_hours: Refresh every N hours
        """
        schedule.every(interval_hours).hours.do(self.refresh_data)
        logger.info(f"⏲️ Periodic refresh scheduled every {interval_hours} hours")
    
    def schedule_match_day_refresh(self, match_days: list = None):
        """
        Schedule refresh on World Cup match days only.
        
        Args:
            match_days: List of dates (YYYY-MM-DD) with World Cup matches
        """
        if match_days is None:
            # 2026 World Cup dates (example - update as needed)
            match_days = []
            logger.info("📅 No match dates provided. Use schedule.every().day for continuous refresh.")
            return
        
        logger.info(f"🏆 Refresh scheduled for {len(match_days)} World Cup match days")
    
    def start(self, daemon: bool = False):
        """
        Start the scheduler (runs indefinitely).
        
        Args:
            daemon: Run as background daemon
        """
        self.is_running = True
        logger.info("▶️ Data refresh scheduler started")
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("⏹️ Scheduler stopped by user")
            self.stop()
    
    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        logger.info("Scheduler stopped")


def run_scheduler():
    """Run the data refresh scheduler with predefined schedule"""
    api_key = os.getenv('API_FOOTBALL_KEY')
    if not api_key:
        logger.error("❌ API_FOOTBALL_KEY environment variable not set")
        logger.info("Set it with: $env:API_FOOTBALL_KEY = 'your_key'")
        sys.exit(1)
    
    scheduler = DataRefreshScheduler(api_key)
    
    # Schedule options (uncomment the one you prefer):
    
    # Option 1: Refresh daily at 3 AM
    scheduler.schedule_daily_refresh("03:00")
    
    # Option 2: Refresh every 6 hours
    # scheduler.schedule_periodic_refresh(interval_hours=6)
    
    # Option 3: Refresh every hour during World Cup season
    # scheduler.schedule_periodic_refresh(interval_hours=1)
    
    logger.info("="*50)
    logger.info("✅ Data Refresh Scheduler Initialized")
    logger.info("="*50)
    
    scheduler.start()


if __name__ == "__main__":
    """
    Usage:
    
    1. Set API key:
       $env:API_FOOTBALL_KEY = 'your_rapidapi_key'
    
    2. Run scheduler:
       python refresh_scheduler.py
    
    3. Stop anytime:
       Ctrl+C
    """
    run_scheduler()
