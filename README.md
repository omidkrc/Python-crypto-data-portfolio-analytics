# Cryptocurrency Data Analysis with Python

This repository contains a Python project for cryptocurrency data analysis. The project was originally prepared for a Financial Economics I course.

The analysis uses Yahoo Finance data and covers three main parts:

- price comparison and cumulative returns for major cryptocurrencies in 2022
- portfolio return, volatility, and Sharpe ratio analysis for Bitcoin, Ethereum, and Ripple
- a moving-average crossover trading strategy for Bitcoin

## Repository Structure

```text
crypto-analysis-python-project/
├── README.md
├── requirements.txt
├── notebooks/
│   └── crypto_analysis_400203402.ipynb
├── src/
│   └── crypto_analysis.py
├── figures/
│   ├── notebook_cell5_output0.png
│   ├── notebook_cell16_output0.png
│   └── portfolio_risk_return_plotly_clean.png
└── report/
    ├── crypto_analysis_report_en.pdf
    ├── crypto_analysis_report_en.tex
    └── original_report_fa.pdf
```

## Project Summary

### Part 1: Cryptocurrency price trends

The first part downloads 2022 price data for Bitcoin, Ethereum, Binance Coin, Ripple, and Cardano. The prices are normalized and plotted to compare their behavior over the year. The cumulative returns are also calculated.

### Part 2: Portfolio analysis

The second part builds portfolios using Bitcoin, Ethereum, and Ripple. Portfolio weights are chosen in 5 percent steps. For each portfolio, return, volatility, and Sharpe ratio are calculated. The risk-return plots show the possible portfolio combinations.

### Part 3: Bitcoin moving-average strategy

The third part tests moving-average crossover strategies for Bitcoin. Moving averages from 5 to 100 days are compared. The best strategy in the report is based on the 85-day and 80-day moving averages.

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Then open the notebook:

```bash
jupyter notebook notebooks/crypto_analysis_400203402.ipynb
```

You can also run the script version:

```bash
python src/crypto_analysis.py
```

## Notes

The project downloads data from Yahoo Finance through `yfinance`, so some results may change slightly if the data provider updates historical prices.

The English PDF report was generated from the LaTeX file in the `report/` folder. The original Persian report is also included for reference.
