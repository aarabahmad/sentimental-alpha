import pandas as pd
import sys

# Set precision to avoid E+ notation for small IDs
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

with open('research_output.txt', 'w') as f:
    try:
        hist_df = pd.read_csv('historical_data.csv', nrows=5)
        f.write("Historical Data Header:\n")
        f.write(str(hist_df.columns.tolist()) + "\n\n")
        f.write("Historical Data Sample:\n")
        f.write(str(hist_df) + "\n\n")
        
        fg_df = pd.read_csv('fear_greed_index.csv', nrows=5)
        f.write("Fear/Greed Data Header:\n")
        f.write(str(fg_df.columns.tolist()) + "\n\n")
        f.write("Fear/Greed Data Sample:\n")
        f.write(str(fg_df) + "\n\n")
        
    except Exception as e:
        f.write(f"Error reading files: {e}\n")
