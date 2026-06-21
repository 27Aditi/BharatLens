import yfinance as yf
import pandas as pd
import numpy as np
import requests
import feedparser
from datetime import datetime, timedelta

INDICES = {
    "NIFTY 50":   "^NSEI",
    "SENSEX":     "^BSESN",
    "NIFTY BANK": "^NSEBANK",
    "NIFTY IT":   "^CNXIT",
    "USD/INR":    "INR=X",
    "Gold (MCX)": "GC=F",
    "Crude Oil":  "CL=F",
}

def fetch_market_data():
    rows = []
    for name, ticker in INDICES.items():
        try:
            t    = yf.Ticker(ticker)
            hist = t.history(period="2d")
            if isinstance(hist.columns, pd.MultiIndex):
                hist.columns = hist.columns.get_level_values(0)
            if len(hist) >= 2:
                prev = hist["Close"].iloc[-2]
                curr = hist["Close"].iloc[-1]
                chg  = ((curr - prev) / prev) * 100
            elif len(hist) == 1:
                curr = hist["Close"].iloc[-1]
                chg  = 0.0
            else:
                continue
            rows.append({
                "name":       name,
                "value":      round(float(curr), 2),
                "change_pct": round(float(chg), 2),
            })
        except Exception:
            pass
    return pd.DataFrame(rows)

def fetch_nifty_history(years=3):
    end   = datetime.today()
    start = end - timedelta(days=365 * years)
    df    = yf.download("^NSEI", start=start, end=end, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[["Close"]].dropna().reset_index()
    df.columns = ["Date", "Close"]
    return df

WB_INDICATORS = {
    "GDP Growth (%)":    "NY.GDP.MKTP.KD.ZG",
    "Inflation (CPI %)": "FP.CPI.TOTL.ZG",
    "Unemployment (%)":  "SL.UEM.TOTL.ZS",
    "FDI Inflows ($B)":  "BX.KLT.DINV.CD.WD",
}

def fetch_macro_data():
    rows = []
    for label, indicator in WB_INDICATORS.items():
        url = (
            f"https://api.worldbank.org/v2/country/IN/indicator/{indicator}"
            f"?format=json&mrv=6&per_page=6"
        )
        try:
            r    = requests.get(url, timeout=8)
            data = r.json()
            if len(data) > 1 and data[1]:
                for entry in data[1]:
                    if entry.get("value") is not None:
                        rows.append({
                            "indicator": label,
                            "year":      entry["date"],
                            "value":     round(entry["value"], 2),
                        })
                        break
        except Exception:
            pass
    return pd.DataFrame(rows)

STATE_DATA = {
    "Maharashtra":    {"gdp_rank": 1,  "unemployment": 5.1, "fdi_rank": 1,  "infra_score": 8.2},
    "Tamil Nadu":     {"gdp_rank": 2,  "unemployment": 3.8, "fdi_rank": 3,  "infra_score": 7.9},
    "Gujarat":        {"gdp_rank": 3,  "unemployment": 2.9, "fdi_rank": 2,  "infra_score": 8.5},
    "Karnataka":      {"gdp_rank": 4,  "unemployment": 4.2, "fdi_rank": 4,  "infra_score": 8.0},
    "Uttar Pradesh":  {"gdp_rank": 5,  "unemployment": 7.4, "fdi_rank": 8,  "infra_score": 5.8},
    "Rajasthan":      {"gdp_rank": 6,  "unemployment": 6.1, "fdi_rank": 7,  "infra_score": 6.2},
    "West Bengal":    {"gdp_rank": 7,  "unemployment": 6.8, "fdi_rank": 9,  "infra_score": 5.9},
    "Telangana":      {"gdp_rank": 8,  "unemployment": 3.5, "fdi_rank": 5,  "infra_score": 7.7},
    "Andhra Pradesh": {"gdp_rank": 9,  "unemployment": 4.9, "fdi_rank": 6,  "infra_score": 6.8},
    "Madhya Pradesh": {"gdp_rank": 10, "unemployment": 5.5, "fdi_rank": 11, "infra_score": 5.5},
    "Kerala":         {"gdp_rank": 11, "unemployment": 6.3, "fdi_rank": 10, "infra_score": 7.1},
    "Punjab":         {"gdp_rank": 12, "unemployment": 7.8, "fdi_rank": 13, "infra_score": 6.4},
    "Haryana":        {"gdp_rank": 13, "unemployment": 8.1, "fdi_rank": 12, "infra_score": 7.0},
    "Bihar":          {"gdp_rank": 14, "unemployment": 9.2, "fdi_rank": 18, "infra_score": 4.1},
    "Odisha":         {"gdp_rank": 15, "unemployment": 5.8, "fdi_rank": 14, "infra_score": 5.3},
}

def get_state_scores():
    rows = []
    for state, d in STATE_DATA.items():
        health = (
            (28 - d["gdp_rank"]) / 27 * 35
            + (10 - d["unemployment"]) / 10 * 30
            + (20 - d["fdi_rank"])  / 19 * 20
            + d["infra_score"] / 10 * 15
        )
        rows.append({
            "state":        state,
            "health_score": round(health, 1),
            "unemployment": d["unemployment"],
            "infra_score":  d["infra_score"],
            "gdp_rank":     d["gdp_rank"],
        })
    df = pd.DataFrame(rows).sort_values("health_score", ascending=False)
    df["grade"] = pd.cut(
        df["health_score"],
        bins=[0, 50, 65, 80, 100],
        labels=["D", "C", "B", "A"],
    )
    return df

NEWS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.moneycontrol.com/rss/economy.xml",
    "https://feeds.feedburner.com/ndtvprofit-latest",
]

def fetch_news(max_articles=30):
    articles = []
    for url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                articles.append({
                    "title":     entry.get("title", ""),
                    "summary":   entry.get("summary", "")[:300],
                    "published": entry.get("published", ""),
                    "link":      entry.get("link", ""),
                    "source":    feed.feed.get("title", "News"),
                })
        except Exception:
            pass
    return articles[:max_articles]
