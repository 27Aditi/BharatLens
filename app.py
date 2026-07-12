import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="BharatLens — India Economic Pulse",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: #020817;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(120,60,255,0.15), transparent),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,200,255,0.08), transparent);
    color: #e2e8f0;
}


[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #080c18 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] .stSlider > div { color: #94a3b8 !important; }


#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem !important; max-width: 1400px !important; }


.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e1040 50%, #0f172a 100%);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 20px;
    padding: 36px 40px;
    margin: 24px 0 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(90deg, rgba(139,92,246,0.1) 0%, rgba(6,182,212,0.1) 100%);
    border-radius: 20px;
}
.hero-title {
    font-size: 2.8rem; font-weight: 800; line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #22d3ee 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative; z-index: 1;
}
.hero-sub {
    font-size: 1rem; color: #64748b; margin-top: 8px;
    position: relative; z-index: 1;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(90deg, rgba(139,92,246,0.2), rgba(6,182,212,0.2));
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 100px; padding: 4px 14px;
    font-size: 0.72rem; font-weight: 600; color: #a78bfa;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 12px; position: relative; z-index: 1;
}
.hero-stats {
    display: flex; gap: 32px; margin-top: 20px;
    position: relative; z-index: 1;
}
.hero-stat-val {
    font-size: 1.4rem; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #22d3ee;
}
.hero-stat-lbl { font-size: 0.72rem; color: #475569; margin-top: 2px; }


.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 24px; }
.kpi-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,16,64,0.5) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 18px 16px;
    transition: all 0.2s ease;
    cursor: default;
    min-width: 0;
    overflow: hidden;
}
.kpi-card:hover {
    border-color: rgba(139,92,246,0.4);
    box-shadow: 0 0 24px rgba(139,92,246,0.12), 0 8px 32px rgba(0,0,0,0.3);
    transform: translateY(-2px);
}
.kpi-value {
    font-size: 1.25rem; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.kpi-name { font-size: 0.7rem; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }
.kpi-change { font-size: 0.78rem; font-weight: 600; margin-top: 6px; }
.pos { color: #34d399; }
.neg { color: #f87171; }
.neu { color: #94a3b8; }


.sec-head {
    display: flex; align-items: center; gap: 10px;
    font-size: 1rem; font-weight: 700; color: #f1f5f9;
    margin: 28px 0 16px;
}
.sec-head-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(139,92,246,0.4), transparent);
}
.sec-head-icon {
    width: 28px; height: 28px; border-radius: 8px;
    background: linear-gradient(135deg, #7c3aed, #0891b2);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}


.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 8px 18px !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(8,145,178,0.3)) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 20px 0 0 !important; }


.news-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.8), rgba(30,16,64,0.3));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 16px 18px; margin-bottom: 10px;
    transition: all 0.2s;
}
.news-card:hover { border-color: rgba(139,92,246,0.3); transform: translateX(4px); }
.news-title { font-size: 0.88rem; font-weight: 500; color: #e2e8f0; line-height: 1.5; }
.news-meta  { font-size: 0.72rem; color: #475569; margin-top: 6px; display:flex; align-items:center; gap:8px; }
.badge {
    display: inline-block; padding: 2px 10px; border-radius: 100px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.05em;
}
.badge-pos { background: rgba(5,46,22,0.8); color: #4ade80; border: 1px solid rgba(74,222,128,0.2); }
.badge-neg { background: rgba(69,10,10,0.8); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
.badge-neu { background: rgba(28,25,23,0.8); color: #a8a29e; border: 1px solid rgba(168,162,158,0.2); }


.mood-box {
    background: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(30,16,64,0.6));
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 20px; padding: 28px 20px; text-align: center;
}


.metric-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(30,16,64,0.4));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 20px;
    text-align: center;
}
.metric-val {
    font-size: 1.8rem; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #a78bfa, #22d3ee);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-lbl { font-size: 0.72rem; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }


.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #0891b2) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 600 !important;
    padding: 10px 24px !important; font-size: 0.9rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}


div[data-testid="stMetricValue"] {
    background: linear-gradient(135deg, #a78bfa, #22d3ee);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; font-weight: 700 !important;
}
div[data-testid="stMetricLabel"] { color: #475569 !important; font-size: 0.75rem !important; }
div[data-testid="stMetricDelta"] { font-size: 0.82rem !important; }


.stSlider [data-baseweb="slider"] { margin-top: 4px; }


.streamlit-expanderHeader {
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important; color: #94a3b8 !important;
}


.stSelectbox > div > div {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}


::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #020817; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.3); border-radius: 3px; }


.footer {
    text-align: center; color: #1e293b; font-size: 0.72rem;
    margin-top: 60px; padding: 16px;
    border-top: 1px solid rgba(255,255,255,0.04);
}


.stAlert { border-radius: 12px !important; border: 1px solid rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)


from modules.data_fetch import (
    fetch_market_data, fetch_nifty_history,
    fetch_macro_data, get_state_scores, fetch_news,
)
from modules.sentiment import batch_sentiment, overall_market_sentiment
from modules.whatif    import simulate

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e2e8f0",
    font_family="Inter",
    margin=dict(l=10, r=10, t=30, b=10),
)
GRID = dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)")


with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 8px'>
      <div style='font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,#a78bfa,#22d3ee);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text'>
        🇮🇳 BharatLens
      </div>
      <div style='font-size:0.72rem;color:#334155;margin-top:4px'>India Economic Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("<p style='font-size:0.78rem;color:#475569;font-weight:600;text-transform:uppercase;letter-spacing:0.08em'>⚙️ Controls</p>", unsafe_allow_html=True)
    lstm_epochs = st.slider("LSTM Epochs",    10, 60, 25, 5)
    pred_days   = st.slider("Forecast Days",   7, 60, 30, 7)
    max_news    = st.slider("News Articles",   5, 30, 15, 5)
    st.divider()
    st.markdown("""
    <div style='font-size:0.72rem;color:#1e293b;line-height:1.8'>
      📡 Yahoo Finance<br>
      🏦 World Bank API<br>
      📰 ET · MoneyControl<br>
      🤖 FinBERT · PyTorch
    </div>
    """, unsafe_allow_html=True)


with st.spinner(""):
    mkt_df = fetch_market_data()
    st.session_state["mkt_df"] = mkt_df

nifty_val  = "—"
nifty_chg  = ""
nifty_color = "#22d3ee"
if not mkt_df.empty and "NIFTY 50" in mkt_df["name"].values:
    row = mkt_df[mkt_df["name"] == "NIFTY 50"].iloc[0]
    nifty_val = f"₹{row['value']:,.0f}"
    sign = "▲" if row["change_pct"] >= 0 else "▼"
    nifty_chg = f"{sign} {abs(row['change_pct']):.2f}%"
    nifty_color = "#34d399" if row["change_pct"] >= 0 else "#f87171"

st.markdown(f"""
<div class='hero'>
  <div class='hero-badge'>🔴 Live · Real-Time Data</div>
  <div class='hero-title'>BharatLens</div>
  <div class='hero-sub'>India's AI-Powered Economic Intelligence Platform</div>
  <div class='hero-stats'>
    <div>
      <div class='hero-stat-val'>{nifty_val}</div>
      <div class='hero-stat-lbl'>NIFTY 50</div>
    </div>
    <div>
      <div class='hero-stat-val' style='color:{nifty_color}'>{nifty_chg}</div>
      <div class='hero-stat-lbl'>Today's Change</div>
    </div>
    <div>
      <div class='hero-stat-val'>5</div>
      <div class='hero-stat-lbl'>AI Modules</div>
    </div>
    <div>
      <div class='hero-stat-val'>15</div>
      <div class='hero-stat-lbl'>States Tracked</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Market Pulse",
    "🔮  NIFTY Forecast",
    "📰  News Sentiment",
    "🗺️  State Health",
    "⚡  What-If Lab",
])


with tab1:
    st.markdown("<div class='sec-head'><div class='sec-head-icon'>📊</div>Live Market Snapshot<div class='sec-head-line'></div></div>", unsafe_allow_html=True)

    if mkt_df.empty:
        st.warning("Could not fetch live data. Check internet connection.")
    else:
        cols = st.columns(len(mkt_df))
        for i, (_, row) in enumerate(mkt_df.iterrows()):
            chg   = row["change_pct"]
            cls   = "pos" if chg >= 0 else "neg"
            arrow = "▲" if chg >= 0 else "▼"
            with cols[i]:
                st.markdown(f"""
                <div class='kpi-card'>
                  <div class='kpi-value {cls}'>{row['value']:,.1f}</div>
                  <div class='kpi-name'>{row['name']}</div>
                  <div class='kpi-change {cls}'>{arrow} {abs(chg):.2f}%</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-head'><div class='sec-head-icon'>🏦</div>Macro Indicators<div class='sec-head-line'></div></div>", unsafe_allow_html=True)
    with st.spinner("Fetching World Bank indicators..."):
        macro_df = fetch_macro_data()

    if not macro_df.empty:
        mc = st.columns(len(macro_df))
        for i, (_, row) in enumerate(macro_df.iterrows()):
            with mc[i]:
                st.markdown(f"""
                <div class='metric-card'>
                  <div class='metric-val'>{row['value']:.2f}</div>
                  <div class='metric-lbl'>{row['indicator']}</div>
                  <div style='font-size:0.68rem;color:#334155;margin-top:4px'>{row['year']}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("World Bank API is slow — try again in a moment.")

    st.markdown("<div class='sec-head'><div class='sec-head-icon'>📈</div>NIFTY 50 — 6 Month Trend<div class='sec-head-line'></div></div>", unsafe_allow_html=True)
    with st.spinner("Loading chart..."):
        hist_df = fetch_nifty_history(years=1)

    if not hist_df.empty:
        last6m = hist_df.tail(126)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=last6m["Date"], y=last6m["Close"],
            mode="lines",
            line=dict(color="#a78bfa", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(167,139,250,0.06)",
            hovertemplate="<b>₹%{y:,.0f}</b><br>%{x|%d %b %Y}<extra></extra>",
        ))
        
        ma20 = last6m["Close"].rolling(20).mean()
        fig.add_trace(go.Scatter(
            x=last6m["Date"], y=ma20,
            mode="lines", name="20D MA",
            line=dict(color="#22d3ee", width=1.5, dash="dot"),
            hovertemplate="MA: ₹%{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT, height=320,
            xaxis=dict(**GRID, color="#475569"),
            yaxis=dict(**GRID, color="#475569", title="NIFTY 50"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11)),
            showlegend=True,
        )
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})


with tab2:
    st.markdown("<div class='sec-head'><div class='sec-head-icon'>🔮</div>LSTM Neural Network Forecast<div class='sec-head-line'></div></div>", unsafe_allow_html=True)

    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.markdown(f"<div class='metric-card'><div class='metric-val'>{lstm_epochs}</div><div class='metric-lbl'>Training Epochs</div></div>", unsafe_allow_html=True)
    with col_info2:
        st.markdown(f"<div class='metric-card'><div class='metric-val'>{pred_days}D</div><div class='metric-lbl'>Forecast Window</div></div>", unsafe_allow_html=True)
    with col_info3:
        st.markdown("<div class='metric-card'><div class='metric-val'>LSTM</div><div class='metric-lbl'>Model Architecture</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀  Train Model & Generate Forecast", key="train_btn"):
        prog = st.progress(0, text="Downloading 3 years of NIFTY data...")
        from models.lstm_model import train_model, predict_future, get_historical_predictions
        hist_df_full = fetch_nifty_history(years=3)
        prog.progress(20, text="Preprocessing & scaling data...")
        artifacts  = train_model(hist_df_full, epochs=lstm_epochs)
        prog.progress(80, text="Generating forecast with uncertainty bands...")
        future_df  = predict_future(artifacts, days=pred_days)
        hist_preds = get_historical_predictions(artifacts)
        prog.progress(100, text="Done!")
        st.session_state["artifacts"]  = artifacts
        st.session_state["future_df"]  = future_df
        st.session_state["hist_preds"] = hist_preds
        prog.empty()
        st.success("Model trained successfully!")

    if "future_df" in st.session_state:
        artifacts  = st.session_state["artifacts"]
        future_df  = st.session_state["future_df"]
        hist_preds = st.session_state["hist_preds"]
        hist_df_f  = artifacts["history_df"]

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=hist_df_f["Date"].tail(200), y=hist_df_f["Close"].tail(200),
            name="Historical", line=dict(color="#94a3b8", width=1.5),
            hovertemplate="₹%{y:,.0f}<extra>Historical</extra>",
        ))
        fig2.add_trace(go.Scatter(
            x=hist_preds["Date"], y=hist_preds["Predicted"],
            name="Validation", line=dict(color="#a78bfa", width=2, dash="dot"),
            hovertemplate="₹%{y:,.0f}<extra>Validation</extra>",
        ))
        fig2.add_trace(go.Scatter(
            x=future_df["Date"], y=future_df["Predicted"],
            name="Forecast", line=dict(color="#f59e0b", width=3),
            hovertemplate="₹%{y:,.0f}<extra>Forecast</extra>",
        ))
        fig2.add_trace(go.Scatter(
            x=pd.concat([future_df["Date"], future_df["Date"][::-1]]),
            y=pd.concat([future_df["Upper"], future_df["Lower"][::-1]]),
            fill="toself", fillcolor="rgba(245,158,11,0.08)",
            line=dict(color="rgba(0,0,0,0)"), name="Uncertainty Band",
        ))
        fig2.update_layout(
            **PLOTLY_LAYOUT, height=440,
            xaxis=dict(**GRID, color="#475569"),
            yaxis=dict(**GRID, color="#475569", title="NIFTY 50"),
            legend=dict(bgcolor="rgba(15,23,42,0.8)", font=dict(color="#94a3b8", size=11),
                        bordercolor="rgba(255,255,255,0.06)", borderwidth=1),
        )
        st.plotly_chart(fig2, width='stretch')

        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📉  Training & Validation Loss"):
                loss_df = pd.DataFrame({
                    "Epoch": list(range(1, len(artifacts["train_losses"]) + 1)),
                    "Train Loss": artifacts["train_losses"],
                    "Val Loss":   artifacts["val_losses"],
                })
                fig_l = px.line(loss_df, x="Epoch", y=["Train Loss","Val Loss"],
                                color_discrete_map={"Train Loss":"#a78bfa","Val Loss":"#22d3ee"})
                
                fig_l.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0",
                    font_family="Inter",
                    height=260,
                    margin=dict(l=10, r=10, t=10, b=10),
                    xaxis=dict(**GRID), yaxis=dict(**GRID),
                    legend=dict(bgcolor="rgba(0,0,0,0)"))
                st.plotly_chart(fig_l, width='stretch', config={"displayModeBar":False})
        with c2:
            with st.expander("📋  Forecast Table"):
                st.dataframe(
                    future_df.style.format({"Predicted":"₹{:,.0f}","Upper":"₹{:,.0f}","Lower":"₹{:,.0f}"}),
                    width='stretch',
                )
    else:
        st.info("👆 Click the button above to train the LSTM and generate a forecast.")


with tab3:
    st.markdown("<div class='sec-head'><div class='sec-head-icon'>📰</div>News Sentiment Analysis — Hindi + English<div class='sec-head-line'></div></div>", unsafe_allow_html=True)

    if st.button("🔍  Fetch & Analyze News", key="news_btn"):
        with st.spinner("Scraping RSS feeds and running FinBERT..."):
            raw  = fetch_news(max_articles=max_news)
            if raw:
                enriched = batch_sentiment(raw)
                st.session_state["enriched_news"] = enriched
            else:
                st.warning("No articles fetched.")

    if "enriched_news" in st.session_state:
        enriched = st.session_state["enriched_news"]
        mood     = overall_market_sentiment(enriched)

        c1, c2, c3 = st.columns([1, 1, 2])
        color = {"positive":"#34d399","negative":"#f87171","neutral":"#94a3b8"}[mood["label"]]
        with c1:
            st.markdown(f"""
            <div class='mood-box'>
              <div style='font-size:3.5rem;line-height:1'>{mood['emoji']}</div>
              <div style='font-size:1.1rem;font-weight:700;color:{color};margin-top:10px'>{mood['label'].upper()}</div>
              <div style='color:#475569;font-size:0.72rem;margin-top:4px'>Market Mood</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='mood-box' style='height:100%'>
              <div style='font-size:0.72rem;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:12px'>Breakdown</div>
              <div style='display:flex;flex-direction:column;gap:8px'>
                <div style='display:flex;justify-content:space-between;align-items:center'>
                  <span style='color:#34d399;font-size:0.82rem'>🟢 Positive</span>
                  <span style='color:#34d399;font-weight:700;font-family:JetBrains Mono'>{mood['breakdown']['positive']}%</span>
                </div>
                <div style='display:flex;justify-content:space-between;align-items:center'>
                  <span style='color:#f87171;font-size:0.82rem'>🔴 Negative</span>
                  <span style='color:#f87171;font-weight:700;font-family:JetBrains Mono'>{mood['breakdown']['negative']}%</span>
                </div>
                <div style='display:flex;justify-content:space-between;align-items:center'>
                  <span style='color:#94a3b8;font-size:0.82rem'>🟡 Neutral</span>
                  <span style='color:#94a3b8;font-weight:700;font-family:JetBrains Mono'>{mood['breakdown']['neutral']}%</span>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
        with c3:
            bd = mood["breakdown"]
            fig_pie = go.Figure(go.Pie(
                labels=["Positive","Negative","Neutral"],
                values=[bd["positive"], bd["negative"], bd["neutral"]],
                marker_colors=["#34d399","#f87171","#64748b"],
                hole=0.65,
                textfont=dict(color="#e2e8f0", size=11),
            ))
            fig_pie.add_annotation(text=f"<b>{mood['label'].title()}</b>", x=0.5, y=0.5,
                                   font=dict(size=14, color=color), showarrow=False)
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                font_family="Inter",
                height=220,
                margin=dict(l=10, r=80, t=20, b=10),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11)))
            st.plotly_chart(fig_pie, width='stretch', config={"displayModeBar":False})

        st.markdown("<div class='sec-head'><div class='sec-head-icon'>📄</div>Article Feed<div class='sec-head-line'></div></div>", unsafe_allow_html=True)
        for art in enriched:
            bc = {"positive":"badge-pos","negative":"badge-neg","neutral":"badge-neu"}.get(art["label"],"badge-neu")
            st.markdown(f"""
            <div class='news-card'>
              <div class='news-title'>{art['emoji']} &nbsp;{art['title']}</div>
              <div class='news-meta'>
                <span>{art.get('source','')}</span>
                <span>·</span>
                <span>{art.get('published','')[:16]}</span>
                <span class='badge {bc}'>{art['label'].upper()} · {art['score']:.2f}</span>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("👆 Click the button above to fetch and analyze latest financial news.")


with tab4:
    st.markdown("<div class='sec-head'><div class='sec-head-icon'>🗺️</div>State-Level Economic Health<div class='sec-head-line'></div></div>", unsafe_allow_html=True)
    state_df = get_state_scores()

    fig_s = go.Figure(go.Bar(
        x=state_df["health_score"],
        y=state_df["state"],
        orientation="h",
        marker=dict(
            color=state_df["health_score"],
            colorscale=[[0,"#f87171"],[0.4,"#f59e0b"],[0.7,"#a78bfa"],[1,"#22d3ee"]],
            showscale=False,
        ),
        text=[f"  {s:.1f}" for s in state_df["health_score"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=12, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>",
    ))
    fig_s.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        font_family="Inter",
        height=520,
        margin=dict(l=10, r=80, t=20, b=10),
        xaxis=dict(**GRID, color="#475569", range=[0, 110]),
        yaxis=dict(color="#e2e8f0", autorange="reversed", tickfont=dict(size=12))
    )
    st.plotly_chart(fig_s, width='stretch')

    st.markdown("<div class='sec-head'><div class='sec-head-icon'>🔎</div>State Deep Dive<div class='sec-head-line'></div></div>", unsafe_allow_html=True)
    selected = st.selectbox("Select a State", state_df["state"].tolist(), label_visibility="collapsed")
    row = state_df[state_df["state"] == selected].iloc[0]
    d1, d2, d3, d4 = st.columns(4)
    for col, val, lbl in [
        (d1, f"{row['health_score']:.1f}/100", "Health Score"),
        (d2, str(row["grade"]),                 "Grade"),
        (d3, f"{row['unemployment']}%",          "Unemployment"),
        (d4, f"{row['infra_score']}/10",         "Infra Score"),
    ]:
        with col:
            st.markdown(f"<div class='metric-card'><div class='metric-val'>{val}</div><div class='metric-lbl'>{lbl}</div></div>", unsafe_allow_html=True)


with tab5:
    st.markdown("<div class='sec-head'><div class='sec-head-icon'>⚡</div>What-If Economic Simulator<div class='sec-head-line'></div></div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#475569;font-size:0.85rem;margin-bottom:20px'>Adjust macro levers and see the AI-estimated impact on NIFTY 50 and key sectors in real time.</p>", unsafe_allow_html=True)

    base_nifty = 22500.0
    mkt_cached = st.session_state.get("mkt_df", pd.DataFrame())
    if not mkt_cached.empty and "NIFTY 50" in mkt_cached["name"].values:
        base_nifty = float(mkt_cached[mkt_cached["name"] == "NIFTY 50"]["value"].iloc[0])

    w1, w2 = st.columns(2)
    with w1:
        st.markdown("<p style='font-size:0.78rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px'>Monetary Policy</p>", unsafe_allow_html=True)
        rbi_delta   = st.slider("🏦 RBI Rate Change (%)",         -1.0,  1.0, 0.0, 0.25)
        fdi_delta   = st.slider("💰 FDI Change ($B)",             -10.0, 10.0, 0.0, 0.5)
    with w2:
        st.markdown("<p style='font-size:0.78rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px'>Global Factors</p>", unsafe_allow_html=True)
        crude_delta = st.slider("🛢️ Crude Oil Change ($/barrel)", -20.0, 20.0, 0.0, 1.0)
        fx_delta    = st.slider("💱 USD/INR Change (₹)",          -5.0,  5.0,  0.0, 0.5)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡  Run Simulation", key="sim_btn"):
        result = simulate(base_nifty, rbi_delta, crude_delta, fx_delta, fdi_delta)
        chg    = result["total_change"]
        chg_color = "#34d399" if chg >= 0 else "#f87171"

        r1, r2, r3 = st.columns(3)
        r1.metric("Base NIFTY",      f"₹{result['base_nifty']:,.0f}")
        r2.metric("Simulated NIFTY", f"₹{result['new_nifty']:,.0f}", delta=f"{chg:+.2f}%")
        r3.metric("Net Impact",      f"{chg:+.2f}%")

        st.markdown("<div class='sec-head'><div class='sec-head-icon'>📊</div>Sector Impact<div class='sec-head-line'></div></div>", unsafe_allow_html=True)
        sectors = result["sector_impact"]
        sec_fig = go.Figure(go.Bar(
            x=list(sectors.values()),
            y=list(sectors.keys()),
            orientation="h",
            marker_color=["#34d399" if v >= 0 else "#f87171" for v in sectors.values()],
            text=[f"{v:+.2f}%" for v in sectors.values()],
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=12, family="JetBrains Mono"),
            hovertemplate="<b>%{y}</b><br>Impact: %{x:+.2f}%<extra></extra>",
        ))
        sec_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            font_family="Inter",
            height=300,
            margin=dict(l=10, r=80, t=20, b=10),
            xaxis={**GRID, "color": "#475569", "zeroline": True, "zerolinecolor": "rgba(255,255,255,0.1)"},
            yaxis=dict(color="#e2e8f0"),
        )
        st.plotly_chart(sec_fig, width='stretch', config={"displayModeBar": False})

        if result["reasons"]:
            st.markdown("<div class='sec-head'><div class='sec-head-icon'>🤖</div>AI Reasoning<div class='sec-head-line'></div></div>", unsafe_allow_html=True)
            for r in result["reasons"]:
                st.markdown(f"<div class='news-card'><div class='news-title'>💡 &nbsp;{r}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:linear-gradient(135deg,rgba(15,23,42,0.6),rgba(30,16,64,0.3));
             border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:32px;text-align:center'>
          <div style='font-size:2rem;margin-bottom:8px'>⚡</div>
          <div style='color:#475569;font-size:0.88rem'>Adjust the sliders above and click <strong style='color:#a78bfa'>Run Simulation</strong></div>
        </div>""", unsafe_allow_html=True)


st.markdown("""
<div class='footer'>
  BharatLens &nbsp;·&nbsp; Built with Streamlit, PyTorch & FinBERT
  &nbsp;·&nbsp; Data: Yahoo Finance · World Bank · Economic Times · MoneyControl
</div>""", unsafe_allow_html=True)
