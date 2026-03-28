# Installation & Setup Guide

## 🚀 Prerequisites

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.9 - 3.13
- **RAM**: Minimum 4GB (8GB+ recommended)
- **Disk Space**: 500MB for project + dependencies
- **Internet**: Required for initial setup

---

## 📦 Installation Steps

### Step 1: Clone/Download Project

```bash
cd C:\Users\user\OneDrive\Desktop
# Project is located at:
# Predictive analysis/
```

### Step 2: Create Virtual Environment

#### Windows
```powershell
cd "Predictive analysis"
python -m venv .venv
.venv\Scripts\activate
```

#### macOS/Linux
```bash
cd "Predictive analysis"
python3 -m venv .venv
source .venv/bin/activate
```

**Expected Output:**
```
(.venv) PS C:\Users\user\OneDrive\Desktop\Predictive analysis>
```

### Step 3: Install Dependencies

```bash
# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected packages** (sample):
```
pandas            2.0+
numpy             1.24+
scipy             1.10+
scikit-learn      1.3+
xgboost           2.0+
streamlit         1.28+
plotly            5.17+
statsmodels       0.14+
```

### Step 4: Verify Installation

```bash
# Check Python version
python --version
# Expected: Python 3.9.x - 3.13.x

# Check installed packages
pip list | findstr streamlit
# Expected: streamlit   1.28.x

# Test imports
python -c "import pandas, numpy, scipy, streamlit, plotly; print('All imports successful!')"
```

---

## 🎮 Running the Dashboard

### Quick Start

```bash
# From project directory with venv activated
streamlit run src/dashboard/app.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8503
  Network URL: http://192.168.0.109:8503

  Ctrl+C to stop
```

### Access Dashboard

Open browser and navigate to: **http://localhost:8503**

### Dashboard Features

| Tab | Function |
|-----|----------|
| 🏠 **Home** | Match predictions for 2026 World Cup groups |
| 📊 **Analytics** | Team strength rankings and comparisons |
| 🏆 **Tournament** | Group stage and knockout simulations |
| ✅ **Validation** | Historical accuracy analysis (138+ matches) |

---

## 🧪 Running Validation

### Full Dataset Validation

```bash
# From project directory with venv activated
python validate_full_dataset.py
```

**Output:**
```
FULL DATASET VALIDATION - 138 predictions

2026-03-20 18:10:36,461 - INFO - Preparing validation dataset...
2026-03-20 18:10:36,562 - INFO - Prepared 137 matches for validation
2026-03-20 18:10:36,581 - INFO - Ensemble model initialized
2026-03-20 18:10:36,581 - INFO - Running model validation against dataset...
2026-03-20 18:10:36,606 - INFO - Validation complete

================================================================================
MODEL VALIDATION REPORT
================================================================================

OVERALL PERFORMANCE
────────────────────────────────────────────────────────────────────────────────
Total Matches Analyzed:        137
Betting Predictions Accuracy:  70.07%

BETTING PREDICTIONS PERFORMANCE
────────────────────────────────────────────────────────────────────────────────
    1 | Count:  37 | Accuracy:  72.97%
   1X | Count:  49 | Accuracy:  73.47%
   12 | Count:  30 | Accuracy:  83.33%
    2 | Count:  21 | Accuracy:  38.10%

Results: data\validation_report.json, data\validation_report.csv
```

### Output Files

```
data/
├── validation_report.json       # Detailed results (JSON format)
└── validation_report.csv        # Summary table (CSV format)
```

---

## 🔧 Configuration

### Python Path Setup

Project automatically adds src/ to path:

```python
# Already configured in main files:
sys.path.insert(0, str(Path(__file__).parent.parent))
# or
sys.path.append(os.path.abspath(...))
```

### Environment Variables (Optional)

```bash
# Windows
set STREAMLIT_SERVER_PORT=8503

# macOS/Linux
export STREAMLIT_SERVER_PORT=8503
```

### Streamlit Config File

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#0066ff"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8503
headless = true
```

---

## 🧹 Troubleshooting

### Issue: "Python was not found"

**Solution:**
```bash
# Use full path to Python
C:\Users\user\AppData\Local\Programs\Python\Python313\python.exe --version

# Or check Windows PATH
echo %PATH%
```

### Issue: "Module not found" errors

**Solution:**
```bash
# Verify venv is activated (.venv at start of terminal prompt)
# If not:
.venv\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: "Port 8503 already in use"

**Solution:**
```bash
# Use different port
streamlit run src/dashboard/app.py --server.port=8504

# Or kill existing process (Windows)
netstat -ano | findstr :8503
taskkill /PID <PID> /F
```

### Issue: Streamlit dashboard won't load

**Solution:**
```bash
# Clear Streamlit cache
rm -r ~/.streamlit/cache

# Restart with debug mode
streamlit run src/dashboard/app.py --logger.level=debug
```

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution:**
```bash
# Ensure you're in project root directory
cd "c:\Users\user\OneDrive\Desktop\Predictive analysis"

# Verify file structure
dir src  # Should list dashboard, data, features, models, validation
```

### Issue: Import errors in custom scripts

**Solution:**
```python
# Add to script top:
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # Go up 1 level
# or
sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # Go up 2 levels
```

---

## 📝 Project Structure Verification

After installation, verify directory structure:

```bash
# List project structure
tree /F  # Windows
tree    # macOS/Linux

# Expected:
# Predictive analysis/
# ├── .venv/                    # Virtual environment (created)
# ├── data/                     # Data directory (created during runs)
# ├── src/
# │   ├── dashboard/
# │   │   └── app.py
# │   ├── data/
# │   │   ├── api_client.py
# │   │   └── download_historical_data.py
# │   ├── features/
# │   │   └── build_features.py
# │   ├── models/
# │   │   ├── ensemble.py
# │   │   ├── poisson_model.py
# │   │   ├── ml_model.py
# │   │   ├── team_analytics.py
# │   │   └── tournament_simulator.py
# │   └── validation/
# │       └── model_validator.py
# ├── requirements.txt
# ├── validate_full_dataset.py
# ├── README.md
# ├── PROJECT_STRUCTURE.md
# ├── MODEL_DOCUMENTATION.md
# ├── FEATURES.md
# ├── INSTALLATION_AND_SETUP.md
# ├── API_DOCUMENTATION.md
# ├── VALIDATION_RESULTS.md
# └── DEVELOPMENT_GUIDE.md
```

---

## 🧑‍💻 Development Installation

For contributing to project:

### Additional Dev Dependencies

```bash
# pytest for testing
pip install pytest pytest-cov

# Code formatting
pip install black flake8

# Type checking
pip install mypy

# Documentation
pip install sphinx sphinx-rtd-theme
```

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Install with dev dependencies
pip install -r requirements-dev.txt

# 3. Run tests before committing
pytest tests/ -v

# 4. Format code
black src/

# 5. Check code quality
flake8 src/
mypy src/

# 6. Commit and push
git add .
git commit -m "Add feature description"
git push origin feature/your-feature
```

---

## 🌐 Deployment (Advanced)

### Docker Installation

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8503

CMD ["streamlit", "run", "src/dashboard/app.py"]
```

Build and run:
```bash
docker build -t predictive-engine .
docker run -p 8503:8503 predictive-engine
```

### Cloud Deployment (Heroku)

```bash
# Create Procfile
echo "web: streamlit run src/dashboard/app.py --server.port=\$PORT" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
heroku create predictive-engine-prod
git push heroku main
```

---

## 🔄 Update & Maintenance

### Update Packages

```bash
# Update all packages to latest versions
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade streamlit

# List outdated packages
pip list --outdated
```

### Backup & Recovery

```bash
# Backup validation results
cp data/validation_report.json data/validation_report_backup.json

# Export environment
pip freeze > requirements_frozen.txt

# Restore environment (if needed)
pip install -r requirements_frozen.txt
```

---

## ✅ Post-Installation Checklist

- [ ] Python 3.9+ installed and verified
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (pip list shows packages)
- [ ] Dashboard launches without errors (streamlit run...)
- [ ] Dashboard accessible at localhost:8503
- [ ] Validation script runs successfully
- [ ] Test data loads correctly
- [ ] All modules importable (test imports)

---

## 📞 Getting Help

### Common Resources

1. **Streamlit Documentation**: https://docs.streamlit.io
2. **Pandas Documentation**: https://pandas.pydata.org/docs
3. **XGBoost Documentation**: https://xgboost.readthedocs.io
4. **Project Documentation**: See README.md and other .md files

### Running Diagnostics

```bash
# Generate system info
python -c "import platform, sys; print(platform.platform()); print(f'Python {sys.version}')"

# Check all imports
python validate_full_dataset.py  # Will show import errors if any

# Streamlit diagnostics
streamlit --version
streamlit cache clear
```

---

**Version**: 1.0  
**Last Updated**: March 20, 2026
