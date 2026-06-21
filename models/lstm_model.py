import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn

class LSTMPredictor(nn.Module):
    def __init__(self, input_size=1, hidden=64, layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden, layers,
            batch_first=True, dropout=dropout
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])


SEQ_LEN = 60   

def _make_sequences(series: np.ndarray, seq_len=SEQ_LEN):
    X, y = [], []
    for i in range(len(series) - seq_len):
        X.append(series[i: i + seq_len])
        y.append(series[i + seq_len])
    return np.array(X), np.array(y)


def train_model(df: pd.DataFrame, epochs=30) -> dict:
    prices = df["Close"].values.reshape(-1, 1).astype(np.float32)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(prices)

    X, y = _make_sequences(scaled)
    X_t  = torch.tensor(X, dtype=torch.float32)
    y_t  = torch.tensor(y, dtype=torch.float32)

    split     = int(len(X_t) * 0.85)
    X_train, X_val = X_t[:split], X_t[split:]
    y_train, y_val = y_t[:split], y_t[split:]

    model     = LSTMPredictor()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()

    train_losses, val_losses = [], []
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        pred  = model(X_train)
        loss  = criterion(pred, y_train)
        loss.backward()
        optimizer.step()
        train_losses.append(loss.item())

        model.eval()
        with torch.no_grad():
            val_loss = criterion(model(X_val), y_val).item()
        val_losses.append(val_loss)

    last_seq = scaled[-SEQ_LEN:].reshape(1, SEQ_LEN, 1)

    return {
        "model":        model,
        "scaler":       scaler,
        "train_losses": train_losses,
        "val_losses":   val_losses,
        "last_seq":     last_seq,
        "history_df":   df,
    }


def predict_future(artifacts: dict, days=30) -> pd.DataFrame:
    model    = artifacts["model"]
    scaler   = artifacts["scaler"]
    last_seq = artifacts["last_seq"].copy()

    model.eval()
    preds = []
    seq   = torch.tensor(last_seq, dtype=torch.float32)

    with torch.no_grad():
        for _ in range(days):
            out = model(seq).item()
            preds.append(out)
            new_pt = torch.tensor([[[out]]], dtype=torch.float32)
            seq    = torch.cat([seq[:, 1:, :], new_pt], dim=1)

    preds_arr    = np.array(preds).reshape(-1, 1)
    preds_actual = scaler.inverse_transform(preds_arr).flatten()

    uncertainty = preds_actual * 0.015
    last_date   = artifacts["history_df"]["Date"].iloc[-1]
    future_dates = pd.bdate_range(start=last_date, periods=days + 1)[1:]

    return pd.DataFrame({
        "Date":  future_dates[:days],
        "Predicted": np.round(preds_actual, 2),
        "Upper": np.round(preds_actual + uncertainty, 2),
        "Lower": np.round(preds_actual - uncertainty, 2),
    })


def get_historical_predictions(artifacts: dict) -> pd.DataFrame:
    model  = artifacts["model"]
    scaler = artifacts["scaler"]
    df     = artifacts["history_df"]

    prices = df["Close"].values.reshape(-1, 1).astype(np.float32)
    scaled = scaler.transform(prices)
    X, _   = _make_sequences(scaled)

    split  = int(len(X) * 0.85)
    X_val  = torch.tensor(X[split:], dtype=torch.float32)

    model.eval()
    with torch.no_grad():
        val_preds = model(X_val).numpy()

    val_preds_actual = scaler.inverse_transform(val_preds).flatten()
    val_dates        = df["Date"].iloc[SEQ_LEN + split:].values

    return pd.DataFrame({"Date": val_dates, "Predicted": np.round(val_preds_actual, 2)})
