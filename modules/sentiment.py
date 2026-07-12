from typing import List, Dict
from deep_translator import GoogleTranslator
import requests
import re
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"

def _get_headers():
    token = st.secrets.get("HF_TOKEN", "")
    return {"Authorization": f"Bearer {token}"}

def _is_hindi(text: str) -> bool:
    return bool(re.search(r'[\u0900-\u097F]', text))

def _translate_if_hindi(text: str) -> str:
    try:
        if _is_hindi(text):
            return GoogleTranslator(source='hi', target='en').translate(text[:500])
    except Exception:
        pass
    return text

def analyze_sentiment(text: str) -> Dict:
    clean = _translate_if_hindi(text)[:512].strip()
    if not clean:
        return {"label": "neutral", "score": 0.5, "emoji": "🟡"}
    try:
        response = requests.post(
            API_URL,
            headers=_get_headers(),
            json={"inputs": clean},
            timeout=10
        )
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            top = sorted(result[0], key=lambda x: x["score"], reverse=True)[0]
            label = top["label"].lower()
            score = round(top["score"], 3)
            emoji = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}.get(label, "🟡")
            return {"label": label, "score": score, "emoji": emoji}
    except Exception:
        pass
    return {"label": "neutral", "score": 0.5, "emoji": "🟡"}

def batch_sentiment(articles: List[Dict]) -> List[Dict]:
    return [{**art, **analyze_sentiment((art.get("title","") + " " + art.get("summary","")).strip())} for art in articles]

def overall_market_sentiment(articles: List[Dict]) -> Dict:
    if not articles:
        return {"label": "neutral", "score": 0.5, "emoji": "😐", "breakdown": {}}
    counts = {"positive": 0, "negative": 0, "neutral": 0}
    for a in articles:
        counts[a.get("label", "neutral")] += 1
    total    = sum(counts.values()) or 1
    dominant = max(counts, key=counts.get)
    emoji    = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}[dominant]
    return {
        "label":     dominant,
        "score":     round(counts["positive"] / total, 3),
        "emoji":     emoji,
        "breakdown": {k: round(v / total * 100, 1) for k, v in counts.items()},
    }
