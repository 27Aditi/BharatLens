# 🇮🇳 BharatLens — India's AI-Powered Economic Intelligence Platform

> **Real-time economic analysis, LSTM forecasting, multilingual news sentiment, and macro simulation — all in one dashboard.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?style=flat-square&logo=streamlit)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2-orange?style=flat-square&logo=pytorch)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Problem Statement

India's economic data is **fragmented** across dozens of sources — stock indices on one platform, inflation data on another, state-level indicators buried in government PDFs, and news scattered across hundreds of portals. Existing platforms like Bloomberg or Moneycontrol show numbers but offer **no explanation, no prediction, and no simulation**.

**BharatLens solves this** by aggregating real-time data from multiple sources, applying AI to analyze and forecast it, and presenting everything in a single interactive dashboard — in both **Hindi and English**.

---

## ✨ Features

| Module | Description |
|---|---|
| 📊 **Market Pulse** | Live NIFTY, SENSEX, Gold, Crude Oil, USD/INR with % change |
| 🔮 **NIFTY Forecast** | LSTM neural network trained on 3 years of data with uncertainty bands |
| 📰 **News Sentiment** | FinBERT-powered sentiment on Hindi + English financial news |
| 🗺️ **State Health** | Economic health score for 15 Indian states |
| ⚡ **What-If Lab** | Simulate impact of RBI rate changes, crude oil, FDI, and currency shifts |

---

## 🏗️ Architecture

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
Data Sources          Processing              Output
─────────────         ──────────              ──────
Yahoo Finance    →    MinMax Scaling    →     LSTM Forecast
World Bank API   →    Feature Engineering →   Macro Dashboard  
RSS News Feeds   →    Hindi Translation  →    Sentiment Score
                      FinBERT Inference  →    Market Mood
Static State Data →   Weighted Scoring  →    State Health Map
User Sliders     →    Econometric Model  →    Sector Impact
```

---

## 🧠 AI/ML Components

### 1. LSTM Forecasting Model
- **Architecture:** 2-layer LSTM → Linear(64→32) → Linear(32→1)
- **Input:** Last 60 trading days of NIFTY 50 closing prices
- **Preprocessing:** MinMaxScaler normalization to [0,1]
- **Split:** 85% train / 15% validation
- **Loss:** Mean Squared Error (MSE)
- **Output:** Next N days forecast with ±1.5% uncertainty bands
- **Why LSTM?** Stock prices are sequential — LSTM's memory cell captures long-term dependencies that vanilla RNNs miss

### 2. Sentiment Analysis (FinBERT)
- **Model:** `ProsusAI/finbert` — BERT fine-tuned on financial text
- **Labels:** Positive / Negative / Neutral
- **Hindi Support:** Devanagari text auto-detected → translated via GoogleTranslator → passed to FinBERT
- **Why FinBERT over BERT?** Domain-specific training on financial corpora makes it understand terms like "rate hike", "market rally", "FII outflow" correctly

### 3. What-If Simulator
- Uses historical elasticity coefficients derived from Indian market data
- RBI rate hike of 25 bps → NIFTY ~-1.2% (rate-sensitive sectors contract)
- Crude +$5/barrel → NIFTY ~-0.4% (import cost pressure)
- INR depreciation ₹1 → IT sector +0.8% (export revenue increases), NIFTY -0.3%
- FDI +$1B → NIFTY +0.6% (capital inflow signal)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or above
- Internet connection (for live data fetching)

### Installation

```bash
# 1. Clone or download the project
cd BharatLens

# 2. (Recommended) Create a virtual environment
python -m venv deepv
deepv\Scripts\activate        # Windows
source deepv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

App will open at `http://localhost:8501`

> ⚠️ **First run:** FinBERT model (~500MB) will download automatically when you first click "Fetch & Analyze News". This is a one-time download.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Dashboard | Streamlit |
| Neural Network | PyTorch |
| NLP Model | HuggingFace Transformers (FinBERT) |
| Market Data | yfinance (Yahoo Finance) |
| Macro Data | World Bank Open API |
| News | feedparser (RSS — ET, MoneyControl, NDTV Profit) |
| Translation | deep-translator (Google Translate) |
| Visualization | Plotly |
| Data Processing | Pandas, NumPy, Scikit-learn |

---

## 📊 Data Sources

| Source | Data |
|---|---|
| Yahoo Finance | NIFTY 50, SENSEX, NIFTY Bank, NIFTY IT, USD/INR, Gold, Crude Oil |
| World Bank API | GDP Growth, Inflation (CPI), Unemployment, FDI Inflows |
| Economic Times RSS | Financial news headlines |
| MoneyControl RSS | Economy news |
| NDTV Profit RSS | Market updates |

---

## 🎯 Key Design Decisions

**Why not use a simple regression model?**
Economic time series have long-range temporal dependencies. A linear regression predicting tomorrow's NIFTY from today's price misses patterns like weekly cycles, quarterly earnings effects, and macro shock aftereffects. LSTM's gated memory architecture is designed for exactly this.

**Why FinBERT over standard BERT?**
General BERT was trained on Wikipedia and BookCorpus — it doesn't understand financial jargon. FinBERT was fine-tuned on financial news and earnings call transcripts, making it significantly more accurate on terms like "bearish sentiment", "FII selling", or "rate corridor".

**Why translate Hindi instead of using a multilingual model?**
Multilingual models like mBERT perform worse on financial Hindi/Hinglish text because training data for this domain in Hindi is scarce. Translating to English first and using the domain-expert FinBERT gives better results.

---

## 📈 Sample Output

- NIFTY 50 forecast with confidence interval for next 30 trading days
- Overall market sentiment score from latest 15 financial news articles
- State economic health ranking from Gujarat (highest) to Bihar (lowest)
- Sector-wise impact simulation when RBI hikes rate by 0.25%

---

## 🔮 Future Improvements

- [ ] Add FII/DII flow data from NSE
- [ ] Integrate RBI monetary policy calendar
- [ ] Add portfolio risk calculator
- [ ] Deploy on Hugging Face Spaces / Streamlit Cloud
- [ ] Add alert system for high-risk economic signals
- [ ] Expand state data to all 28 states + 8 UTs

---

## 👨‍💻 Author

Built as a final year deep learning project demonstrating real-world application of LSTM time series forecasting and NLP-based sentiment analysis on Indian financial data.

---

## 📄 License

MIT License — free to use, modify, and distribute.
