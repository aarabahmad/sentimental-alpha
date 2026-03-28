# PrimeTradeAI: Sentiment-Driven Trading Performance Analysis

Welcome to the **PrimeTradeAI Sentiment Analysis Suite**. This project explores the relationship between historical trader performance (from Hyperliquid) and the Bitcoin Market Sentiment (Fear & Greed Index).

## 📊 Project Overview
The core objective of this analysis is to uncover how market sentiment influences trader profitability, volume, and win rates. By merging daily sentiment scores with high-frequency historical trade data, we've identified key regimes where traders achieve their highest 'Alpha'.

### Key Datasets
- **`historical_data.csv`**: Granular trader execution data including PnL, size, side, and timestamps.
- **`fear_greed_index.csv`**: Historical Bitcoin Market Sentiment data (0-100 values and classifications).

## 🚀 Key Insights
- **The Fear Advantage**: Traders achieve their highest average daily PnL ($52,793) during periods of **Extreme Fear**, compared to just $11,141 during Greed.
- **Volatility Engine**: Trading volume spikes by over 750% during capitulation events (Extreme Fear).
- **Consistency vs. Magnitude**: Extreme Greed has the highest "Win Rate" (87.7%) but lower absolute profit per day.

## 📁 Repository Structure
- `analysis.py`: The main Python script used for data cleaning, aggregation, and visualization.
- `Trading_Intelligence_Report.md`: A formal document with strategic inferences and actionable conclusions.
- `requirements.txt`: Python dependencies required to run the analysis.
- `analysis_report.txt`: Automatically generated statistical summary.
- `*.png`: Visualizations of PnL, Volume, and Correlation matrices.

## 🛠️ Getting Started

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Run the Analysis
To regenerate the reports and visualizations:
```bash
python analysis.py
```

## 📜 Final Findings
For a deep dive into the strategic conclusions of this study, please refer to the [Trading Intelligence Report](Trading_Intelligence_Report.md).

---
*Created as part of the PrimeTradeAI Intelligence Suite.*
