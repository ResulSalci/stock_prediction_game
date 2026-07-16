"""Grafik cizim modulu (matplotlib)."""
from __future__ import annotations

import os

import matplotlib.pyplot as plt

from .data import StockWindow

OUTPUT_DIR = "charts"


def _ensure_output_dir() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_history(window: StockWindow, round_no: int, block: bool = True) -> str:
    """Sadece gecmis 60 gunu gosterir (hisse adi gizli)."""
    _ensure_output_dir()
    hist = window.history_prices
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(range(len(hist)), hist, color="#2a78d6", linewidth=2)
    ax.set_title(f"Tur {round_no} - Gizli hisse (60 gunluk gecmis)")
    ax.set_xlabel("Gun")
    ax.set_ylabel("Fiyat ($)")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, f"round_{round_no}_history.png")
    fig.savefig(path, dpi=120)
    if block:
        plt.show()
    plt.close(fig)
    return path


def plot_result(window: StockWindow, round_no: int, direction: str, block: bool = True) -> str:
    """Gecmis + gercek sonucu birlikte gosterir."""
    _ensure_output_dir()
    hist = window.history_prices
    fut = window.future_prices
    x_hist = list(range(len(hist)))
    x_fut = list(range(len(hist) - 1, len(hist) - 1 + len(fut) + 1))
    fut_with_join = [hist[-1]] + fut

    outcome_color = "#1baf7a" if fut[-1] >= hist[-1] else "#e34948"

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(x_hist, hist, color="#2a78d6", linewidth=2, label="Gecmis")
    ax.plot(x_fut, fut_with_join, color=outcome_color, linewidth=2, label="Gercek sonuc")
    ax.axvline(len(hist) - 1, color="#eda100", linestyle="--", linewidth=1, label="Bugun")
    ax.set_title(f"Tur {round_no} - {window.ticker} ({direction.upper()})")
    ax.set_xlabel("Gun")
    ax.set_ylabel("Fiyat ($)")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, f"round_{round_no}_result_{window.ticker}.png")
    fig.savefig(path, dpi=120)
    if block:
        plt.show()
    plt.close(fig)
    return path