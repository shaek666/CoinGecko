import pandas as pd

# Load the CSV file
file_path = 'cleaned_coingecko_data.csv'
data = pd.read_csv(file_path)

# Pivot the data
pivoted_data = data.melt(  # Using the `melt` function to transform the DataFrame from wide format to long format
    id_vars=['Name', 'Symbol', 'Price Category'],  # Keeping these columns unchanged in the new format
    value_vars=['1h', '24h', '7d'],  # These columns contain the performance metrics over different timeframes
    var_name='Performance Metric',  # New column name for the time-based metric categories
    value_name='Performance Value'  # New column name for the values corresponding to the performance metrics
)

# Save the pivoted data
pivoted_data.to_csv('2_pivoted_data.csv', index=False)