#!/usr/bin/env python
"""
Quick start script for 2026 World Cup Predictive Analysis Engine
Runs setup checks and launches the Streamlit dashboard
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import subprocess
from pathlib import Path

def check_environment():
    """Check if environment is properly set up."""
    print("🔍 Checking environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version OK")
    
    # Check required packages
    required_packages = ['streamlit', 'pandas', 'numpy', 'plotly', 'scipy', 'sklearn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print(f"   Install with: pip install {' '.join(missing_packages)}")
        return False
    print("✅ All packages installed")
    
    return True

def create_data_directory():
    """Ensure data directory exists."""
    print("\n📁 Checking directories...")
    
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir(exist_ok=True)
        print("✅ Data directory created")
    else:
        print("✅ Data directory exists")

def print_welcome():
    """Print welcome message."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║         🏆 2026 FIFA World Cup Predictive Engine 🏆            ║
║                                                                ║
║  Advanced Machine Learning & Statistical Sports Analytics     ║
╚════════════════════════════════════════════════════════════════╝
    """)

def print_instructions():
    """Print usage instructions."""
    print("""
📚 USAGE:

Your dashboard is accessible at: http://localhost:8501

Available views:
  🎯 Match Prediction    - Predict individual match outcomes
  📊 Team Rankings       - Global team strength rankings  
  🏟️  Head-to-Head       - Compare two teams in detail
  🏆 Tournament Sim      - Simulate groups, knockouts, or full tournament
  📈 Analytics           - Deep-dive team performance analysis

Quick Tips:
  • Start with "Match Prediction" to test the model
  • Check "Tournament Simulator" for full 2026 predictions
  • Use "Trophy Winner Odds" for championship probabilities
  • Run "pytest tests/" to validate all models

Ctrl+C to stop the server
    """)

def main():
    """Main entry point."""
    print_welcome()
    
    if not check_environment():
        print("\n❌ Environment check failed. Please install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    create_data_directory()
    
    print("\n🚀 Launching Streamlit dashboard...\n")
    print_instructions()
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "src/dashboard/app.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
