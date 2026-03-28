# API Documentation

## 📡 RESTful API Reference

Official API for programmatic access to the Predictive Analysis Engine.

---

## 🔑 Authentication

Currently, the system uses **no authentication** (development mode). For production, implement API key authentication:

```python
API_KEY = "your-secret-key-12345"
HEADERS = {'Authorization': f'Bearer {API_KEY}'}
```

---

## 🎯 Core Endpoints

### 1. Make Prediction

**Endpoint**: `/api/predict`  
**Method**: `POST`  
**Description**: Generate match outcome prediction

#### Request

```python
import requests
import json

url = "http://localhost:8000/api/predict"

payload = {
    "home_team": "Argentina",
    "away_team": "France",
    "home_features": {
        "form": 0.8,
        "off_eff": 1.2,
        "def_eff": 0.9
    },
    "away_features": {
        "form": 0.75,
        "off_eff": 1.15,
        "def_eff": 0.95
    },
    "market_odds": {
        "1": 1.85,
        "X": 3.50,
        "2": 4.20
    }
}

response = requests.post(url, json=payload)
```

#### Response (Success: 200)

```json
{
    "success": true,
    "prediction": {
        "home_win_prob": 0.45,
        "draw_prob": 0.28,
        "away_win_prob": 0.27,
        "confidence_level": "Medium-High",
        "home_xg": 1.65,
        "away_xg": 1.40,
        "expected_score": "2 - 1",
        "model_components": {
            "poisson": {
                "home_win": 0.42,
                "draw": 0.31,
                "away_win": 0.27
            },
            "ml": {
                "home_win": 0.48,
                "draw": 0.25,
                "away_win": 0.27
            }
        }
    },
    "timestamp": "2026-03-20T18:10:36.461Z"
}
```

#### Response (Error: 400)

```json
{
    "success": false,
    "error": "Invalid request",
    "details": "Missing required field: away_team",
    "status_code": 400
}
```

#### Python Usage Example

```python
from src.models.ensemble import EnsemblePredictor
from src.features.build_features import FeatureEngineer

# Initialize ensemble
ensemble = EnsemblePredictor(historical_df)

# Generate prediction
prediction = ensemble.generate_prediction(
    home_team='Argentina',
    away_team='France',
    home_features={'form': 0.8, 'off_eff': 1.2, 'def_eff': 0.9},
    away_features={'form': 0.75, 'off_eff': 1.15, 'def_eff': 0.95},
    market_odds={'1': 1.85, 'X': 3.50, '2': 4.20}
)

print(prediction)
# Output:
# {
#     'home_win_prob': 0.45,
#     'draw_prob': 0.28,
#     'away_win_prob': 0.27,
#     'confidence_level': 'Medium-High',
#     'home_xg': 1.65,
#     'away_xg': 1.40,
#     'expected_score': '2 - 1'
# }
```

---

### 2. Batch Predictions

**Endpoint**: `/api/predict/batch`  
**Method**: `POST`  
**Description**: Generate predictions for multiple matches

#### Request

```python
url = "http://localhost:8000/api/predict/batch"

payload = {
    "matches": [
        {
            "home_team": "Argentina",
            "away_team": "France",
            "home_features": {"form": 0.8, "off_eff": 1.2, "def_eff": 0.9},
            "away_features": {"form": 0.75, "off_eff": 1.15, "def_eff": 0.95}
        },
        {
            "home_team": "Brazil",
            "away_team": "Germany",
            "home_features": {"form": 0.85, "off_eff": 1.25, "def_eff": 0.85},
            "away_features": {"form": 0.70, "off_eff": 1.10, "def_eff": 1.0}
        }
    ]
}

response = requests.post(url, json=payload)
```

#### Response (200)

```json
{
    "success": true,
    "predictions": [
        {
            "match": "Argentina vs France",
            "home_win_prob": 0.45,
            "draw_prob": 0.28,
            "away_win_prob": 0.27,
            "confidence": "Medium-High"
        },
        {
            "match": "Brazil vs Germany",
            "home_win_prob": 0.52,
            "draw_prob": 0.25,
            "away_win_prob": 0.23,
            "confidence": "Medium-High"
        }
    ],
    "total_processed": 2,
    "timestamp": "2026-03-20T18:10:36.461Z"
}
```

---

### 3. Team Statistics

**Endpoint**: `/api/teams/{team_name}`  
**Method**: `GET`  
**Description**: Retrieve team statistics and rankings

#### Request

```bash
curl http://localhost:8000/api/teams/Argentina
```

#### Response (200)

```json
{
    "team_name": "Argentina",
    "rank": 1,
    "stats": {
        "form": 0.8,
        "offensive_efficiency": 1.2,
        "defensive_efficiency": 0.9,
        "home_advantage": 1.12,
        "goals_for_avg": 1.85,
        "goals_against_avg": 0.95,
        "win_rate": 0.75,
        "draw_rate": 0.15,
        "loss_rate": 0.10
    },
    "recent_matches": [
        {
            "date": "2026-03-15",
            "opponent": "Colombia",
            "result": "3-1",
            "outcome": "win"
        }
    ]
}
```

---

### 4. historical Validation Results

**Endpoint**: `/api/validation`  
**Method**: `GET`  
**Description**: Retrieve historical validation metrics

#### Request

```bash
curl http://localhost:8000/api/validation
```

#### Response (200)

```json
{
    "validation_date": "2026-03-20",
    "total_matches": 137,
    "overall_metrics": {
        "betting_accuracy": 0.7007,
        "model_accuracy": 0.0,
        "agreement_rate": 0.0
    },
    "by_prediction_type": {
        "1": {
            "count": 37,
            "accuracy": 0.7297
        },
        "1X": {
            "count": 49,
            "accuracy": 0.7347
        },
        "12": {
            "count": 30,
            "accuracy": 0.8333
        },
        "2": {
            "count": 21,
            "accuracy": 0.3810
        }
    },
    "confidence_breakdown": {
        "high": {"count": 0, "accuracy": 0.0},
        "medium_high": {"count": 0, "accuracy": 0.0},
        "medium": {"count": 0, "accuracy": 0.0},
        "low": {"count": 137, "accuracy": 0.0}
    }
}
```

---

### 5. Tournament Simulation

**Endpoint**: `/api/simulate/tournament`  
**Method**: `POST`  
**Description**: Simulate tournament outcomes

#### Request

```python
url = "http://localhost:8000/api/simulate/tournament"

payload = {
    "tournament_type": "world_cup_2026",
    "simulation_count": 1000,
    "groups": {
        "A": ["Argentina", "France", "Brazil", "England"],
        "B": ["Spain", "Portugal", "Netherlands", "Germany"]
    }
}

response = requests.post(url, json=payload)
```

#### Response (200)

```json
{
    "tournament": "world_cup_2026",
    "simulations_run": 1000,
    "group_stage_results": {
        "A": {
            "qualified_pct": {
                "Argentina": 92.5,
                "France": 85.3,
                "Brazil": 78.2,
                "England": 34.1
            }
        },
        "B": {
            "qualified_pct": {
                "Spain": 88.7,
                "Germany": 81.2,
                "Portugal": 45.3,
                "Netherlands": 32.2
            }
        }
    },
    "top_contenders": [
        {
            "rank": 1,
            "team": "Argentina",
            "championship_probability": 0.18
        }
    ]
}
```

---

## 📊 Data Types & Formats

### Feature Vector

```python
features = {
    "form": float,              # [0.0, 1.0] - Recent performance
    "off_eff": float,           # [0.5, 2.0] - Offensive efficiency
    "def_eff": float,           # [0.5, 3.0] - Defensive efficiency
    "home_advantage": float,    # [0.85, 1.15] - Home field advantage
    "h2h": float                # [0.0, 1.0] - Head-to-head win rate
}
```

### Prediction Response

```python
prediction = {
    "home_win_prob": float,         # [0.0, 1.0]
    "draw_prob": float,             # [0.0, 1.0]
    "away_win_prob": float,         # [0.0, 1.0]
    "confidence_level": str,        # "High", "Medium-High", "Medium", "Low (Toss-up)"
    "home_xg": float,               # Expected goals home
    "away_xg": float,               # Expected goals away
    "expected_score": str           # e.g., "2 - 1"
}
```

### Error Response

```python
error = {
    "success": boolean,
    "error": str,                   # Error type
    "details": str,                 # Detailed message
    "status_code": int              # HTTP status code
}
```

---

## 🔄 Query Parameters

### Prediction Endpoint

```
GET /api/predict?team1=Argentina&team2=France&include_model_breakdown=true&confidence_threshold=0.3
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `team1` | str | - | Home team name (required) |
| `team2` | str | - | Away team name (required) |
| `include_model_breakdown` | bool | false | Include Poisson & ML components |
| `confidence_threshold` | float | 0.0 | Minimum confidence (0-1) |
| `market_odds` | bool | false | Include market calibration |

### Validation Endpoint

```
GET /api/validation?start_date=2026-01-01&end_date=2026-03-31&prediction_type=12&tournament=World+Cup
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start_date` | date | - | Filter start date (YYYY-MM-DD) |
| `end_date` | date | - | Filter end date |
| `prediction_type` | str | all | Filter by prediction type (1, X, 2, 1X, X2, 12) |
| `tournament` | str | all | Filter by tournament |
| `min_confidence` | int | 0 | Minimum confidence threshold |

---

## 🚫 Error Codes

| Code | Message | Cause | Solution |
|------|---------|-------|----------|
| **400** | Bad Request | Invalid JSON or missing fields | Check request format |
| **404** | Not Found | Team/resource doesn't exist | Verify team names |
| **422** | Unprocessable Entity | Invalid data types | Check data ranges |
| **500** | Internal Server Error | Model initialization failed | Check logs |
| **503** | Service Unavailable | Server temporarily down | Retry later |

---

## 💡 Code Examples

### Python Integration

```python
from src.models.ensemble import EnsemblePredictor
import pandas as pd

# Load historical data
df = pd.read_csv('data/historical_matches.csv')

# Initialize ensemble
ensemble = EnsemblePredictor(df)

# Generate single prediction
pred = ensemble.generate_prediction(
    'Argentina', 'France',
    {'form': 0.8, 'off_eff': 1.2, 'def_eff': 0.9},
    {'form': 0.75, 'off_eff': 1.15, 'def_eff': 0.95}
)

print(f"Argentina win: {pred['home_win_prob']:.0%}")
print(f"Confidence: {pred['confidence_level']}")
```

### JavaScript Integration

```javascript
async function getPrediction(homeTeam, awayTeam) {
    const payload = {
        home_team: homeTeam,
        away_team: awayTeam,
        home_features: {'form': 0.8, 'off_eff': 1.2, 'def_eff': 0.9},
        away_features: {'form': 0.75, 'off_eff': 1.15, 'def_eff': 0.95}
    };
    
    const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    });
    
    return await response.json();
}

getPrediction('Argentina', 'France')
    .then(data => console.log(data.prediction));
```

### cURL Integration

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "home_team": "Argentina",
    "away_team": "France",
    "home_features": {"form": 0.8, "off_eff": 1.2, "def_eff": 0.9},
    "away_features": {"form": 0.75, "off_eff": 1.15, "def_eff": 0.95}
  }'
```

---

## ⚡ Rate Limiting

**Current**: Unlimited (development mode)

**Production recommendations**:

```python
# Implement rate limiting
MAX_REQUESTS_PER_MINUTE = 60
MAX_BATCH_SIZE = 100

# For Streamlit: cache to reduce repeated calls
@st.cache_data(ttl=3600)
def get_prediction(team1, team2, features1, features2):
    return ensemble.generate_prediction(team1, team2, features1, features2)
```

---

## 📋 API Versioning

Current API version: **v1.0**

```
http://localhost:8000/api/v1/predict
http://localhost:8000/api/v2/predict  (future)
```

---

## 🔒 Security Considerations

### To Implement for Production:

1. **Authentication**: API key or JWT tokens
2. **HTTPS**: SSL/TLS encryption
3. **CORS**: Configure allowed origins
4. **Input Validation**: Sanitize all inputs
5. **Rate Limiting**: Prevent abuse
6. **Logging**: Track all API calls
7. **Error Masking**: Don't expose internal errors

---

## 📞 Support & Questions

For API issues or questions:
- Check documentation at `Model_DOCUMENTATION.md`
- Review example scripts in `src/dashboard/app.py`
- Test using the validation script: `validate_full_dataset.py`

---

**Version**: 1.0  
**Last Updated**: March 20, 2026
