"""Gercek hisse verisini yfinance uzerinden ceken modul."""
from __future__ import annotations

import datetime as dt
import random
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
import yfinance as yf

from .tickers import TICKER_POOL

WINDOW_SIZE = 90       # toplam gun sayisi (gecmis + gelecek)
HISTORY_SIZE = 60      # oyuncuya gosterilen gecmis gun sayisi
FUTURE_SIZE = WINDOW_SIZE - HISTORY_SIZE


@dataclass
class StockWindow:
    ticker: str
    dates: List[str]
    prices: List[float]

    @property
    def history_prices(self) -> List[float]:
        return self.prices[:HISTORY_SIZE]

    @property
    def future_prices(self) -> List[float]:
        return self.prices[HISTORY_SIZE:WINDOW_SIZE]

    @property
    def entry_price(self) -> float:
        return self.history_prices[-1]

    @property
    def exit_price(self) -> float:
        return self.future_prices[-1]


def _try_fetch(ticker: str) -> Optional[pd.DataFrame]:
    # Rastgele bir gecmis tarih araligi sec (son 90 gun haric, 2.5 yila kadar geriye git)
    days_back = random.randint(90, 900)
    end = dt.date.today() - dt.timedelta(days=days_back)
    start = end - dt.timedelta(days=int(WINDOW_SIZE * 1.7))
    try:
        df = yf.download(
            ticker,
            start=start.isoformat(),
            end=end.isoformat(),
            progress=False,
            auto_adjust=True,
        )
    except Exception:
        return None
    if df is None or df.empty or len(df) < WINDOW_SIZE:
        return None
    return df.tail(WINDOW_SIZE)


def fetch_random_window(max_attempts: int = 10) -> StockWindow:
    """Rastgele bir hisse ve rastgele bir gecmis zaman penceresi secip indirir."""
    tried = set()
    for _ in range(max_attempts):
        pool = [t for t in TICKER_POOL if t not in tried]
        if not pool:
            break
        ticker = random.choice(pool)
        tried.add(ticker)
        df = _try_fetch(ticker)
        if df is None:
            continue
        closes = df["Close"]
        if hasattr(closes, "squeeze"):
            closes = closes.squeeze()
        prices = [round(float(p), 2) for p in closes.tolist()]
        dates = [d.strftime("%Y-%m-%d") for d in df.index.to_pydatetime()]
        return StockWindow(ticker=ticker, dates=dates, prices=prices)
    raise RuntimeError(
        "Veri indirilemedi. Internet baglantinizi kontrol edin ya da tekrar deneyin."
    )