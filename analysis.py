import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set design aesthetics
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 6)

def perform_analysis():
    print("Loading datasets...")
    # Load data
    hist_df = pd.read_csv('historical_data.csv')
    fg_df = pd.read_csv('fear_greed_index.csv')

    print("Cleaning and formatting timestamps...")
    # Conver historical data timestamp to date
    # Format: 02-12-2024 22:50
    hist_df['Timestamp IST'] = pd.to_datetime(hist_df['Timestamp IST'], format='%d-%m-%Y %H:%M')
    hist_df['Date'] = hist_df['Timestamp IST'].dt.strftime('%Y-%m-%Y') # Standardizing to YYYY-MM-DD
    # Wait, 02-12-2024 is DD-MM-YYYY.
    hist_df['Date'] = hist_df['Timestamp IST'].dt.strftime('%Y-%m-%d')
    hist_df['Closed PnL'] = pd.to_numeric(hist_df['Closed PnL'], errors='coerce').fillna(0)
    hist_df['Size USD'] = pd.to_numeric(hist_df['Size USD'], errors='coerce').fillna(0)

    # Convert Fear/Greed data date
    fg_df['Date'] = pd.to_datetime(fg_df['date']).dt.strftime('%Y-%m-%d')

    print("Aggregating historical trader data by date...")
    # Aggregating metrics by date
    daily_trader_stats = hist_df.groupby('Date').agg({
        'Closed PnL': ['sum', 'count', 'mean'],
        'Size USD': 'sum',
        'Account': 'nunique'
    }).reset_index()

    # Flatten the columns
    daily_trader_stats.columns = ['Date', 'Total_PnL', 'Total_Trades', 'Avg_PnL_per_Trade', 'Total_Volume_USD', 'Unique_Traders']

    print("Merging with sentiment data...")
    # Merge with Fear/Greed Index
    merged_df = pd.merge(daily_trader_stats, fg_df[['Date', 'value', 'classification']], on='Date', how='inner')

    if merged_df.empty:
        print("Warning: Merged dataframe is empty. There might be no overlap in date ranges.")
        # Check date ranges
        print(f"Historical Data Date Range: {hist_df['Date'].min()} to {hist_df['Date'].max()}")
        print(f"Fear/Greed Data Date Range: {fg_df['Date'].min()} to {fg_df['Date'].max()}")
        return

    print(f"Merged {len(merged_df)} days of data.")

    # 1. Performance vs. Sentiment Classification
    plt.figure()
    perf_by_class = merged_df.groupby('classification')['Total_PnL'].mean().sort_values()
    perf_by_class.plot(kind='bar', color='teal')
    plt.title('Average Daily PnL vs. Market Sentiment Classification')
    plt.ylabel('Average PnL (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('pnl_vs_sentiment_class.png')
    print("Saved pnl_vs_sentiment_class.png")

    # 2. Activity (Volume) vs. Sentiment Classification
    plt.figure()
    vol_by_class = merged_df.groupby('classification')['Total_Volume_USD'].mean().sort_values()
    vol_by_class.plot(kind='bar', color='orange')
    plt.title('Average Daily Trading Volume vs. Market Sentiment Classification')
    plt.ylabel('Average Volume (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('volume_vs_sentiment_class.png')
    print("Saved volume_vs_sentiment_class.png")

    # 3. Correlation Matrix
    plt.figure()
    corr = merged_df[['Total_PnL', 'Total_Trades', 'Total_Volume_USD', 'Unique_Traders', 'value']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix: Trader Metrics vs. Sentiment Value')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')
    print("Saved correlation_matrix.png")

    # 4. Scatter Plot: Sentiment Value vs. Total PnL
    plt.figure()
    sns.scatterplot(data=merged_df, x='value', y='Total_PnL', hue='classification', palette='viridis', alpha=0.7)
    plt.title('Fear/Greed Value vs. Daily Total PnL')
    plt.xlabel('Fear/Greed Value (0-100)')
    plt.ylabel('Daily Total PnL (USD)')
    plt.savefig('sentiment_value_vs_pnl_scatter.png')
    print("Saved sentiment_value_vs_pnl_scatter.png")

    # Calculate some key statistics
    sentiment_cor = corr.loc['Total_PnL', 'value']
    print(f"\nCorrelation between Sentiment Value and Daily PnL: {sentiment_cor:.4f}")
    
    # Win Rate Approximation (profitable days per classification)
    merged_df['Is_Profitable_Day'] = merged_df['Total_PnL'] > 0
    win_rate_per_class = merged_df.groupby('classification')['Is_Profitable_Day'].mean() * 100
    print("\nWin Rate (%) of profitable days by Sentiment Classification:")
    print(win_rate_per_class)

    # Save summary report
    with open('analysis_report.txt', 'w') as fr:
        fr.write("Analysis Report: Trader Performance vs. Market Sentiment\n")
        fr.write("="*55 + "\n")
        fr.write(f"Overlap Period: {merged_df['Date'].min()} to {merged_df['Date'].max()}\n")
        fr.write(f"Total Combined Days: {len(merged_df)}\n\n")
        fr.write(f"Correlation (PnL vs Sentiment Value): {sentiment_cor:.4f}\n\n")
        fr.write("Average Daily Performance per Sentiment Classification:\n")
        fr.write(perf_by_class.to_string() + "\n\n")
        fr.write("Average Daily Volume per Sentiment Classification:\n")
        fr.write(vol_by_class.to_string() + "\n\n")
        fr.write("Profitable Day Rate (%) per Sentiment Classification:\n")
        fr.write(win_rate_per_class.to_string() + "\n")

if __name__ == "__main__":
    perform_analysis()
