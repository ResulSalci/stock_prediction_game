"""Oyun mantigi ve komut satiri arayuzu."""
from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from . import chart
from .data import fetch_random_window

STARTING_BALANCE = 10_000.0
STAKE_OPTIONS = {"1": 0.10, "2": 0.25, "3": 0.50}

console = Console()


class Game:
    def __init__(self) -> None:
        self.balance = STARTING_BALANCE
        self.streak = 0
        self.round = 1

    def status_table(self) -> Table:
        table = Table.grid(padding=(0, 3))
        table.add_row(
            f"[bold]Bakiye:[/bold] ${self.balance:,.0f}",
            f"[bold]Seri:[/bold] {self.streak}",
            f"[bold]Tur:[/bold] {self.round}",
        )
        return table

    def ask_direction(self) -> str:
        return Prompt.ask("Yon sec", choices=["long", "short"], default="long")

    def ask_stake(self) -> float:
        console.print("Pozisyon buyuklugu: [1] %10  [2] %25  [3] %50")
        choice = Prompt.ask("Sec", choices=list(STAKE_OPTIONS.keys()), default="2")
        return STAKE_OPTIONS[choice]

    def play_round(self) -> None:
        console.rule(f"Tur {self.round}")
        console.print(self.status_table())
        console.print("[dim]Gercek bir hisseden 60 gunluk gecmis veri indiriliyor...[/dim]")
        window = fetch_random_window()

        chart.plot_history(window, self.round)
        start_change = (
            (window.entry_price - window.history_prices[0]) / window.history_prices[0] * 100
        )
        console.print(
            Panel(
                f"Bugunku fiyat: ${window.entry_price:,.2f}\n"
                f"60 gunluk degisim: {start_change:+.1f}%",
                title="Gizli hisse",
            )
        )

        direction = self.ask_direction()
        stake_pct = self.ask_stake()

        entry_price = window.entry_price
        exit_price = window.exit_price
        pct_change = (exit_price - entry_price) / entry_price
        stake_amount = self.balance * stake_pct
        pnl = stake_amount * pct_change * (1 if direction == "long" else -1)
        new_balance = self.balance + pnl

        chart.plot_result(window, self.round, direction)

        pnl_color = "green" if pnl >= 0 else "red"
        console.print(
            Panel(
                f"Hisse: [bold]{window.ticker}[/bold]\n"
                f"Cikis fiyati: ${exit_price:,.2f}  (degisim: {pct_change * 100:+.1f}%)\n"
                f"Pozisyon: {direction.upper()} - ${stake_amount:,.0f}\n"
                f"[{pnl_color}]Kar/zarar: {pnl:+,.0f}$[/{pnl_color}]\n"
                f"Yeni bakiye: ${new_balance:,.0f}",
                title="Sonuc",
            )
        )

        self.balance = new_balance
        self.streak = self.streak + 1 if pnl > 0 else 0
        self.round += 1

    def run(self) -> None:
        console.print(
            Panel(
                "Gercek hisselerin gecmisini goreceksin, yon ve pozisyon buyuklugu secip "
                "sonraki 30 gunun ne yaptigini tahmin edeceksin. Hisse adi tahminden sonra aciklanir.",
                title="Market Signal",
            )
        )
        while True:
            try:
                self.play_round()
            except RuntimeError as exc:
                console.print(f"[red]{exc}[/red]")
                break
            if self.balance <= 0:
                console.print("[red]Bakiye sifirlandi, oyun bitti.[/red]")
                break
            again = Prompt.ask("Devam edilsin mi?", choices=["e", "h"], default="e")
            if again == "h":
                break
        console.print(f"Son bakiye: ${self.balance:,.0f} - Toplam tur: {self.round - 1}")