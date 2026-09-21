# Python Market Data and Portfolio Analytics

## Overview

This repository contains a Financial Economics course project implemented in **Python**. It uses cryptocurrency market data as the application, but the main portfolio value is the analytical workflow: downloading market data, transforming prices into returns, comparing assets, evaluating portfolio risk-return combinations, computing Sharpe ratios, and testing a simple moving-average rule.

## Skills Demonstrated

- Python for financial and market-data analysis
- `pandas` / `NumPy` data manipulation
- Automated market-data retrieval with `yfinance`
- Return and cumulative-return calculations
- Portfolio return and volatility estimation
- Sharpe-ratio comparison across portfolio weights
- Data visualization with Matplotlib and Plotly
- Rule-based time-series strategy analysis
- Reproducible script and notebook workflows

## Project Components

### 1. Market-data comparison

The first section compares 2022 prices and cumulative returns for Bitcoin, Ethereum, Binance Coin, Ripple, and Cardano. Price indices are normalized to a common starting value to make cross-asset movements easier to compare.

### 2. Portfolio risk-return analysis

The second section evaluates portfolios of Bitcoin, Ethereum, and Ripple over a grid of weights. For each portfolio, the script calculates annualized return, volatility, and a Sharpe ratio under the course assumption of a zero risk-free rate.

### 3. Moving-average exercise

The final section evaluates simple Bitcoin moving-average rules over the 2022 sample. This is an **in-sample course exercise**, not evidence of a production trading strategy or out-of-sample profitability.

## Repository Structure

```text
crypto-python/
├── README.md
├── requirements.txt
├── notebooks/
│   └── crypto_analysis.ipynb
├── src/
│   └── crypto_analysis.py
├── figures/
└── report/
    ├── crypto_analysis_report_en.pdf
    ├── crypto_analysis_report_en.tex
    └── original_report_fa.pdf
```

## How to Run

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the cleaned script:

```bash
python src/crypto_analysis.py
```

Or open the original notebook:

```bash
jupyter notebook notebooks/crypto_analysis.ipynb
```

The analysis retrieves historical prices from Yahoo Finance through `yfinance`, so an internet connection is required. Provider-side revisions can cause small differences in rerun outputs.

## Notes

The cleaned Python script keeps the analytical structure of the course project while making the data download, normalization, portfolio grid, and output handling more robust. The English PDF report is provided under `report/`, together with the original Persian report for reference.

## Author

**Omid Karami**

Financial Economics coursework and Python portfolio project.
