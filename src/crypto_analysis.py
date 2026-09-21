"""Market data and portfolio analytics course project.

This script is a cleaned, portable version of the original notebook. It keeps
the original analytical scope while making data downloads, normalization,
portfolio construction, and output handling more robust.
"""

from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = ROOT / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)
FIGURE_DIR.mkdir(exist_ok=True)

ANNUALIZATION_DAYS = 365
RISK_FREE_RATE = 0.0


def download_prices(tickers, start, end, adjusted=False):
    """Download close or adjusted-close prices as a DataFrame."""
    raw = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        group_by="column",
    )

    if raw.empty:
        raise RuntimeError(f"No price data returned for {tickers}.")

    field = "Adj Close" if adjusted else "Close"

    if isinstance(raw.columns, pd.MultiIndex):
        available = raw.columns.get_level_values(0)
        if field not in available:
            field = "Close"
        prices = raw[field].copy()
    else:
        if field in raw.columns:
            prices = raw[[field]].copy()
        elif "Close" in raw.columns:
            prices = raw[["Close"]].copy()
        else:
            raise RuntimeError("Downloaded data do not contain a close-price field.")

    if isinstance(prices, pd.Series):
        prices = prices.to_frame()

    if isinstance(tickers, str):
        prices.columns = [tickers]

    return prices.sort_index()


def normalize_to_100(prices):
    """Normalize each price series to 100 at its first valid observation."""
    return prices.apply(lambda s: s / s.dropna().iloc[0] * 100)


def portfolio_grid(prices):
    """Evaluate long-only portfolio weights in five-percentage-point steps."""
    log_returns = np.log(prices / prices.shift(1)).dropna()
    annual_returns = log_returns.mean() * ANNUALIZATION_DAYS
    annual_cov = log_returns.cov() * ANNUALIZATION_DAYS

    rows = []
    weights = np.arange(0.0, 1.0001, 0.05)

    for w_btc, w_eth, w_xrp in product(weights, repeat=3):
        if not np.isclose(w_btc + w_eth + w_xrp, 1.0):
            continue

        w = np.array([w_btc, w_eth, w_xrp], dtype=float)
        port_return = float(np.dot(annual_returns.values, w))
        port_var = float(w.T @ annual_cov.values @ w)
        port_vol = float(np.sqrt(max(port_var, 0.0)))
        sharpe = np.nan if port_vol == 0 else (port_return - RISK_FREE_RATE) / port_vol

        rows.append(
            {
                "bitcoin_weight": w_btc,
                "ethereum_weight": w_eth,
                "ripple_weight": w_xrp,
                "annualized_return": port_return,
                "annualized_volatility": port_vol,
                "sharpe_ratio": sharpe,
            }
        )

    return pd.DataFrame(rows)


def moving_average_grid(price_series):
    """Evaluate simple in-sample 2022 moving-average rules.

    The original course exercise applies a 0.95 multiplier to daily returns in
    the transaction-adjusted wealth calculation. It is retained here as a
    course assumption rather than presented as a realistic transaction-cost model.
    """
    price_series = price_series.dropna()
    returns = price_series.pct_change(fill_method=None)
    evaluation = price_series.loc["2022-01-01":"2022-12-31"]

    rows = []
    for long_window in range(10, 101, 5):
        for short_window in range(5, long_window, 5):
            short_ma = price_series.rolling(short_window).mean()
            long_ma = price_series.rolling(long_window).mean()

            wealth = 1.0
            adjusted_wealth = 1.0
            buy_days = 0
            sell_days = 0

            for date in evaluation.index:
                if pd.isna(short_ma.loc[date]) or pd.isna(long_ma.loc[date]):
                    continue
                r = returns.loc[date]
                if pd.isna(r):
                    continue

                if short_ma.loc[date] > long_ma.loc[date]:
                    buy_days += 1
                    wealth *= 1.0 + r
                    adjusted_wealth *= 1.0 + 0.95 * r
                elif long_ma.loc[date] > short_ma.loc[date]:
                    sell_days += 1

            rows.append(
                {
                    "long_window": long_window,
                    "short_window": short_window,
                    "buy_days": buy_days,
                    "sell_days": sell_days,
                    "wealth_ratio": wealth,
                    "course_adjusted_wealth_ratio": adjusted_wealth,
                }
            )

    return pd.DataFrame(rows)


def main():
    # ------------------------------------------------------------------
    # Part 1: market-data comparison
    # ------------------------------------------------------------------
    tickers_2022 = ["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD"]
    names_2022 = {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
        "BNB-USD": "Binance Coin",
        "XRP-USD": "Ripple",
        "ADA-USD": "Cardano",
    }

    prices_2022 = download_prices(tickers_2022, "2022-01-01", "2023-01-01")
    prices_2022 = prices_2022.rename(columns=names_2022)

    normalized = normalize_to_100(prices_2022)
    normalized.plot(figsize=(12, 6), title="Cryptocurrency Price Indices (Start = 100)")
    plt.ylabel("Index")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "crypto_price_indices.png", dpi=150)
    plt.close()

    simple_returns = prices_2022.pct_change(fill_method=None)
    cumulative_returns = (1.0 + simple_returns).prod() - 1.0
    cumulative_returns.to_csv(OUTPUT_DIR / "cumulative_returns_2022.csv", header=["return"])

    # ------------------------------------------------------------------
    # Part 2: conditional return comparison
    # ------------------------------------------------------------------
    tickers_conditional = [
        "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD",
        "DOGE-USD", "SOL-USD", "MATIC-USD", "TRX-USD", "LTC-USD",
    ]
    conditional_prices = download_prices(
        tickers_conditional, "2022-12-26", "2023-06-26"
    )
    conditional_returns = conditional_prices.pct_change(fill_method=None)
    btc_returns = conditional_returns["BTC-USD"]

    positive_days = (conditional_returns > 0).sum()
    negative_days = (conditional_returns < 0).sum()
    pd.DataFrame(
        {"positive_days": positive_days, "negative_days": negative_days}
    ).to_csv(OUTPUT_DIR / "positive_negative_days.csv")

    when_btc_positive = (1.0 + conditional_returns.loc[btc_returns > 0]).prod() - 1.0
    when_btc_negative = (1.0 + conditional_returns.loc[btc_returns < 0]).prod() - 1.0
    pd.DataFrame(
        {
            "btc_positive_days": when_btc_positive,
            "btc_negative_days": when_btc_negative,
        }
    ).to_csv(OUTPUT_DIR / "conditional_cumulative_returns.csv")

    # ------------------------------------------------------------------
    # Part 3: portfolio risk-return grid
    # ------------------------------------------------------------------
    portfolio_prices = download_prices(
        ["BTC-USD", "ETH-USD", "XRP-USD"], "2022-01-01", "2023-01-01"
    )
    portfolio_prices = portfolio_prices.rename(
        columns={"BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "XRP-USD": "Ripple"}
    )

    portfolios = portfolio_grid(portfolio_prices)
    portfolios.to_csv(OUTPUT_DIR / "portfolio_grid.csv", index=False)

    fig = go.Figure(
        data=go.Scatter(
            x=portfolios["annualized_volatility"],
            y=portfolios["annualized_return"],
            mode="markers",
            marker={
                "color": portfolios["sharpe_ratio"],
                "showscale": True,
                "size": 7,
                "colorbar": {"title": "Sharpe Ratio"},
            },
        )
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Annualized Volatility",
        yaxis_title="Annualized Return",
        title="Portfolio Risk-Return Grid",
    )
    fig.write_html(OUTPUT_DIR / "portfolio_risk_return.html")

    best_portfolio = portfolios.loc[portfolios["sharpe_ratio"].idxmax()]
    print("\nHighest-Sharpe portfolio in the five-percentage-point grid:")
    print(best_portfolio)

    # ------------------------------------------------------------------
    # Part 4: moving-average course exercise
    # ------------------------------------------------------------------
    btc = download_prices(
        "BTC-USD", "2021-09-01", "2023-01-01", adjusted=True
    )["BTC-USD"]

    ma_results = moving_average_grid(btc)
    ma_results.to_csv(OUTPUT_DIR / "moving_average_grid.csv", index=False)

    best_raw = ma_results.loc[ma_results["wealth_ratio"].idxmax()]
    best_adjusted = ma_results.loc[
        ma_results["course_adjusted_wealth_ratio"].idxmax()
    ]

    print("\nBest in-sample moving-average rule by raw wealth ratio:")
    print(best_raw)
    print("\nBest in-sample moving-average rule under the course adjustment:")
    print(best_adjusted)


if __name__ == "__main__":
    main()
