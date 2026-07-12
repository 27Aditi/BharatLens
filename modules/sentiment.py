from typing import List, Dict
from transformers import pipeline
from deep_translator import GoogleTranslator
import re

_sentiment_pipe = None

def _load_pipe():
    global _sentiment_pipe
    if _sentiment_pipe is None:
        _sentiment_pipe = pipeline(
            "text-classification",
            model="ProsusAI/finbert",
            truncation=True,
            max_length=512,
        )
    return _sentiment_pipe

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
    pipe  = _load_pipe()
    clean = _translate_if_hindi(text)
    clean = clean[:512].strip()
    if not clean:
        return {"label": "neutral", "score": 0.5, "emoji": "😐"}
    try:
        result = pipe(clean)[0]
        label  = result["label"].lower()
        score  = round(result["score"], 3)
        emoji  = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}.get(label, "🟡")
        return {"label": label, "score": score, "emoji": emoji}
    except Exception:
        return {"label": "neutral", "score": 0.5, "emoji": "😐"}

def batch_sentiment(articles: List[Dict]) -> List[Dict]:
    enriched = []
    for art in articles:
        text = (art.get("title", "") + " " + art.get("summary", "")).strip()
        s    = analyze_sentiment(text)
        enriched.append({**art, **s})
    return enriched

def overall_market_sentiment(articles: List[Dict]) -> Dict:
    if not articles:
        return {"label": "neutral", "score": 0.5, "emoji": "😐", "breakdown": {}}

    counts = {"positive": 0, "negative": 0, "neutral": 0}
    for a in articles:
        counts[a.get("label", "neutral")] += 1

    total    = sum(counts.values()) or 1
    dominant = max(counts, key=counts.get)
    score    = counts["positive"] / total
    emoji    = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}[dominant]

    return {
        "label":     dominant,
        "score":     round(score, 3),
        "emoji":     emoji,
        "breakdown": {k: round(v / total * 100, 1) for k, v in counts.items()},
    }
