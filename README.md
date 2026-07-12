# BharatLens — India's AI-Powered Economic Intelligence Platform

> Real-time economic analysis, LSTM forecasting, multilingual news sentiment, and macro simulation — all in one dashboard.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?style=flat-square&logo=streamlit)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2-orange?style=flat-square&logo=pytorch)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Problem Statement

India's economic data is **fragmented** across dozens of sources — stock indices on one platform, inflation data on another, state-level indicators buried in government PDFs, and news scattered across hundreds of portals. Existing platforms like Bloomberg or Moneycontrol display numbers but offer no explanation, no prediction, and no simulation.

BharatLens solves this by aggregating real-time data from multiple sources, applying AI to analyze and forecast it, and presenting everything in a single interactive dashboard — in both Hindi and English.

---

## Features

| Module | Description |
|---|---|
| Market Pulse | Live NIFTY, SENSEX, Gold, Crude Oil, USD/INR with % change |
| NIFTY Forecast | LSTM neural network trained on 3 years of data with uncertainty bands |
| News Sentiment | FinBERT-powered sentiment analysis on Hindi and English financial news |
| State Health | Economic health score for 15 Indian states |
| What-If Lab | Simulate impact of RBI rate changes, crude oil prices, FDI, and currency shifts |

---

## Architecture

```
BharatLens/
│
├── app.py                  # Main Streamlit dashboard
│
├── modules/
│   ├── data_fetch.py       # Data ingestion (Yahoo Finance, World Bank, RSS)
│   ├── sentiment.py        # FinBERT sentiment analysis (Hindi + English)
│   └── whatif.py           # What-If econometric simulator
│
├── models/
│   └── lstm_model.py       # LSTM architecture, training, forecasting
│
└── requirements.txt
```

### Pipeline Flow

```
Data Sources           Processing                Output
────────────           ──────────                ──────
Yahoo Finance    →     MinMax Scaling      →     LSTM Forecast
World Bank API   →     Feature Engineering →     Macro Dashboard
RSS News Feeds   →     Hindi Translation   →     Sentiment Score
                       FinBERT Inference   →     Market Mood
Static State Data →    Weighted Scoring    →     State Health Map
User Sliders      →    Econometric Model   →     Sector Impact
```

---

## AI/ML Components

### 1. LSTM Forecasting Model

- **Architecture:** 2-layer LSTM → Linear(64 → 32) → Linear(32 → 1)
- **Input:** Last 60 trading days of NIFTY 50 closing prices
- **Preprocessing:** MinMaxScaler normalization to [0, 1]
- **Split:** 85% training / 15% validation
- **Loss Function:** Mean Squared Error (MSE)
- **Output:** Next N days forecast with ±1.5% uncertainty bands
- **Why LSTM:** Stock prices are sequential — LSTM's memory cell captures long-term dependencies that standard feedforward networks miss

### 2. Sentiment Analysis — FinBERT

- **Model:** ProsusAI/finbert — BERT fine-tuned on financial text
- **Labels:** Positive / Negative / Neutral
- **Hindi Support:** Devanagari text is auto-detected, translated to English via GoogleTranslator, then passed to FinBERT
- **Why FinBERT over BERT:** Domain-specific training on financial corpora makes it understand terms like "rate hike", "market rally", and "FII outflow" accurately

### 3. What-If Simulator

Elasticity coefficients derived from historical Indian market behavior:

- RBI rate hike of 25 bps → NIFTY approximately -1.2%
- Crude oil +$5/barrel → NIFTY approximately -0.4%
- INR depreciation of Rs 1 → IT sector +0.8%, NIFTY -0.3%
- FDI inflow of +$1B → NIFTY approximately +0.6%

---

## Getting Started

### Prerequisites

- Python 3.8 or above
- Active internet connection for live data fetching

### Installation

```bash
# Clone the repository
cd BharatLens

# Create a virtual environment (recommended)
python -m venv deepv
deepv\Scripts\activate        # Windows
source deepv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at http://localhost:8501

> Note: FinBERT model (~500MB) downloads automatically on first use of the News Sentiment tab. This is a one-time download.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Dashboard | Streamlit |
| Neural Network | PyTorch |
| NLP Model | HuggingFace Transformers (FinBERT) |
| Market Data | yfinance — Yahoo Finance |
| Macro Data | World Bank Open API |
| News | feedparser — ET, MoneyControl, NDTV Profit RSS |
| Translation | deep-translator — Google Translate |
| Visualization | Plotly |
| Data Processing | Pandas, NumPy, Scikit-learn |

---

## Data Sources

| Source | Data Provided |
|---|---|
| Yahoo Finance | NIFTY 50, SENSEX, NIFTY Bank, NIFTY IT, USD/INR, Gold, Crude Oil |
| World Bank API | GDP Growth, Inflation (CPI), Unemployment, FDI Inflows |
| Economic Times RSS | Financial news headlines |
| MoneyControl RSS | Economy news |
| NDTV Profit RSS | Market updates |

---

## Key Design Decisions

**Why LSTM over simple regression?**
Economic time series have long-range temporal dependencies. Linear regression predicting tomorrow's NIFTY from today's price misses patterns like weekly cycles, quarterly earnings effects, and macro shock aftereffects. LSTM's gated memory architecture is designed specifically for this.

**Why FinBERT over standard BERT?**
General-purpose BERT was trained on Wikipedia and BookCorpus — it does not understand financial jargon. FinBERT was fine-tuned on financial news and earnings call transcripts, making it significantly more accurate on domain-specific terms.

**Why translate Hindi instead of using a multilingual model?**
Multilingual models like mBERT perform poorly on financial Hindi and Hinglish text because labeled training data for this domain in Hindi is scarce. Translating to English first and using the domain-expert FinBERT gives more reliable results.

---

## Future Improvements

- Add FII/DII flow data from NSE
- Integrate RBI monetary policy calendar
- Add portfolio risk calculator
- Add alert system for high-risk economic signals
- Expand state coverage to all 28 states and 8 Union Territories

---

## License

MIT License — free to use, modify, and distribute.
